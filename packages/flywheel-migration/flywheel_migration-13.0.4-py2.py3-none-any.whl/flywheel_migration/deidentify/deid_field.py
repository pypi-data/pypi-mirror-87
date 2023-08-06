"""Represents action to take in order to de-id a single field"""
import copy
import logging
import re

from abc import ABCMeta, abstractmethod
from datetime import datetime, timedelta

from .. import util

log = logging.getLogger(__name__)
# Example: +0000 (Dicom), +00:00 (datetime)
RE_TIMEZONES = [re.compile(r"(.+)([-+]\d{4})$"), re.compile(r"(.+)([-+]\d{2}:\d{2})$")]
RE_OUTPUT = re.compile(r"\{([^}]+)\}")


class DeIdFieldMixin:
    """Mixin base class to add functionalities to DeIdField based on profile used"""

    __metaclass__ = ABCMeta
    flavor = None  # to be used as prefix for the DeIdField subclasses name


class DeIdField:
    """Abstract class that represents action to take to de-identify a single field"""

    __metaclass__ = ABCMeta

    # NOTE: If you derive from this class, set a unique key for the factory method to use
    key = None
    __hash_cache = {}

    def __init__(
        self,
        fieldname,
        is_regex=False,
        dry=False,
    ):
        self.fieldname = fieldname
        self._is_regex = is_regex
        self._dry = dry  # if True, does not modify record

    @property
    def is_dry(self):
        return self._dry

    @property
    def is_regex(self):
        return self._is_regex

    def list_fieldname(self, record):
        """Return a list of fieldnames for record.

        By default returns [self.fieldname]. Can be overwritten by certain
        subclasses of FieldEnhancerBaseMixin to returns a range of record attributes
        (e.g. when field uses regex, or range definition).
        """
        return [self.fieldname]

    @classmethod
    def factory(cls, config, dry=False, mixin=None):
        """Create a new DeIdField instance for the given config.

        Arguments:
            config (dict): The field configuration
            dry (bool): Is set to true, set the field as dry, i.e. a field that does not
                modify the record.
            mixin (DeIdFieldMixin): Optional subclass of DeIdFieldMixin to be
                inherited by the DeIdField subclass to make the field profile specific.
        """
        result = None
        is_regex = False
        name = config.get("name")
        regex = config.get("regex")
        if name and regex:
            raise ValueError(
                f"Field can not have name and regex defined. " f"Both found in {config}"
            )
        if name:
            fieldname = name
        elif regex:
            fieldname = regex
            is_regex = True
        else:
            raise ValueError(
                f"Field element must defined either name or regex. "
                f"none found in {config}"
            )

        for subclass in cls.__subclasses__():
            for key in config.keys():
                if subclass.key == key:
                    if mixin:  # Attach DeIdFieldMixin if defined.
                        subclass_name = f"{mixin.flavor}{cls.__name__}"
                        subclass = type(subclass_name, (mixin, subclass), {})
                    try:
                        result = subclass(
                            fieldname,
                            is_regex=is_regex,
                            dry=dry,
                        )
                    except TypeError:
                        raise TypeError
                    break
            if result:
                break

        if not result:
            raise ValueError("Unknown de-identify action")

        result.load_config(config)
        return result

    def to_config(self):
        """Convert to configuration dictionary"""
        result = {}
        if self._is_regex:
            result["regex"] = str(self.fieldname)
        else:
            result["name"] = str(self.fieldname)
        self.local_to_config(result)
        return result

    def local_to_config(self, config):
        """Convert rule specific settings to configuration dictionary"""
        # Most fields just store True in the key field
        config[self.key] = True

    def load_config(self, config):
        """Load rule specific settings from configuration dictionary"""

    def deidentify(self, profile, state, record):
        """Perform the update - default implementation is to do a replace"""
        if not self.is_dry:
            new_value = self.get_value(profile, state, record)
            if new_value is not None:
                profile.replace_field(state, record, self.fieldname, new_value)

    @abstractmethod
    def get_value(self, profile, state, record):
        """Get the transformed value, given profile state and record"""

    @classmethod
    def _hash(cls, profile, value, output_format="hex"):
        """Hash a value according to profile rules"""
        # Memoize hash results
        salt = profile.hash_salt
        hash_key = (salt, value, output_format)
        result = cls.__hash_cache.get(hash_key)
        if not result:
            result = util.hash_value(
                value,
                algorithm=profile.hash_algorithm,
                salt=salt,
                output_format=output_format,
            )
            cls.__hash_cache[hash_key] = result
        return result

    def _perform_date_inc(self, profile, state, record, fmt, timezone=False):
        new_value = None
        original = profile.read_field(state, record, self.fieldname)
        if original:
            suffix = ""

            # NOTE: Parsing optional timezone doesn't seem to be universally supported
            # Since we don't actually need the value, just strip and reapply if present
            if timezone:
                for tz_reg in RE_TIMEZONES:
                    match = tz_reg.match(original)
                    if match:
                        original = match.group(1)
                        suffix = match.group(2)
                        break
            # Add fractional seconds to datetime string if they are not present
            if fmt.endswith(".%f") and "." not in original:
                original = original + ".0"
            # TODO: Should we capture ValueError here?
            try:
                orig_date = datetime.strptime(original, fmt)
                new_date = orig_date + timedelta(days=profile.date_increment)
                new_value = new_date.strftime(fmt) + suffix
            except ValueError as err:
                log.error("NO ACTION WAS TAKEN! Unable to parse date field: %s", err)

        return new_value


