from album import Album
from enum import Enum

class AgentState(Enum):
    COMPLETED = 1
    LOOKING_FOR_EXCHANGE = 2
    LOOKING_FOR_SHEETS = 3

class Agent:
    def __init__(self):
        self.__friends = []
        self.__album = Album()
        self.__state = AgentState.LOOKING_FOR_SHEETS
    
    def add_friend(self, friend):
        self.__friends.append(friend)
    
    def save_sheet(self, sheet):
        if not self.__album.is_full():
            self.__album.add_sheet(sheet)
    
    def get_missing_sheets(self):
        pass

    def check_surplus_list(self, surplus):
        pass

    def exchange_sheets(self, new_sheets, own_sheets):
        pass
    