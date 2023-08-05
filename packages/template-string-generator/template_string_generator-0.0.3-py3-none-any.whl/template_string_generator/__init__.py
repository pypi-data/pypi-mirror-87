from app import StringGenerator


def get_default_replacements():
    return StringGenerator.default_place_holders()


def create_strings(template: str, replacements: dict = None) -> list:
    string_generator = StringGenerator(template, replacements)
    return string_generator.create_strings()