class DeIdIdentityField(DeIdField):
    """Action to do nothing on a field"""

    key = "identity"

    def deidentify(self, profile, state, record):
        """Do nothing

        This is to support identity action. As of today use to handle reference to record attributes
        in filename.output on which no action is performed (i.e. not defined in `groups` or `fields`).
        """

    def get_value(self, profile, state, record):
        return profile.read_field(state, record, self.fieldname)


class DeIdRemoveField(DeIdField):
    """Action to remove a field from the record"""

    key = "remove"

    def deidentify(self, profile, state, record):
        profile.remove_field(state, record, self.fieldname)

    def get_value(self, profile, state, record):
        return None


class DeIdReplaceField(DeIdField):
    """Action to replace a field from the record"""

    key = "replace-with"

    def __init__(self, fieldname, **kwargs):
        super(DeIdReplaceField, self).__init__(fieldname, **kwargs)
        self.value = None

    def get_value(self, profile, state, record):
        return self.value

    def local_to_config(self, config):
        config["replace-with"] = self.value

    def load_config(self, config):
        self.value = config["replace-with"]


class DeIdHashField(DeIdField):
    """Action to replace a field with it's hashed value"""

    key = "hash"

    def get_value(self, profile, state, record):
        new_value = None
        original = profile.read_field(state, record, self.fieldname)
        if original:
            new_value = self._hash(profile, original)

            # Respect character limit, if applicable
            if profile.hash_digits > 0:
                new_value = new_value[: profile.hash_digits]

        return new_value


