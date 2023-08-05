""" A "model locator" in Rho ML is the combination of the model name the model
    version, and a delimiter between them.

    This is important for storage and retrieval of models as they evolve over
    time. Using the default settings is highly recommended but each component is
    configurable.

    By default:

    #. Model names can be any alphanumeric character
    #. Delimeter is "_" (the underscore character)
    #. Model versions must adhere to [semver versioning](https://semver.org/)

    e.g.::

        MyModel_0.1.0

    Notes:

    #. The most commonly used member of this module is :class:`~.Version`,
       which is passed to any :class:`~rho_ml.rho_model.RhoModel` at
       instantiation.
    #. In most cases users won't need to interact directly with the other
       functions in this module.  One notable counterexample is if a custom
       :class:`~rho_ml.serialization.PipelineStorageConfig` is needed.

"""
import logging
import re
from typing import List, Tuple, Union, Optional
import attr

logger = logging.getLogger(__name__)

DEFAULT_MODEL_NAME_PATTERN = r"(.*)"
DEFAULT_DELIMITER_PATTERN = r"\_"
DEFAULT_VERSION_PATTERN = r"([\d\*]+\.[\d\*]+\.[\d\*]+.*)"


def generate_model_locator(
        model_name: str,
        model_version: str,
        delimiter: str = "_",
        model_name_pattern: Union[str, None] = DEFAULT_MODEL_NAME_PATTERN,
        delimiter_pattern: str = DEFAULT_DELIMITER_PATTERN,
        version_pattern: str = DEFAULT_VERSION_PATTERN) -> str:
    """ Combine the model name and version into name_version format, which
        by default uses "_" as the delimiter.

        Validates model name and version against the provided (or default)
        patterns.
    """
    # Validate model name against pattern
    if not re.compile(model_name_pattern).match(model_name):
        raise ValueError(f"{model_name} does not conform to "
                         f"model name pattern {model_name_pattern}")

    # Validate delimiter against pattern
    if not re.compile(delimiter_pattern).match(delimiter):
        raise ValueError(f"{delimiter} does not conform to "
                         f"delimiter pattern {delimiter_pattern}")

    # Validate model version against pattern
    if not re.compile(version_pattern).match(model_version):
        raise ValueError(f"{model_name} does not conform to "
                         f"model version pattern {version_pattern}")

    # Combine and return if all good
    return model_name + delimiter + model_version


def validate_model_version(
        model_version: str,
        version_pattern: str = DEFAULT_VERSION_PATTERN) -> str:
    """ Model version must conform to semver but can include wildcards.
    """
    pattern = re.compile(r"^" + version_pattern)
    if not pattern.match(model_version):
        raise ValueError("Invalid model_version format ({0}). Must conform "
                         "to semver with wildcards allowed. "
                         "e.g. 1.1.1, 1.*.*".format(model_version))
    return model_version


def split_model_locator(
        model_locator: str,
        model_name_pattern: Union[str, None] = DEFAULT_MODEL_NAME_PATTERN,
        delimiter_pattern: str = DEFAULT_DELIMITER_PATTERN,
        version_pattern: str = DEFAULT_VERSION_PATTERN,
        exclude_paths: bool = False
) -> Tuple[Union[str, None], Union[str, None]]:
    """ Given a full model locator including it's name and version (Model_0.1.0)
        return the model name and version as separate entities based on
        provided patterns (e.g. ('Model', '0.1.0')).

        Allows model_name_pattern to be None, in which case this expects the
        `model_locator` to instead be the version string along (e.g. 0.1.0)
        and will return (None, '0.1.0')

        exclude_paths allows you to pass the model_locator as a full path
        to the object. This is off by default because a model name can be
        "anything" according to the default model name pattern and this operates
        with the basic rule that the model_locator will exist after the final
        forward slash ('/')
    """
    version_search = re.compile(version_pattern)
    version_group = version_search.search(model_locator)
    if version_group is None:
        this_version = None
    else:
        this_version = version_group.group(1)

    if model_name_pattern is None:
        this_model_name = None
    else:
        model_name_search = re.compile(model_name_pattern + delimiter_pattern)
        model_name_group = model_name_search.search(model_locator)
        if model_name_group is None:
            this_model_name = None
        else:
            this_model_name = model_name_group.group(1)

    if exclude_paths:
        this_model_name = this_model_name.split('/')[-1]

    return this_model_name, this_version


