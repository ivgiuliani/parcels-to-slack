class NameMatcher:
    def __init__(self, path="name_list.txt"):
        self.__path = path
        self.refresh()

    def refresh(self):
        with open(self.__path) as f:
            self.__name_list = f.read().lower().splitlines()

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
            raise Exception("No name found!")


if __name__ == "__main__":
    nm = NameMatcher()
    nm.print()