class DeIdHashUIDField(DeIdField):
    """Action to replace a uid field with it's hashed value"""

    key = "hashuid"

    def get_value(self, profile, state, record):
        new_value = None

        original = profile.read_field(state, record, self.fieldname)
        if original:
            orig_parts = original.split(".")

            # Determine how many fields are required
            if not profile.uid_numeric_name:
                required = profile.uid_prefix_fields + profile.uid_suffix_fields
                if required > len(orig_parts):
                    raise ValueError("UID is too short to be hashed")

            # Get the digest
            digest = self._hash(profile, original, output_format="dec")
            result_parts = []

            # Build the new UID string with prefix
            if profile.uid_prefix_fields > 0:
                if profile.uid_numeric_name:
                    if (
                        not len(profile.uid_numeric_name.split("."))
                        == profile.uid_prefix_fields
                    ):
                        raise ValueError(
                            f"Registered OID numeric name must have exactly {profile.uid_prefix_fields} "
                            f"fields"
                        )
                    result_parts += profile.uid_numeric_name.split(".")
                else:
                    result_parts += orig_parts[: profile.uid_prefix_fields]

            # Parts taken from hash string
            idx = 0
            for seg in profile.uid_hash_fields:
                # Workaround for avoiding E203:
                #   https://github.com/PyCQA/pycodestyle/issues/373#issuecomment-398693703
                to_index = idx + seg
                result_parts.append(digest[idx:to_index])
                idx += seg

            # And suffix
            if profile.uid_suffix_fields > 0:
                suffix = []
                # Keep no more than the number of digits specified
                # i.e. strip any dates
                # Workaround for avoiding E203:
                #   https://github.com/PyCQA/pycodestyle/issues/373#issuecomment-398693703
                from_index = -profile.uid_suffix_fields
                for part in orig_parts[from_index:]:
                    if len(part) > profile.uid_max_suffix_digits:
                        # Workaround for avoiding E203:
                        #   https://github.com/PyCQA/pycodestyle/issues/373#issuecomment-398693703
                        from_index_max_suffix_digits = -profile.uid_max_suffix_digits
                        part = part[from_index_max_suffix_digits:]
                    suffix.append(part)
                result_parts += suffix

            new_value = ".".join(result_parts)

        return new_value


class DeIdIncrementDateField(DeIdField):
    """Action to replace a field with it's incremented date"""

    key = "increment-date"

    def __init__(self, fieldname, **kwargs):
        super(DeIdIncrementDateField, self).__init__(fieldname, **kwargs)
        self.date_format = None

    def load_config(self, config):
        if "date-format" in config:
            self.date_format = config.get("date-format")

    def get_value(self, profile, state, record):
        date_format = self.date_format if self.date_format else profile.date_format
        return self._perform_date_inc(profile, state, record, date_format)

    def local_to_config(self, config):
        super(DeIdIncrementDateField, self).local_to_config(config)
        if self.date_format:
            config["date-format"] = self.date_format


class DeIdIncrementDateTimeField(DeIdField):
    """Action to replace a field with it's incremented date"""

    key = "increment-datetime"

    def __init__(self, fieldname, **kwargs):
        super(DeIdIncrementDateTimeField, self).__init__(fieldname, **kwargs)
        self.datetime_format = None

    def load_config(self, config):
        if "datetime-format" in config:
            self.datetime_format = config.get("datetime-format")

    def get_value(self, profile, state, record):
        datetime_format = (
            self.datetime_format if self.datetime_format else profile.datetime_format
        )
        return self._perform_date_inc(
            profile, state, record, datetime_format, timezone=True
        )

    def local_to_config(self, config):
        super(DeIdIncrementDateTimeField, self).local_to_config(config)
        if self.datetime_format:
            config["datetime-format"] = self.datetime_format