def find_highest_compatible_version(
        search_version: str,
        search_list: List[str],
        model_name_pattern: Union[str, None] = DEFAULT_MODEL_NAME_PATTERN,
        delimiter_pattern: str = DEFAULT_DELIMITER_PATTERN,
        version_pattern: str = DEFAULT_VERSION_PATTERN) -> str:
    """ Return the model locator or version of the highest compatible version.

        If search_list is a list of model locators (['model_0.1.1']) it returns
        the full locator of the highest version that matches `search_version`.

        If search_list is a list of versions only (['0.1.1']), then it does
        the same search against `search_version` and returns just version number

        The default model locator pattern is a combination of the default
        model name pattern (any valid characters ending in "_" as the delimiter
        for the beginning of the version pattern) and the default version
        pattern (semver compatible 0.0.0*).

        That is::

            {{model name}}_{{model version}}

        e.g.::

            MyModel_0.1.0
            my_model_0.1.0
            prefix/mymodel_0.1.0

        If a different convention is followed, you can update the default
        model_name_pattern and version_pattern. Note: any custom search patterns
        must still adhere to some baked in assumptions

        #. The model name pattern must have a single capture group OR be
           None, which will result in this assuming it's only searching
           against a version pattern.
        #. The version pattern needs to follow semver, which is what the
           default pattern provides, so it's not recommended to change and
           also requires to have exactly 1 capture group.

        Args:
            search_version (string): The version to search. This can include
                wildcards. E.g. "1.0.0", "2.*.*", "1.1.*"
            search_list (list): List of full model locators with model name and
                version, e.g. `['model_name_0.0.0', 'model_name_0.1.0']`
                or a list of just version numbers, e.g. `['0.0.0', '0.1.0']`
            model_name_pattern (r string): Regex pattern describing any name
                that may be prepended to the search version. Pass as None
                to exclude a model name pattern (e.g. if your
                search_list is a list of only version nums
                ['0.1.1', '0.1.2']). NOTE: This pattern must currently consist
                of exactly one regex group.
            delimiter_pattern (r string): Regex pattern describing delimiter
                Not recommended to modify this pattern.
            version_pattern (r string): Regex pattern describing version
                numbers. NOT recommended to modify this pattern, as the logic
                assumes semver, which is default version pattern provided.
        Returns:
            string: string with major, minor, patch of highest
                compatible version found in available keys based on the
                search version. e.g. "0.1.0"
                e.g. if search version is "0.1.*" & available keys includes
                ['my_name_0.1.1', 'my_name_1.0.0', 'my_name_0.1.5']
                this will return my_name_0.1.5
    """
    search_version = validate_model_version(search_version)

    def _run_search(search_list, v_index, version_elements) -> Optional[str]:
        """ Loop through all keys to identify highest compatible.
            This is called sequentially for major, minor, patch.

            Args:
                search_list (list): List of full model locators with name and
                    version, e.g.
                        ['model_name_0.0.0', 'model_name_0.1.0']
                    or a list of just version numbers, e.g.
                        ['0.0.0', '0.1.0']
                v_index (int): The index of the model version to find. 0 is
                    major, 1 is minor, 2 is patch.
                version_elements (list): List of integers representing the
                    indices of version elements that have already been
                    found. The first element is always major, second is
                    minor, third is patch. e.g. [0, 1, 0] == "0.1.0"
            Returns:
                string: string with major, minor, patch of highest
                    compatible version found in available keys based on the
                    search version. e.g. "0.1.0"
        """
        highest_compatible_num = -1  # Haven't found anything yet
        for available_version in search_list:

            model_name, model_version = split_model_locator(
                available_version,
                model_name_pattern=model_name_pattern,
                delimiter_pattern=delimiter_pattern,
                version_pattern=version_pattern)

            if model_version is None:
                continue

            # Skip this available_version if it has a version element
            # > something we've already found. e.g. if we already found
            # major version 1 as the max, and this is major version 0,
            # then it doesn't matter what the value of this_num is because
            # it's already incompatible. This can only ever ben 3 elements
            # when following semver, so hardcode.
            incompatible_previous_version_num = False
            for i in range(len(version_elements)):
                if version_elements[i] is None \
                        or int(model_version.split(".")[i]) \
                        != version_elements[i]:
                    incompatible_previous_version_num = True

            if incompatible_previous_version_num:
                continue

            # We only compare one version num (major/minor/patch) at a time
            this_num = int(model_version.split(".")[v_index])

            # The 'search_num' can include wildcards, which means it
            # can be anything. If it's an int, then this_num must be
            # equal to the search_num.
            search_num = search_version.split(".")[v_index]
            if search_num == "*":
                if this_num > highest_compatible_num:
                    highest_compatible_num = this_num
            else:
                search_num = int(search_num)
                if this_num > highest_compatible_num \
                        and this_num == search_num:
                    highest_compatible_num = this_num

        if highest_compatible_num == -1:
            return None
        return highest_compatible_num

    version_elements = []
    for element_idx in range(3):
        version_elements.append(
            _run_search(search_list, element_idx, version_elements))

    if any(v is None for v in version_elements):
        msg = f"Unable to find compatible version with pattern {search_version}"
        if model_name_pattern is not None:
            msg += f" for model pattern {model_name_pattern}"
        msg += f" from available options: {search_list}"
        logger.warning(msg)
        return None

    highest_version = str(version_elements[0]) + "." \
                      + str(version_elements[1]) \
                      + "." + str(version_elements[2])

    # Return the whole key that has the discovered version.
    for key in search_list:
        model_name, model_version = split_model_locator(
            key,
            model_name_pattern=model_name_pattern,
            delimiter_pattern=delimiter_pattern,
            version_pattern=version_pattern)
        if model_version == highest_version:
            return key

    return None


