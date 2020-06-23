from album import Album
from enum import Enum

class AgentState(Enum):
    COMPLETED = 1
    LOOKING_FOR_EXCHANGE = 2
    LOOKING_FOR_SHEETS = 3

class Agent:
    def __init__(self, album_sheets=700):
        self.__friends = []
        self.__album = Album(size=album_sheets)
        self.__state = AgentState.LOOKING_FOR_SHEETS
    
    def add_friend(self, friend):
        self.__friends.append(friend)
    
    def save_sheet(self, sheet):
        if not self.__album.is_full():
            self.__album.add_sheet(sheet)
    
    def get_missing_sheets(self):
        return self.__album.get_missing()

    def check_surplus_list(self, surplus):
        missing = self.__album.get_missing()
        if len(surplus) == 0 or len(missing) == 0:
            return []
        
        m_id = 0
        s_id = 0
        result = []
        while m_id < self.__album.size and s_id < self.__album.size:
            if missing[m_id] < surplus[s_id]:
                m_id += 1
            elif surplus[s_id] < missing[m_id]:
                s_id += 1
            else
                result.append(s_id)
                s_id += 1
                m_id += 1

        return result

    def exchange_sheets(self, new_sheets, own_sheets):
        for i in new_sheets:
            self.__album.add_sheet(i)
        for i in own_sheets:
            self.__album.remove_surplus(i)
    