"""File profile for de-identifying dicom files"""
import collections
import datetime
import gzip
import logging
import os
import re
import sys
import tempfile

import pydicom
import pydicom.datadict
import pydicom.tag
from pydicom.filewriter import writers
from pydicom.charset import text_VRs
from pydicom.data import get_testdata_files
import six
from fs.osfs import OSFS
from flywheel_metadata.file.dicom.fixer import fw_pydicom_config

from ..util import (
    date_delta,
    is_dicom,
    dict_paths,
    walk_dicom_wild_sequence,
    get_dicom_record_attributes,
)
from .file_profile import FileProfile
from .deid_field import DeIdField, DeIdFieldMixin

log = logging.getLogger(__name__)

DICOM_TAG_HEX_RE = re.compile(r"^(0x)?[0-9a-fA-F]{8}$")
DICOM_TAG_TUPLE_RE = re.compile(r"\(\s*([0-9a-fA-F]{4})\s*,\s*([0-9a-fA-F]{4})\s*\)")
# match data element in sequence
DICOM_NESTED_RE = re.compile(
    r"^(?:([0-9A-Fa-f]{8}|[\w]+)\.([\d]?[*]?)\.)+([0-9A-Fa-f]{8}|[\w]+)$"
)


class DicomTagStr(str):
    """Subclass of string that host attributes/methods to handle the different means
    field can reference Dicom data element(s)"""

    # list of methods to be used for parsing field name
    parsers_method_names = ["parse_tag_tuple", "parse_tag_hex", "parse_nested"]

    def __new__(cls, value, *_args, **_kwargs):
        if isinstance(value, int):
            # for human readable representation of hex
            value = str(pydicom.tag.Tag(value))
        return super(DicomTagStr, cls).__new__(cls, value)

    def __init__(self, _value, *args, **kwargs):
        super(DicomTagStr, self).__init__(*args, **kwargs)
        self._is_sequence = False
        self._is_private = False
        self._dicom_tag = self.parse_field_name(_value)
        self._is_wild_sequence = None

    @property
    def dicom_tag(self):
        return self._dicom_tag

    @property
    def is_sequence(self):
        return self._is_sequence

    @property
    def is_private(self):
        return self._is_private

    @property
    def is_wild_sequence(self):
        if self._is_wild_sequence is None:
            if self.dicom_tag and self.is_sequence and "*" in self.dicom_tag:
                self._is_wild_sequence = True
            else:
                self._is_wild_sequence = False
        return self._is_wild_sequence

    def parse_tag_tuple(self, name):
        """Process a field name of type tuple (e.g. (0010, 0020)).

        Args:
            name (str): A field name.

        Returns:
            pydicom.Tag or None: If name matches DICOM_TAG_TUPLE_RE, returns a Tag,
              None otherwise.
        """
        match = DICOM_TAG_TUPLE_RE.match(name)
        if match:
            # converting "GGGG"+"EEEE" to hex int, then Tag.
            return pydicom.tag.Tag(int(match.group(1) + match.group(2), 16))
        return None

    def parse_tag_hex(self, name):
        """Process a field name of type hex notation (e.g. 0x00100020).

        Args:
            name (str): A field name.

        Returns:
            pydicom.Tag or None: If name matches DICOM_TAG_HEX_RE, returns a Tag,
              None otherwise.
        """
        match = DICOM_TAG_HEX_RE.match(name)
        if match:
            # converting "GGGGEEEE" hex int, then Tag.
            return pydicom.tag.Tag(int(name, 16))
        return None

    def parse_nested(self, name):
        """Process a field name of type nested sequence (e.g. BlaSequence.0.Keyword
        but can be any arbitrary depth).

        Args:
            name (str): A field name.

        Returns:
            list or None: If ``name`` matches DICOM_NESTED_RE, returns a list of
               [Tag, index, Tag, ...] (odd number of items), None otherwise.
        """
        match = DICOM_NESTED_RE.match(name)
        if match:
            # breaking dotty string in its part (either keyword, hex int or *)
            nested_seq_items = re.findall(r"((?:0x)?[0-9A-Fa-f]{8}|[\w]+|[*])+", name)
            tag_seq = []
            for i, item in enumerate(nested_seq_items):
                if i % 2 == 0:  # even i are either keyword or hex tag
                    if DICOM_TAG_HEX_RE.match(item):
                        # convert as keyword
                        tag_seq.append(pydicom.datadict.dictionary_keyword(item))
                    else:
                        tag_seq.append(item)
                else:  # odd i are expected to be coercible as integer or being '*'
                    if item == "*":
                        tag_seq.append(item)
                    else:
                        tag_seq.append(int(item))
            self._is_sequence = True
            return tag_seq
        return None

    def parse_field_name(self, name):
        """Parse the field name and returns

        Args:
            name (str): The field name.

        Returns:
            (list or Tag): Depending on name.

        Raises:
            ValueError: if name matches multiple fieldname definition types.
        """
        if isinstance(name, int):
            return pydicom.tag.Tag(name)

        name = name.strip()

        # process all parsers to checking for uniqueness of match
        parsers = [getattr(self, meth_name) for meth_name in self.parsers_method_names]
        parsers_res = map(lambda f: f(name), parsers)
        parsers_res = list(filter(None, parsers_res))

        if len(parsers_res) > 1:
            raise ValueError(f"{name} matches multiple name type definition")
        elif len(parsers_res) == 1:
            return parsers_res[0]
        else:
            return None