class DeIdRegexSubField(DeIdField):
    """Action to edit a string matching a regex with capture groups"""

    key = "regex-sub"

    def __init__(self, fieldname, **kwargs):
        super(DeIdRegexSubField, self).__init__(fieldname, **kwargs)
        self.list_members = list()
        self.input_regex = None
        self.output_regex = re.compile(r"\{([^}]+)\}")
        self.output = None

    @staticmethod
    def _patch_profile(profile, read_value):
        """
        Create a copy of the FileProfile, replacing read_field with a function
            that returns read_value
        """

        def _patched_read_field(*args):  # pylint: disable=unused-argument
            return read_value

        new_profile = copy.deepcopy(profile)
        new_profile.read_field = _patched_read_field
        return new_profile

    def load_config(self, config):
        for item in config.get(self.key):
            self.list_members.append(DeIdRegexSubListItem(item))

    def local_to_config(self, config):
        config[self.key] = [member.to_config() for member in self.list_members]
        return config

    def get_value(self, profile, state, record):
        current = profile.read_field(state, record, self.fieldname)
        match = False
        for member in self.list_members:
            if member.regex_matches_field_value(current):
                match = True
                break
        if match is False:
            raise ValueError(
                f"Field {self.fieldname} value {current} does not match any of the input-regex values"
            )
        out_vars = self.output_regex.findall(member.output)
        val_dict = dict()
        for var_name in out_vars:
            match = member.input_regex.match(current)
            match_val = match.groupdict().get(var_name)
            if member.group_dict.get(var_name):
                group_field = member.group_dict.get(var_name)
                if match_val is not None:
                    patch_profile = self._patch_profile(profile, match_val)
                    var_value = group_field.get_value(patch_profile, state, record)
                else:
                    if (
                        profile.field_map.get(var_name)
                        and group_field.key != "identity"
                    ):
                        warn_str = (
                            f"Field {var_name} is defined in the profile AND in"
                            f" a {self.fieldname} group. Group action will be"
                            " applied after profile action."
                        )
                        log.warning(warn_str)
                    var_value = group_field.get_value(profile, state, record)
            elif match_val is not None:
                var_value = match_val
            else:
                err_str = (
                    f"Action for {var_name} is not defined in groups for "
                    f"{member.input_regex}. Please modify "
                    f"profile for {self.fieldname}"
                )
                raise ValueError(err_str)

            if var_value is None:
                var_value = ""
            val_dict[var_name] = var_value

        return member.format_output(val_dict)


class DeIdRegexSubListItem:
    """Class for representing a list item within DeIdRegexSubField"""

    output_dot_replace_char = "___"

    def __init__(self, config):
        self.input_regex = re.compile(config.get("input-regex"))
        self.group_dict = dict()
        self._preprocess_output(config.get("output"))
        self.output_vars = RE_OUTPUT.findall(self.output)
        self._load_group_config(config.get("groups", []))

    def _preprocess_output(self, output):
        """Create mapping to allow for referencing variable with '.' in output"""
        self.output = output

        # output referencing dotty key (e.g. '{label}_{subject.label}') cannot be
        # formatted readily because `.` is an object attribute delimiter.
        output_map = {}
        proc_output = output
        for var in re.findall(r"\{([^}]+)\}", output):
            if "." in var:
                xmap = var.replace(".", self.output_dot_replace_char)
                output_map[var] = xmap
                proc_output = proc_output.replace(var, xmap)
            else:
                output_map[var] = var
        self._output_map = output_map
        self._proc_output = proc_output

    def format_output(self, val_dict):
        """Format output according to output_map"""
        val_dict_mapped = {self._output_map[k]: v for k, v in val_dict.items()}
        return self._proc_output.format(**val_dict_mapped)

    def _load_group_config(self, group_list):
        """Load the configuration for the groups"""
        for group_config in group_list:
            group_member_field = DeIdField.factory(group_config, dry=True)
            self.group_dict[group_member_field.fieldname] = group_member_field

    def regex_matches_field_value(self, value):
        """return True if the value matches the regex, else False"""
        return bool(self.input_regex.match(value))

    def to_config(self):
        """Convert to configuration dictionary"""
        config_dict = dict()
        config_dict["input-regex"] = self.input_regex
        config_dict["output"] = self.output
        config_dict["groups"] = [
            group.to_config() for group in self.group_dict.values()
        ]
        return config_dict

    def is_capture_group(self, var_name):
        """
        Return True if the varname matches a named capture group in
            self.input_regex
        """
        return bool(self.input_regex.groupindex.get(var_name))

    def var_name_is_valid(self, var_name):
        """
        Return True if the varname is a capture group or is defined in self.group_dict,
        False otherwise.
        """
        valid = False
        if self.is_capture_group(var_name):
            valid = True
        if self.group_dict.get(var_name):
            valid = True

        return valid

    def get_invalid_output_vars(self):
        """Return a list of invalid output_vars"""
        invalid_vars = [
            var for var in self.output_vars if not self.var_name_is_valid(var)
        ]
        return invalid_vars
