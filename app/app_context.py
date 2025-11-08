"""
Application Context Module for DDS Chat System

This module provides the main application context for the DDS chat system,
managing the lifecycle and interactions of chatters and groups. It serves as
the central coordinator for:
- User (Chatter) management
- Group management
- Message routing and storage
- System state maintenance

The module uses environment variables for configuration and maintains in-memory
state of all system entities.
"""

from rti_chatter import Chatter
from idl_structs import Group
from uuid import uuid4
from copy import deepcopy
import asyncio
import time
from dotenv import load_dotenv
import os

# Load environment variables with override capability
load_dotenv(override=True)

# Configure message polling interval from environment or use default
TIME_SLEEP = float(os.environ.get("TIME_SLEEP", 0.3))  # Time between message checks

class AppContext:
    """
    Main application context class for the DDS chat system.
    
    This class manages the entire chat application state including:
    - User (Chatter) registration and management
    - Group creation and management
    - Message routing and storage
    - User-Group relationships
    
    The context maintains three main dictionaries:
    1. chatters_dict: Maps user IDs to their Chatter objects
    2. groups_dict: Maps group IDs to their Group objects
    3. chatters_rcvd_messages: Stores received messages for each user
    """

    def __init__(self):
        """
        Initialize the application context with empty state containers.
        """
        # Map of user IDs to their corresponding Chatter objects
        self.chatters_dict = {}  # {user_id: Chatter}
        
        # Map of group IDs to their corresponding Group objects
        self.groups_dict = {}  # {group_id: Group}
        
        # Storage for messages received by each user
        self.chatters_rcvd_messages = {}  # {user_id: [{group_id, sender_id, msg}, ...]}
    
    def create_group(self, group_name: str) -> str:
        """
        Create a new chat group in the system.
        
        Args:
            group_name (str): The display name for the new group
            
        Returns:
            str: The unique ID generated for the new group
            
        Note:
            New groups are created empty - users must be explicitly added
            using add_user_to_group()
        
        Example:
            >>> group_id = app_context.create_group("Python Discussion")
            >>> print(group_id)
            'f7d4e3b2-1a2b-3c4d-5e6f-7g8h9i0j1k2l'
        """
        group_id = str(uuid4())
        self.groups_dict[group_id] = Group(group_id=group_id, 
                                         group_name=group_name, 
                                         participating_chatters_id=[])
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
        Add a user to a chat group.
        
        This method:
        1. Validates both user and group existence
        2. Updates the user's group membership
        3. Updates the group's member list
        
        Args:
            user_id (str): The ID of the user to add
            group_id (str): The ID of the group to add the user to
            
        Returns:
            int: Status code indicating the result:
                 -2: User ID does not exist
                 -1: Group ID does not exist
                  0: Operation successful
                  
        Example:
            >>> status = app_context.add_user_to_group("user123", "group456")
            >>> if status == 0:
            ...     print("User added successfully")
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
        """
        Continuously poll for new messages for a specific user.
        
        This method runs in an infinite loop to:
        1. Check for new messages for the specified user
        2. Update the message cache with any new messages
        3. Sleep for a configured interval
        
        Args:
            user_id (str): The ID of the user to poll messages for
            
        Note:
            This method should typically be run in a separate thread as it
            contains an infinite loop with sleep intervals.
        """
        chatter = self.chatters_dict[user_id]

        while True:
            # Get any new messages
            msgs_dict = chatter.receive_messages()
            # Update the message cache for this user
            self.chatters_rcvd_messages[user_id] = self.chatters_rcvd_messages.get(user_id, []).extend(msgs_dict[user_id])
            # Wait before next poll
            time.sleep(TIME_SLEEP)

    def get_user_groups(self, user_id: str):
        """
        Get all groups that a specific user is a member of.
        
        Args:
            user_id (str): The ID of the user to get groups for
            
        Returns:
            dict or int: If successful, returns a dictionary mapping group IDs to group names
                        for all groups the user is a member of.
                        Returns -1 if the user ID does not exist.
                        
        Example:
            >>> app_context.get_user_groups("user123")
            {
                "group1": "Python Developers",
                "group2": "Project Team Alpha"
            }
        """
        if self.chatters_dict.get(user_id) is None:
            return -1
        
        return {group_id: self.groups_dict[group_id].group_name
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
        """
        Get a copy of all groups in the system.
        
        Returns:
            dict: A deep copy of the groups dictionary to prevent direct
                 modification of internal state.
        """
        return deepcopy(self.groups_dict)
    
    def get_chatters(self):
        """
        Get information about all chatters in the system.
        
        Note:
            This method returns a simplified version of chatter information
            because DDS readers and writers cannot be pickled. Only basic
            attributes are included.
        
        Returns:
            dict: A dictionary mapping user IDs to their information:
                {
                    user_id: {
                        "user_id": str,
                        "user_name": str,
                        "groups": list[str]  # List of group IDs
                    },
                    ...
                }
        """
        return {uid: {
                    "user_id": c.member.user_id,
                    "user_name": c.member.user_name,
                    "groups": list(c.member.participating_groups_id)
                } for uid, c in self.chatters_dict.items()}

    def get_rcvd_messages(self, user_id: str):
        """
        Get all received messages for a specific user.
        
        Args:
            user_id (str): The ID of the user to get messages for
            
        Returns:
            list: A list of message dictionaries containing:
                [
                    {
                        "group_id": str,
                        "sender_id": str,
                        "msg": str
                    },
                    ...
                ]
                Returns an empty list if no messages exist or user not found.
        """
        return self.chatters_rcvd_messages.get(user_id, [])    

