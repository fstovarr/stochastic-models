from album import Album
from enum import Enum

class AgentState(Enum):
    """Enum that represents the possible states of the agent
    """
    COMPLETED = 1
    LOOKING_FOR_SHEETS = 2

class Agent():
    """Model of the agent who wants to fill its album through simulation
    """

    def __init__(self, album_sheets=700, idx=0):
        """Class constructor

        Args:
            album_sheets (int, optional): Album total sheets. Defaults to 700.
            idx (int, optional): Agent Identifier. Defaults to 0.
        """
        self.__friends = []
        self.__album = Album(size=album_sheets)
        self.__state = AgentState.LOOKING_FOR_SHEETS
        self.idx = idx
        self.__purchased_sheets = 0

    def look_for_exchange(self):
        """Look for the best option to do a exchange based on maximum profit of itself
        """
        if not len(self.__friends) > 0 or not self.has_surplus():
            return
        missing = self.get_missing_sheets()
        max_id = -1
        max_list_1 = []
        max_list_2 = []
        tmp = []
        tmp_2 = []

        for (i, friend) in enumerate(self.__friends):
            if not friend.has_surplus():
                continue
            
            tmp = friend.check_missing_list(missing)
            if len(tmp) <= len(max_list_1):
                continue
            
            tmp_2 = self.check_missing_list(friend.get_missing_sheets())
            if len(tmp_2) <= len(max_list_2):
                continue
            
            max_list_1 = tmp
            max_list_2 = tmp_2
            max_id = i
            
            if len(max_list_1) == len(missing):
                break
        return (max_list_1, max_list_2, self.__friends[max_id])

    def get_album_size(self):
        return self.__album.size

    def do_exchange(self, list1, list2, friend):
        """To do a exchange with an agent

        Args:
            list1 (list): List of its own sheets
            list2 (list): List of the friend's sheets 
            friend (int): Id of the friend in the list
        """
        friend.exchange_sheets(list2, list1)
        self.exchange_sheets(list1, list2)
    
    def add_friend(self, friend):
        self.__friends.append(friend)
    
    def save_sheet(self, sheet):
        if not self.__album.is_full():
            self.__purchased_sheets += 1
            self.__album.add_sheet(sheet)
            self.__update_state()
    
    def get_missing_sheets(self):
        return self.__album.get_missing()

    def get_state(self):
        return self.__state

    def get_surplus(self):
        return self.__album.get_surplus()

    def get_metrics(self):
        return "{},{},{},{}".format(self.idx, len(self.__friends), self.__album.get_surplus_count(), self.__purchased_sheets)

    def check_missing_list(self, missing):
        """Check weather the agent needs some sheet of a list of possible sheetts

        Args:
            missing (list): List of possible missing sheets

        Returns:
            list: List of the missing sheets
        """
        surplus = self.__album.get_surplus()
        limit = min(len(surplus), len(missing))
        
        m_id = 0
        s_id = 0
        result = []

        while len(result) < limit and m_id < len(missing) and s_id < len(surplus):
            if missing[m_id][0] < surplus[s_id][0]:
                m_id += 1
            elif surplus[s_id][0] < missing[m_id][0]:
                s_id += 1
            else:
                result.append(surplus[s_id][0])
                s_id += 1
                m_id += 1

        return result

    def exchange_sheets(self, new_sheets, own_sheets):
        for i in new_sheets:
            self.__album.add_sheet(i)

        for i in own_sheets:
            self.__album.remove_surplus(i)
        self.__update_state()

    def has_surplus(self):
        return self.__album.has_surplus()
    
    def __update_state(self):
        self.__state = AgentState.COMPLETED if self.__album.is_full() else AgentState.LOOKING_FOR_SHEETS

    def __str__(self):
        return "\n\nAgent: {}".format(self.idx) + "\nAlbum:\n" + str(self.__album) + "\nState:" + str(self.__state)
