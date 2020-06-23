from random_generator import RandomGenerator

class Environment():
    def __init__(self, album_sheets=700):
        self.__rg = RandomGenerator(seed=0)
        self.__sheets_count = album_sheets

    def get_sheet(self):
        return self.__rg.get_int(0, self.__sheets_count)

    def get_sheets_count(self):
        return self.__sheets_count