def find_matching_model_names(
        search_pattern: str,
        available_model_locators: List[str],
        model_name_pattern: str = DEFAULT_MODEL_NAME_PATTERN,
        delimiter_pattern: str = DEFAULT_DELIMITER_PATTERN,
        version_pattern: str = DEFAULT_VERSION_PATTERN) -> List[str]:
    """ Return the model locators with model names that match the search_pattern

        By default, this expects that the model locators follow the convention

            {{model name}}_{{model version}}

        e.g.

            MyModel_0.1.0
            my_model_0.1.0
            prefix/mymodel_0.1.0

        If a different convention is followed, you can update the default
        model_name_pattern. The name pattern must have a single capture group.

        Args:
            search_pattern (string): The model name to look for. This can
                include wildcards. E.g. "MyModel", "*Model", "*"
            available_model_locators (list): List of full model locators with
                name and version, e.g.
                ['model_name_0.0.0', 'model_name_0.1.0', 'MyModel_0.1.0']
            model_name_pattern (r string): Regex pattern describing any name
                that may be prepended to the search version. Pass as None
                to return all keys. NOTE: This pattern must currently consist
                of exactly one regex group.
            delimiter_pattern (r string): Regex pattern describing delimiter
                Not recommended to modify this pattern.
        Returns:
            List[str]: List of model locators that match the search. e.g.
            if search pattern is "\*Model" & available keys includes
            ['my_name_0.1.1', 'my_name_1.0.0', 'MyModel_0.1.5'] this will
            return ['MyModel_0.1.5']
    """

    matched_locators = []
    for locator in available_model_locators:
        model_name, model_version = split_model_locator(
            locator, model_name_pattern, delimiter_pattern, version_pattern)
        if model_name is None:
            continue

        # We allow a star "*" as a wildcard indicator to be consistent with
        # version search.
        if '*' in search_pattern:
            wildcard_pattern = r''
            for char in search_pattern:
                if char == '*':
                    wildcard_pattern += r'.*'
                else:
                    wildcard_pattern += char

            # If the wildcard is NOT the first character, then prepend `^` to
            # search pattern. If wildcard is NOT the last character, then
            # append `$` to search pattern.
            if search_pattern[0] != '*':
                wildcard_pattern = r'^' + wildcard_pattern
            if search_pattern[-1] != '*':
                wildcard_pattern = wildcard_pattern + r'$'

            wildcard_pattern = re.compile(wildcard_pattern)
            if wildcard_pattern.search(model_name):
                matched_locators.append(locator)
        else:  # If no wildcard, do an exact match search
            if model_name == search_pattern:
                matched_locators.append(locator)

    return matched_locators


