class NameMatcher:
    def __init__(self, name_dict):
        self.__name_list=name_dict

    def print(self):
        for index, name in enumerate(self.__name_list):
            print("{} - {}".format(index, name))

    def find_name_in_blob_of_text(self, blob_of_text):

        tokens = set(" ".join([" ".join(line.split()) for line in blob_of_text.lower().splitlines() if line]).split(" "))

        name_found = None
        for name in self.__name_list:
            name_set = set(name.split())
            if tokens & name_set:
                return name

        if name_found is None:
            raise RuntimeError("No name found!")


if __name__ == "__main__":
    names = {'dario':'id1', 'bob':'id2'}
    nm = NameMatcher(names)
    nm.print()

    name = nm.find_name_in_blob_of_text("asdasd dario asdas dd sda")

    print("Found {}".format(name))
