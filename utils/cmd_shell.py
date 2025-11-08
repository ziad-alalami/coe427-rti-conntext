import cmd
from app import AppContext
import asyncio
import threading
import shlex

def split_args(func):
    """Decorator to automatically split the arg string into args"""
    def wrapper(self, arg):
        try:
            args = shlex.split(arg)  # handles spaces and quotes
        except ValueError as e:
            print("Error parsing arguments:", e)
            return
        return func(self, *args)
    return wrapper


class ChatShell(cmd.Cmd):

    prompt = "> "
    app = AppContext()

    def do_create_group(self, group_name):

        group_id = self.app.create_group(group_name= group_name)
        print(f"GROUP {group_name} CREATED SUCCESSFULLY WITH ID: {group_id}")
        
        print()

    def do_create_user(self, user_name):

        user_id = self.app.create_chatter(user_name= user_name)
        print(f"USER {user_name} CREATED SUCCESSFULLY WITH ID: {user_id}")

        threading.Thread(
        target=lambda: self.app.loop_messages(user_id=user_id),
        daemon=True
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

        msg = "".join(msg)
        status = self.app.send_message(group_id= group_id, user_id= user_id, msg= msg)

        if status == -2:
            print(f"USER WITH ID {user_id} DOES NOT EXIST. CHECK USERS OR HELP FOR MORE DETAILS.")
        
        if status == -1:
            print(f"GROUP WITH ID {group_id} DOES NOT EXIST. CHECK GROUPS OR HELP FOR MORE DETAILS.")
        
        elif status == 0:
            print(f"USER WITH ID {user_id} SENT MESSAGE TO GROUP WITH ID {group_id} SUCCESSFULLY.")  
        
        print()
    
    def do_list_groups(self, arg = None):

        groups = self.app.get_groups()

        for group in groups.values():

            print(f"GROUP ID {group.group_id} WITH NAME {group.group_name}")

        print()
    
    def do_list_users(self, arg = None):

        users = self.app.get_chatters()

        for user in users.values():

            print(f"USER ID {user.get("user_id")} WITH NAME {user.get("user_name")}")

        print()
    
    def do_get_groups(self, user_id):

        user_groups_dict = self.app.get_user_groups(user_id= user_id)

        if user_groups_dict == -1:
            print(f"USER WITH ID {user_id} DOES NOT EXIST. CHECK USERS OR HELP FOR MORE DETAILS.")
        
        else:

            print(f"USER WITH ID {user_id} IS IN THE FOLLOWING GROUPS: ")

            for group_id in user_groups_dict.keys():
                print(f"GROUP WITH ID {group_id} AND NAME {user_groups_dict[group_id]}")
        
        print()
    
    def do_get_users(self, group_id):

        group_users_dict = self.app.get_group_users(group_id= group_id)

        if group_users_dict == -1:
            print(f"GROUP WITH ID {group_id} DOES NOT EXIST. CHECK GROUPS OR HELP FOR MORE DETAILS.")
        
        else:

            print(f"GROUP WITH ID {group_id} IS IN THE FOLLOWING GROUPS: ")

            for group_id in group_users_dict.keys():
                print(f"USER WITH ID {group_id} AND NAME {group_users_dict[group_id]}")
        
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

    def do_h(self, arg = None):
        self.do_help()