def convert_empty_str(val: Optional[str]) -> Optional[str]:
    """ Helper method to convert an empty string to None for consistency.
    """
    if not val:
        result = None
    else:
        result = val
    return result


@attr.s(auto_attribs=True, frozen=True)
class Version(object):
    """ Standard version class for RhoModel instances.

    Supports comparison (<, >, ==, etc.) """
    major: int
    minor: int
    patch: int
    label: Optional[str] = attr.ib(converter=convert_empty_str, default=None)

    separator_pattern = r'[\-\_\+\.]'  # Separate version from label
    label_pattern = r'((?P<separator>' \
                    + separator_pattern \
                    + r')(?P<label>.+))?'  # Add grp names to label & separator
    version_pattern = r'(?P<major>\d+)\.(?P<minor>\d+)\.(?P<patch>\d+)' \
                      + label_pattern  # version groups & label groups combinee

    def __str__(self):
        return self.to_string()

    @property
    def label_no_separator(self):
        """ Convenience property to provide the label and exclude the separator

            e.g.
                label == '-alpha.1'
                label_no_separator == 'alpha.1'
        """
        if self.label:
            match = re.match(self.label_pattern, self.label)
            if match is not None:
                return match.group('label')
        return None

    @staticmethod
    def _get_to_increment(to_increment: str):
        """ Accepts a user defined to_increment value and ensures it's valid /
            gets default value.
        """
        if to_increment is None:
            to_increment = 'patch'
        allowable_options = ('major', 'minor', 'patch')
        if to_increment not in allowable_options:
            raise ValueError("Value of `to_increment` must be one of "
                             f"{allowable_options}")
        return to_increment

    @staticmethod
    def _get_new_version(version: 'Version', to_increment: str):
        """ Return the "new" major/minor/patch versions based on a provided
            'to_increment' value.
        """
        # Validate the to_increment val
        to_increment = version._get_to_increment(to_increment)

        if to_increment == 'major':
            major = version.major + 1
            minor = 0
            patch = 0
        elif to_increment == 'minor':
            major = version.major
            minor = version.minor + 1
            patch = 0
        elif to_increment == 'patch':
            major = version.major
            minor = version.minor
            patch = version.patch + 1
        else:
            raise ValueError(
                f"{to_increment} is not a valid version parameter "
                f"to bump!  Should be one of 'major', 'minor', "
                f"or 'patch'")
        return major, minor, patch

    @classmethod
    def increment_version(cls,
                          current_version: 'Version',
                          to_increment: Union[str, None] = None) -> 'Version':
        """ Given an old Version, increment the value of the version's
            `major`, `minor`, or `patch` value based on `to_increment`.

            If `to_increment` is None, defaults to `patch`

            This will always remove any label that may exist on the current
            version.
        """
        major, minor, patch = \
            cls._get_new_version(current_version, to_increment)
        return cls(major=major, minor=minor, patch=patch, label=None)

    @classmethod
    def from_string(cls, val: str):
        """ Create a Version object from a string of the form
            'major.minor.patch-label', where the label is optional.  If it is
            present, it must be separated from the rest of the string by either
            a hyphen (-), underscore (_), plus (+), or period (.).

            semver has specific guidelines around usage of "+_docs_build" and
            "-prerelease" but this level of granularity is not currently
            provided in Rho ML. It is major.minor.patch(optional additional of
            your choosing) where (optional additional) must start with one of the
            valid separators listed above.
        """
        match = re.match(cls.version_pattern, val)

        label = None
        if match.group('separator') is not None \
                and match.group('label') is not None:
            label = match.group('separator') + match.group('label')
        return cls(major=int(match.group('major')),
                   minor=int(match.group('minor')),
                   patch=int(match.group('patch')),
                   label=label)

    def to_string(self) -> str:
        """ Create a version string of the form
        major.min.patch[separator][label]
        where the separator and label are only present if both exist.
        """
        version_str = "{0}.{1}.{2}".format(self.major, self.minor, self.patch)
        if self.label:
            version_str += self.label
        return version_str