class DicomDeIdFieldMixin(DeIdFieldMixin):
    """Mixin to add functionality to DeIdField for Dicom profile"""

    flavor = "Dicom"

    def deidentify(self, profile, state, record):
        """Deidentifies depending on field type"""
        if self.is_regex:
            self._deidentify_regex_field(profile, state, record)
        elif self.fieldname.is_wild_sequence:
            self._deidentify_wild_sequence_field(profile, state, record)
        else:
            super(DicomDeIdFieldMixin, self).deidentify(profile, state, record)

    def list_fieldname(self, record):
        """Returns a list of fieldnames for record depending on field type"""
        if self.is_regex:
            return self._list_fieldname_regex_field(record)
        elif self.fieldname.is_wild_sequence:
            return self._list_fieldname_wild_sequence(record)
        else:
            return super(DicomDeIdFieldMixin, self).list_fieldname(record)

    def _list_fieldname_wild_sequence(self, record):
        """Returns list of Dicom data element paths as list of keyword and indices
        defined as nested element with wild card (e.g. keyword1.*.keyword2)"""
        dict_tree = walk_dicom_wild_sequence(record, self.fieldname.dicom_tag)
        dcm_tags = list(dict_paths(dict_tree))
        return dcm_tags

    def _deidentify_wild_sequence_field(self, profile, state, record):
        """Find all occurrences by expanding wild card and perform the update"""
        # Replicate field
        dcm_tags = self.list_fieldname(record)
        for tag in dcm_tags:
            fieldname = DicomTagStr(".".join(map(str, tag)))
            tmp_field = DeIdField.factory(
                {"name": fieldname, self.key: getattr(self, "value", True)}
            )
            tmp_field.deidentify(profile, state, record)

    def _list_fieldname_regex_field(self, record):
        """Returns all dicom record attributes, in dotty-notation, matching regex.

        For example, r"*InstanceUID.*" would return of all dotty-path matching
        .*InstanceUID.* such as StudyInstanceUID and any nested element in Sequences
        such as "SomeSequence.0.ReferencedSOPInstanceUID".
        """
        fieldnames = []
        attrs = get_dicom_record_attributes(record)
        reg = re.compile(self.fieldname)
        for attr in attrs:
            match = reg.match(attr)
            if match:
                fieldnames.append(attr)
        return fieldnames

    def _deidentify_regex_field(self, profile, state, record):
        """Deidentify each data element matching regex"""
        # Replicate field
        fieldnames = self.list_fieldname(record)
        for fieldname in fieldnames:
            tmp_field = DeIdField.factory(
                {"name": fieldname, self.key: getattr(self, "value", True)}
            )
            tmp_field.fieldname = DicomTagStr(fieldname)
            tmp_field.deidentify(profile, state, record)


