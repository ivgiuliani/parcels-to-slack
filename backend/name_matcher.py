class NameMatcher:
    VALID_CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ 1234567890".lower()

    def __init__(self, name_dict):
        self.__name_list=name_dict

    def print(self):
        for index, name in enumerate(self.__name_list):
            print("{} - {}".format(index, name))

    def sanitise(self, text):
        return "".join([char for char in text if char in self.VALID_CHARS])

    def find_name_in_blob_of_text(self, blob_of_text):
        lines = [" ".join(line.split()) for line in blob_of_text.lower().splitlines() if line]
        sanitised_lines = [self.sanitise(line) for line in lines]
        tokens = set(" ".join(sanitised_lines).split(" "))

        for name in self.__name_list:
            name_set = set(self.sanitise(name).split())
            if tokens & name_set:
                return name

        raise RuntimeError("No name found!")
