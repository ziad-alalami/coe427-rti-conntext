from rti_chatter import Chatter
from idl_structs import Group
from uuid import uuid4
from copy import deepcopy
import asyncio
import time
from dotenv import load_dotenv
import os


load_dotenv(override = True)
TIME_SLEEP = float(os.environ.get("TIME_SLEEP", 0.3))

class AppContext:

    def __init__(self):

        self.chatters_dict = {} # USER_ID : CHATTER_OBJECT
        self.groups_dict = {} # GROUP_ID : GROUP_OBJECT
        self.chatters_rcvd_messages = {} # USER_ID : {GROUP_ID: ..., SENDER_ID: ..., MSG: ...}
    
    def create_group(self, group_name: str) -> str:
        """
        Creates a new group in the application.
        By default groups do not have chatters until you add chatters to groups.
        """
        group_id = str(uuid4())
        self.groups_dict[group_id] = Group(group_id = group_id, group_name = group_name, participating_chatters_id = [])
        return group_id
    
    def create_chatter(self, user_name: str) -> str:
        """
        Creates a new chatter in the application.
        """

        user_id = str(uuid4())
        self.chatters_dict[user_id] = Chatter(user_id = user_id, user_name= user_name)
        return user_id
    
    def add_user_to_group(self, user_id: str, group_id: str) -> int:

        """
        Return -2 if user_id does not exist.
        Return -1 if group_id does not exist.
        Return 0 if operation is successful.
        """

        if self.chatters_dict.get(user_id) is None:
            return -2

        if self.groups_dict.get(group_id) is None:
            return -1
        
        self.chatters_dict[user_id].add_group(group_id)
        self.groups_dict[group_id].participating_chatters_id.append(user_id)
        return 0
    
    def remove_group(self, group_id: str) -> int:

        """
        Returns -1 if group_id does not exist.
        Returns 0 if operation is successful.
        """

        if self.groups_dict.get(group_id) is None:
            return -1
        
        del self.groups_dict[group_id]
        return 0
    
    def remove_user(self, user_id: str) -> int:

        """
        Returns -1 if group_id does not exist.
        Returns 0 if operation is successful.
        """

        if self.chatters_dict.get(user_id) is None:
            return -1
        
        del self.chatters_dict[user_id]
        return 0
    
    def send_message(self, group_id: str, user_id: str, msg: str) -> int:
        """
        Returns -2 if user_id does not exist.
        Returns -1 if group_id does not exist.
        Returns 0 if operation is successful.
        """

        if self.chatters_dict.get(user_id) is None:
            return -2

        if self.groups_dict.get(group_id) is None:
            return -1
        
        self.chatters_dict[user_id].send_message(group_id = group_id, msg = msg)
        return 0
    
    def loop_messages(self, user_id: str):
        chatter = self.chatters_dict[user_id]

        while True:
            msgs_dict = chatter.receive_messages()
            self.chatters_rcvd_messages[user_id] = self.chatters_rcvd_messages.get(user_id, []).extend(msgs_dict[user_id])
            time.sleep(TIME_SLEEP)

    def get_user_groups(self, user_id: str):
        """Returns -1 if user_id does not exist.
           Returns [{groups_ids: groups_names}] if successful.
        """

        if self.chatters_dict.get(user_id) is None:
            return -1
        
        return  {group_id: self.groups_dict[group_id].group_name
                     for group_id in self.chatters_dict[user_id].member.participating_groups_id} 
                    
    
    def get_group_users(self, group_id: str):

        """Returns -1 if user_id does not exist.
           Returns [{user_ids: user_names}] if successful.
        """

        if self.groups_dict.get(group_id) is None:
            return -1
        
        return {user_id: self.chatters_dict[user_id].member.user_name
                for user_id in self.groups_dict[group_id].participating_chatters_id} 
                
        

    def get_groups(self):

        return deepcopy(self.groups_dict)
    
    def get_chatters(self):
        
        #SINCE I CANT PICKLE THE DATA READERS AND DATA WRITERS IN THE CHATTER CLASS, I WILL JUST
        #HAND PICK THE OTHER ATTRIBUTES

        return {uid: {
                    "user_id": c.member.user_id,
                    "user_name": c.member.user_name,
                    "groups": list(c.member.participating_groups_id)
                } for uid, c in self.chatters_dict.items()}

    def get_rcvd_messages(self, user_id: str):

        return self.chatters_rcvd_messages.get(user_id, [])    