class DicomFileProfile(FileProfile):
    """Dicom implementation of load/save and remove/replace fields"""

    name = "dicom"
    hash_digits = 16  # How many digits are supported for 'hash' action
    log_fields = ["StudyInstanceUID", "SeriesInstanceUID", "SOPInstanceUID"]
    regex_compatible = True
    decode = True  # If set to True, will attempt to decode the record upon loading
    deidfield_mixin = DicomDeIdFieldMixin

    def __init__(self):
        super(DicomFileProfile, self).__init__(packfile_type="dicom")

        self.patient_age_from_birthdate = False
        self.patient_age_units = None

        self.remove_private_tags = False

        # set of all lower-cased DICOM keywords, for later validate()
        self.lc_kw_dict = {
            keyword.lower(): keyword
            for keyword in pydicom.datadict.keyword_dict
            if keyword  # non-blank
        }

    def add_field(self, field):
        # Handle tag conversion for later
        field.fieldname = DicomTagStr(field.fieldname)
        super(DicomFileProfile, self).add_field(field)

    def create_file_state(self):
        """Create state object for processing files"""
        return {"series_uid": None, "session_uid": None, "sop_uids": set()}

    def get_dest_path(self, state, record, path):
        """Return default named based on SOPInstanceUID or one based on profile if defined"""
        if not self.filenames:
            # Destination path is sop_uid.modality.dcm
            sop_uid = self.get_value(state, record, "SOPInstanceUID")
            if not sop_uid:
                return path
            modality = self.get_value(state, record, "Modality") or "NA"
            dest_path = "{}.{}.dcm".format(sop_uid, modality.replace("/", "_"))
        else:
            dest_path = super(DicomFileProfile, self).get_dest_path(state, record, path)
        return dest_path

    def to_config(self):
        result = super(DicomFileProfile, self).to_config()

        result["patient-age-from-birthdate"] = self.patient_age_from_birthdate
        if self.patient_age_units:
            result["patient-age-units"] = self.patient_age_units

        result["remove-private-tags"] = self.remove_private_tags

        if self.decode != self.__class__.decode:
            result["decode"] = self.decode

        return result

    def load_config(self, config):
        super(DicomFileProfile, self).load_config(config)

        self.patient_age_from_birthdate = config.get(
            "patient-age-from-birthdate", False
        )
        self.patient_age_units = config.get("patient-age-units")
        self.remove_private_tags = config.get("remove-private-tags", False)
        self.decode = config.get("decode", self.__class__.decode)

    @fw_pydicom_config()
    def load_record(self, state, src_fs, path):  # pylint: disable=too-many-branches
        modified = False
        try:
            with src_fs.open(path, "rb") as f:
                # Extract gzipped dicoms
                _, ext = os.path.splitext(path)
                if ext.lower() == ".gz":
                    f = gzip.GzipFile(fileobj=f)

                # Read and decode the dicom
                dcm = pydicom.dcmread(f, force=True)

                # Remove private tags before decoding
                if self.remove_private_tags:
                    dcm.remove_private_tags()
                    modified = True

                if self.decode:
                    dcm.decode()

                if not dcm.dir():
                    # assuming that a Dicom has at least one known tag
                    raise TypeError("Not a DICOM file")

        except Exception:  # pylint: disable=broad-except
            if not is_dicom(src_fs, path):
                log.warning("IGNORING %s - it is not a DICOM file!", path)
                return None, False
            if self.deid_name != "none":
                log.warning("IGNORING %s - cannot deid an invalid DICOM file!", path)
                return None, False

            log.warning('Packing invalid dicom %s because deid profile is "none"', path)
            return True, False

        # Validate the series/session
        series_uid = dcm.get("SeriesInstanceUID")
        session_uid = dcm.get("StudyInstanceUID")

        if state["series_uid"] is not None:
            # Validate SeriesInstanceUID
            if series_uid != state["series_uid"]:
                log.warning(
                    "DICOM %s has a different SeriesInstanceUID (%s) from the rest of the series: %s",
                    path,
                    series_uid,
                    state["series_uid"],
                )
            # Validate StudyInstanceUID
            elif session_uid != state["session_uid"]:
                log.warning(
                    "DICOM %s has a different StudyInstanceUID (%s) from the rest of the series: %s",
                    path,
                    session_uid,
                    state["session_uid"],
                )
        else:
            state["series_uid"] = series_uid
            state["session_uid"] = session_uid

        # Validate SOPInstanceUID
        sop_uid = dcm.get("SOPInstanceUID")
        if sop_uid:
            if sop_uid in state["sop_uids"]:
                log.error(
                    "DICOM %s re-uses SOPInstanceUID %s, and will be excluded!",
                    path,
                    sop_uid,
                )
                return None, False
            state["sop_uids"].add(sop_uid)

        # Set patient age from date of birth, if specified
        if self.patient_age_from_birthdate:
            dob = dcm.get("PatientBirthDate")
            study_date = dcm.get("StudyDate")

            if dob and study_date:
                try:
                    study_date = datetime.datetime.strptime(
                        study_date, self.date_format
                    )
                    dob = datetime.datetime.strptime(dob, self.date_format)

                    # Max value from dcm.py:84
                    age, units = date_delta(
                        dob,
                        study_date,
                        desired_unit=self.patient_age_units,
                        max_value=960,
                    )
                    dcm.PatientAge = "%03d%s" % (age, units)
                    modified = True
                except ValueError as err:
                    log.debug("Unable to update patient age in file %s: %s", path, err)

        return dcm, modified

    def save_record(self, state, record, dst_fs, path):
        with dst_fs.open(path, "wb") as f:
            record.save_as(f)

    def read_field(self, state, record, fieldname):
        # Ensure that value is a string
        # dcm_tag = getattr(fieldname, "_dicom_tag", None)
        # is_seq = getattr(fieldname, "_is_sequence", False)
        if isinstance(fieldname, DicomTagStr) and fieldname.dicom_tag:
            value = None
            if fieldname.is_sequence:
                value = self._get_field_if_sequence(record, fieldname.dicom_tag)
            else:
                data_element = record.get(fieldname.dicom_tag)
                if data_element is not None:
                    value = record.get(fieldname.dicom_tag).value
        else:
            value = getattr(record, fieldname, None)

        if value is not None and not isinstance(value, six.string_types):
            if isinstance(value, collections.Sequence):
                value = ",".join([str(x) for x in value])
            else:  # Unknown value, just convert to string
                value = str(value)
        return value

    def _get_field_if_sequence(self, record, tag):
        """Return data element corresponding to tag"""
        if not len(tag) == 1:
            try:
                return self._get_field_if_sequence(record[tag[0]], tag[1:])
            except (IndexError, KeyError):
                return None
        return record.get(tag[0])

    def _get_or_create_field_if_sequence(self, record, tag):
        """Return DataElement according to tag creating it if does not exist"""
        if not len(tag) == 1:
            try:
                return self._get_or_create_field_if_sequence(record[tag[0]], tag[1:])
            except IndexError:  # extend sequence range
                for _ in range(len(record.value), tag[0] + 1):
                    record.value.append(pydicom.dataset.Dataset())
                return self._get_or_create_field_if_sequence(record[tag[0]], tag[1:])
            except KeyError:  # create sequence
                setattr(record, tag[0], None)
                return self._get_or_create_field_if_sequence(record[tag[0]], tag[1:])
        try:
            return record[tag[0]]
        except KeyError:  # Note: ValueError is raised if tag[0] is not a public tag/keyword
            setattr(record, tag[0], None)
            return record[tag[0]]
        except IndexError:  # extend sequence range
            for _ in range(len(record.value), tag[0] + 1):
                record.value.append(pydicom.dataset.Dataset())

    def remove_field(self, state, record, fieldname):
        if isinstance(fieldname, DicomTagStr) and fieldname.dicom_tag:
            if fieldname.is_sequence:  # this is a sequence
                self._remove_field_if_sequence(record, fieldname.dicom_tag)
            elif fieldname.dicom_tag in record:
                del record[fieldname.dicom_tag]
        else:
            if hasattr(record, fieldname):
                delattr(record, fieldname)

    def _remove_field_if_sequence(self, record, tag):
        """Remove value on tag list, recursively"""
        if len(tag) == 1:
            if tag[0] in record:
                del record[tag[0]]
        else:
            try:
                self._remove_field_if_sequence(record[tag[0]], tag[1:])
            except (KeyError, ValueError):
                pass

    def replace_field(self, state, record, fieldname, value):
        if isinstance(fieldname, DicomTagStr) and fieldname.dicom_tag:
            if fieldname.is_sequence:  # this is a sequence
                de = self._get_or_create_field_if_sequence(record, fieldname.dicom_tag)
                de.value = value
            else:
                try:
                    record[fieldname.dicom_tag].value = value
                except KeyError:
                    # checking public dictionary to get corresponding VR
                    # if not found, log error and exit until we have a better support
                    # for it
                    try:
                        vr = pydicom.datadict.dictionary_VR(fieldname.dicom_tag)
                    except KeyError:
                        log.error(
                            f"Invalid replace-with action. Unknown VR for tag {fieldname.dicom_tag}."
                        )
                        sys.exit(1)
                    record.add_new(fieldname.dicom_tag, vr, value)
        else:
            setattr(record, fieldname, value)

    def validate_filenames(self, errors):
        """Validate the filename section of the profile,

        Args:
            errors (list): Current list of error message

        Returns:
            (list): Extended list of errors message
        """

        for filename in self.filenames:
            group_names = []
            if filename.get("input-regex"):  # check regexp
                try:
                    regex = re.compile(filename.get("input-regex"))
                    group_names = [x.lower() for x in regex.groupindex.keys()]
                except re.error:
                    # errors got log already in superclass method, still needs group_names for following validation
                    continue

            # check group do not collide with dicom keyword
            lc_kw_list = list(self.lc_kw_dict.keys())
            for grp in group_names:
                if grp in lc_kw_list:
                    errors.append(
                        f"regex group {grp} must be unique. Currently colliding with Dicom keywords"
                    )

            # check output filename keyword are valid
            kws = re.findall(r"\{([^}]+)\}", filename["output"])
            lc_kw_list = list(self.lc_kw_dict.keys()) + group_names
            for kw in kws:
                lc_kw = kw.lower()
                if lc_kw not in lc_kw_list:
                    errors.append(
                        f"Filename output invalid. Group not in Dicom keyword or in regex groups: {kw}"
                    )

        return errors

    @fw_pydicom_config()
    def process_files(self, *args, **kwargs):
        super(DicomFileProfile, self).process_files(*args, **kwargs)

    def _validate_replace_with(self, field, errors):
        with tempfile.TemporaryFile() as fp:
            fp.is_little_endian = True
            fp.is_implicit_VR = False
            try:
                vr = pydicom.datadict.dictionary_VR(field.fieldname)
                de = pydicom.DataElement(field.fieldname, vr, field.value)
                writer_function, writer_param = writers[vr]
                if vr in text_VRs or vr in ("PN", "SQ"):
                    writer_function(fp, de)
                else:
                    # Many numeric types use the same writer but with
                    # numeric format parameter
                    if writer_param is not None:
                        writer_function(fp, de, writer_param)
                    else:
                        writer_function(fp, de)
            except Exception:
                errors.append(
                    f"Incorrect value type for Dicom element {field.fieldname} (VR={vr}): {type(field.value).__name__}"
                )

    def _validate_hash(self, field, errors):
        """Validate that VR of data element is string compatible"""
        vr = pydicom.datadict.dictionary_VR(field.fieldname)
        if vr in [
            "AT",
            "FL",
            "FD",
            "OB",
            "OW",
            "OF",
            "SL",
            "SQ",
            "SS",
            "UL",
            "UN",
            "US",
            "OB/OW",
            "OW/OB",
            "OB or OW",
            "OW or OB",
        ]:
            errors.append(
                f"{field.fieldname} cannot be hashed - VR not compatible ({vr})"
            )

    def validate(self, enhanced=False):
        """Validate the profile, returning any errors.

        Args:
            enhanced (bool): If True, test profile execution on a set of test files

        Returns:
            list(str): A list of error messages, or an empty list
        """

        errors = super(DicomFileProfile, self).validate()

        if self.filenames:
            self.validate_filenames(errors)

        for field in self.fields:
            if field.fieldname.startswith(self.filename_field_prefix) or getattr(
                field, "_is_regex"
            ):
                continue
            # do not validate if name is a tag or nested
            if (
                DICOM_TAG_HEX_RE.match(field.fieldname)
                or DICOM_TAG_TUPLE_RE.match(field.fieldname)
                or DICOM_NESTED_RE.match(field.fieldname)
            ):
                continue
            lc_field = field.fieldname.lower()
            if lc_field not in self.lc_kw_dict:
                errors.append("Not in DICOM keyword list: " + field.fieldname)
            # case difference; correct to proper DICOM spelling
            elif field.fieldname != self.lc_kw_dict[lc_field]:
                field.fieldname = DicomTagStr(self.lc_kw_dict[lc_field])

            # validate action specifics
            if field.fieldname.lower() in self.lc_kw_dict:
                if field.key == "replace-with":
                    self._validate_replace_with(field, errors)
                if field.key == "hash":
                    self._validate_hash(field, errors)

        if enhanced:
            # Test deid profile on test Dicom files
            test_files = get_testdata_files("*.dcm")
            for test_file in test_files:
                dirname, basename = os.path.split(test_file)
                basename = six.u(basename)  # fs requires unicode
                if basename == "1.3.6.1.4.1.5962.1.1.0.0.0.977067309.6001.0.OT.dcm":
                    continue  # this test file seems to be corrupted
                test_fs = OSFS(dirname)
                try:
                    self.process_files(test_fs, test_fs, [basename])
                except Exception:
                    log.error(
                        "Failed to run profile on pydicom test file %s",
                        basename,
                        exc_info=True,
                    )
                    raise

        return errors
