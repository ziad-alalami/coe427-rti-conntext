"""
Command-line Interface Module for DDS Chat System

This module provides a command-line interface for interacting with the DDS chat system.
It implements a shell-like interface using Python's cmd module, allowing users to:
- Create and manage users and groups
- Send and receive messages
- View system state and relationships
- Get help and documentation

The interface provides robust command parsing and error handling for all operations.
"""

import cmd
from app import AppContext
import asyncio
import threading
import shlex

def split_args(func):
    """
    Decorator to parse command arguments safely.
    
    This decorator handles:
    - Splitting argument strings into separate arguments
    - Preserving quoted strings as single arguments
    - Error handling for malformed input
    
    Args:
        func: The command method to wrap
        
    Returns:
        wrapper: The wrapped function that handles argument parsing
        
    Example:
        @split_args
        def do_command(self, arg1, arg2):
            # arg1 and arg2 are already split and stripped
            pass
    """
    def wrapper(self, arg):
        try:
            args = shlex.split(arg)  # Handles spaces and quotes properly
        except ValueError as e:
            print("Error parsing arguments:", e)
            return
        return func(self, *args)
    return wrapper


class ChatShell(cmd.Cmd):
    """
    Command-line interface for the DDS Chat System.
    
    This class provides a shell-like interface with commands for:
    - User management (create, remove, list users)
    - Group management (create, remove, list groups)
    - Membership management (add users to groups)
    - Message sending and receiving
    - System status and information
    
    All commands provide feedback and error messages for user guidance.
    The shell maintains an instance of AppContext for all operations.
    """

    prompt = "> "  # Command prompt symbol
    app = AppContext()  # Main application context

    def do_create_group(self, group_name):
        """
        Create a new chat group.
        
        Usage: create_group <group_name>
        
        Args:
            group_name (str): Name for the new group
            
        Example:
            > create_group "Python Developers"
        """
        group_id = self.app.create_group(group_name=group_name)
        print(f"GROUP {group_name} CREATED SUCCESSFULLY WITH ID: {group_id}")
        print()

    def do_create_user(self, user_name):
        """
        Create a new chat user/chatter.
        
        This command:
        1. Creates a new user with the given name
        2. Starts a background thread for message polling
        3. Returns the generated user ID
        
        Usage: create_user <user_name>
        
        Args:
            user_name (str): Name for the new user
            
        Example:
            > create_user "John Doe"
            
        Note:
            A daemon thread is started to continuously poll for messages
            for this user in the background.
        """
        user_id = self.app.create_chatter(user_name=user_name)
        print(f"USER {user_name} CREATED SUCCESSFULLY WITH ID: {user_id}")

        # Start background message polling thread
        threading.Thread(
            target=lambda: self.app.loop_messages(user_id=user_id),
            daemon=True  # Thread will terminate when main program exits
        ).start()

        print()

    @split_args
    def do_add_user_to_group(self, user_id, group_id):

        status = self.app.add_user_to_group(user_id= user_id, group_id= group_id)

        if status == -2:
            print(f"USER WITH ID {user_id} DOES NOT EXIST. CHECK USERS OR HELP FOR MORE DETAILS.")
        
        if status == -1:
            print(f"GROUP WITH ID {group_id} DOES NOT EXIST. CHECK GROUPS OR HELP FOR MORE DETAILS.")
        
        elif status == 0:
            print(f"USER WITH ID {user_id} ADDED TO GROUP WITH ID {group_id} SUCCESSFULLY.")
        
        print()

    
    def do_remove_group(self, group_id):

        status = self.app.remove_group(group_id= group_id)

        if status == -1:
            print(f"GROUP WITH ID {group_id} DOES NOT EXIST. CHECK GROUPS OR HELP FOR MORE DETAILS.")
        
        elif status == 0:
            print(f"GROUP WITH ID {group_id} DELETED SUCCESSFULLY.")

        print()

    def do_remove_user(self, user_id):

        status = self.app.remove_user(user_id= user_id)

        if status == -1:
            print(f"USER WITH ID {user_id} DOES NOT EXIST. CHECK USERS OR HELP FOR MORE DETAILS.")
        
        elif status == 0:
            print(f"USER WITH ID {user_id} DELETED SUCCESSFULLY.")
        
        print()


    @split_args
    def do_send_message(self, group_id, user_id, *msg):
        """
        Send a message from a user to a group.
        
        This command validates both user and group existence before
        attempting to send the message. All words after the user_id
        are joined to form the message.
        
        Usage: send_message <group_id> <user_id> <message text...>
        
        Args:
            group_id (str): ID of the target group
            user_id (str): ID of the sending user
            *msg: Variable number of words forming the message
            
        Returns:
            None, but prints status message:
            - Success confirmation
            - Error if user doesn't exist
            - Error if group doesn't exist
            
        Example:
            > send_message group123 user456 Hello everyone!
        """
        msg = "".join(msg)
        status = self.app.send_message(group_id=group_id, user_id=user_id, msg=msg)

        if status == -2:
            print(f"USER WITH ID {user_id} DOES NOT EXIST. CHECK USERS OR HELP FOR MORE DETAILS.")
        elif status == -1:
            print(f"GROUP WITH ID {group_id} DOES NOT EXIST. CHECK GROUPS OR HELP FOR MORE DETAILS.")
        elif status == 0:
            print(f"USER WITH ID {user_id} SENT MESSAGE TO GROUP WITH ID {group_id} SUCCESSFULLY.")  
        
        print()
    
    def do_list_groups(self, arg=None):
        """
        List all groups in the system.
        
        Displays a formatted list of all groups with their IDs
        and names. Takes no arguments.
        
        Usage: list_groups
        
        Example:
            > list_groups
            GROUP ID abc123 WITH NAME Python Team
            GROUP ID def456 WITH NAME Project Alpha
        """
        groups = self.app.get_groups()
        for group in groups.values():
            print(f"GROUP ID {group.group_id} WITH NAME {group.group_name}")
        print()
    
    def do_list_users(self, arg=None):
        """
        List all users in the system.
        
        Displays a formatted list of all users with their IDs
        and names. Takes no arguments.
        
        Usage: list_users
        
        Example:
            > list_users
            USER ID xyz789 WITH NAME John Doe
            USER ID uvw456 WITH NAME Jane Smith
        """
        users = self.app.get_chatters()
        for user in users.values():
            print(f"USER ID {user.get('user_id')} WITH NAME {user.get('user_name')}")
        print()
    
    def do_get_groups(self, user_id):
        """
        List all groups a specific user is a member of.
        
        Retrieves and displays all groups the specified user
        belongs to, with both group IDs and names.
        
        Usage: get_groups <user_id>
        
        Args:
            user_id (str): ID of the user to check
            
        Example:
            > get_groups user123
            USER WITH ID user123 IS IN THE FOLLOWING GROUPS:
            GROUP WITH ID group1 AND NAME Python Team
            GROUP WITH ID group2 AND NAME Project Alpha
        """
        user_groups_dict = self.app.get_user_groups(user_id=user_id)

        if user_groups_dict == -1:
            print(f"USER WITH ID {user_id} DOES NOT EXIST. CHECK USERS OR HELP FOR MORE DETAILS.")
        else:
            print(f"USER WITH ID {user_id} IS IN THE FOLLOWING GROUPS: ")
            for group_id in user_groups_dict.keys():
                print(f"GROUP WITH ID {group_id} AND NAME {user_groups_dict[group_id]}")
        
        print()
    
    def do_get_users(self, group_id):
        """
        List all users that are members of a specific group.
        
        Retrieves and displays all users who are members of
        the specified group, with both user IDs and names.
        
        Usage: get_users <group_id>
        
        Args:
            group_id (str): ID of the group to check
            
        Example:
            > get_users group123
            GROUP WITH ID group123 HAS THE FOLLOWING USERS:
            USER WITH ID user1 AND NAME John Doe
            USER WITH ID user2 AND NAME Jane Smith
        """
        group_users_dict = self.app.get_group_users(group_id=group_id)

        if group_users_dict == -1:
            print(f"GROUP WITH ID {group_id} DOES NOT EXIST. CHECK GROUPS OR HELP FOR MORE DETAILS.")
        else:
            print(f"GROUP WITH ID {group_id} HAS THE FOLLOWING USERS: ")
            for user_id in group_users_dict.keys():
                print(f"USER WITH ID {user_id} AND NAME {group_users_dict[user_id]}")
        
        print()


    def do_help(self, arg = None):

        print("\nWelcome to the DDS ChatShell! Manage users, groups, and messages in real time.\n")
        print("Available commands:\n")
        
        print("  create_group <group_name>")
        print("      Create a new group with the specified name.")
        print()
        
        print("  create_user <user_name>")
        print("      Create a new user/chatter with the specified name.")
        print()
        
        print("  add_user_to_group <user_id> <group_id>")
        print("      Add an existing user to an existing group.")
        print()
        
        print("  remove_group <group_id>")
        print("      Delete a group by its ID.")
        print()
        
        print("  remove_user <user_id>")
        print("      Delete a user by their ID.")
        print()
        
        print("  send_message <group_id> <user_id> <msg>")
        print("      Send a message from a user to a group.")
        print()

        print("  get_groups <user_id>")
        print("     Get all the group IDs and names of a given user.")
        print()

        print("  get_users <group_id>")
        print("     Get all the user IDs and names of a given group.")
        print()
        
        print("  list_groups")
        print("      List all groups with their IDs and names.")
        print()
        
        print("  list_users")
        print("      List all users with their IDs and names.")
        print()
        
        print("  help")
        print("      Show this help message.\n")
        print()

        print()

    def do_h(self, arg=None):
        """
        Shortcut for the help command.
        
        Usage: h
        
        This is a convenience method that simply calls the main help command.
        """
        self.do_help()



