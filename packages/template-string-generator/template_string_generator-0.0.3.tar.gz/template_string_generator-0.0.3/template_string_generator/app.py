import string


class StringGenerator:
    def __init__(self, string_template: str, placeholders: dict = None):
        self.template = string_template
        self.placeholders = placeholders if placeholders else self.default_place_holders()

        self.previous_replace = {}

    @staticmethod
    def default_place_holders() -> dict:
        return {
            "%A": list(string.ascii_uppercase),
            "%a": list(string.ascii_lowercase),
            "%n": list(string.digits),
            "%s": ['A', 'B'] + list(string.digits)
        }

    def count_list_appearances_in_string(self) -> int:
        appearances = 0

        for key in self.placeholders.keys():
            appearances += self.template.count(key)

        return appearances

    def combinations_from_template(self) -> int:
        total_combinations = 0
        for current_key in self.placeholders.keys():
            times_found = self.template.count(current_key)
            if times_found:
                for x in range(times_found):
                    if not total_combinations:
                        total_combinations = len(
                            self.placeholders[current_key]
                        )
                        continue

                    total_combinations = total_combinations * len(
                        self.placeholders[current_key]
                    )

        return total_combinations

    def find_next_placeholder(self, haystack: str) -> [str, int]:
        next_placeholder = ''
        last_found = -1

        for key in self.placeholders.keys():
            current_match = haystack.rfind(key)
            if last_found < 0 or current_match > last_found \
                    and current_match != -1:
                next_placeholder = key
                last_found = current_match

        return next_placeholder, last_found

    def form_string(self):
        new_string = self.template

        # Initially set to True as the function will always increase the
        # iteration by one
        increment = True
        for x in range(self.count_list_appearances_in_string()):
            next_key, next_key_index = self.find_next_placeholder(new_string)
            key_options = self.placeholders[next_key]
            previous_index = self.previous_replace.get(next_key_index) \
                if self.previous_replace.get(next_key_index) \
                else 0

            # TODO when iterating for th first time the previous_index is
            #  set to 0 as it doesnt yet exists but it's later increased
            #  by one skipping the first value and pushing it back to the end
            new_index = previous_index + 1 if increment else previous_index
            increment = False  # Increment done
            if new_index >= len(key_options):
                new_index = 0
                increment = True  # Carry over to the next iteration

            # Preserve the state for the next string
            self.previous_replace[next_key_index] = new_index

            new_string = key_options[new_index].join(
                new_string.rsplit(next_key, 1)
            )

        return new_string

    def create_strings(self) -> list:
        items = []
        i = 0
        while i < self.combinations_from_template():
            items.append(self.form_string())

            i += 1

        return items
