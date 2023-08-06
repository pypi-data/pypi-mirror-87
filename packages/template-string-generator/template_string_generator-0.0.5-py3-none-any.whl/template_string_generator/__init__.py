"""
Wrapper for the app module to expose it as a package
"""

from typing import Dict

from .app import StringGenerator


def get_default_replacements() -> Dict[str, int]:
    """
    Wrapper of StringGenerator.default_place_holders()

    :return: The replacement for the default wildcards
    :rtype: A dictionary with str keys and list as values
    """
    return StringGenerator.default_place_holders()


def create_strings(template: str, replacements: Dict[str, int] = None) -> list:
    """
    Wrapper of string_generator.create_strings()

    This method will create a new instance of StringGenerator for
    each interaction

    :param template: String containing wildcards to be used as
    template for all combinations
    :type template: str
    :param replacements: Dic containing the placeholders contained in the
    template and their respective list of possible values defaults
    to StringGenerator.default_place_holders()
    :type replacements: A dictionary with str keys and list as values
    :return: A list of string with each string combination
    :rtype list of strings
    """
    string_generator = StringGenerator(template, replacements)
    return string_generator.create_strings()
