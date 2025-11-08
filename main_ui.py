"""
DDS Chat System GUI Application

This module implements a graphical user interface for a DDS-based chat system.
It provides functionality for:
- User management (create/remove users)
- Group management (create/remove groups)
- Group membership management
- Real-time chat functionality with message polling
- Multi-user and multi-group support

The GUI is built using tkinter and implements a two-panel design with management
features on the left and chat functionality on the right.
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
from utils import ChatShell


class ChatGUI:
    """
    Main GUI class for the DDS Chat System.
    
    This class manages the entire chat application interface, including:
    - User interface initialization and layout
    - User and group management
    - Message handling and display
    - Real-time updates through polling
    
    Attributes:
        root (tk.Tk): The main window of the application
        shell (ChatShell): Interface to the DDS chat functionality
        group_messages (dict): Cache of messages for each group
        user_messages (dict): Cache of messages for each user
    """
    
    def __init__(self, root):
        """
        Initialize the ChatGUI instance.
        
        Args:
            root (tk.Tk): The root window for the application
        """
        self.root = root
        self.root.title("DDS Chat System")
        self.root.geometry("1200x700")  # Set default window size
        
        self.shell = ChatShell()  # Initialize DDS chat interface
        self.group_messages = {}  # Store messages by group
        self.init_ui()  # Setup the user interface
        self.refresh_lists()  # Initialize all lists and dropdowns
        
    def init_ui(self):
        """Initialize the user interface"""
        # Main container with two panels
        main_paned = tk.PanedWindow(self.root, orient=tk.HORIZONTAL, sashrelief=tk.RAISED)
        main_paned.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Left panel - Management
        left_frame = tk.Frame(main_paned, width=400)
        main_paned.add(left_frame)
        self.create_management_panel(left_frame)
        
        # Right panel - Chat
        right_frame = tk.Frame(main_paned, width=600)
        main_paned.add(right_frame)
        self.create_chat_panel(right_frame)
        
    def create_management_panel(self, parent):
        """
        Create the left management panel of the GUI.
        
        This panel contains three main tabs:
        1. Users - For creating and managing users
        2. Groups - For creating and managing chat groups
        3. Membership - For managing user group memberships
        
        Args:
            parent (tk.Frame): The parent frame to contain the management panel
            
        The panel uses a notebook (tabbed) layout for organization and
        provides controls for all administrative functions.
        """
        # Title
        title = tk.Label(parent, text="Management Panel", font=("Arial", 14, "bold"))
        title.pack(pady=10)
        
        # Notebook (tabs)
        notebook = ttk.Notebook(parent)
        notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Users tab
        users_frame = tk.Frame(notebook)
        notebook.add(users_frame, text="Users")
        self.create_users_tab(users_frame)
        
        # Groups tab
        groups_frame = tk.Frame(notebook)
        notebook.add(groups_frame, text="Groups")
        self.create_groups_tab(groups_frame)
        
        # Membership tab
        membership_frame = tk.Frame(notebook)
        notebook.add(membership_frame, text="Membership")
        self.create_membership_tab(membership_frame)
        
    def create_users_tab(self, parent):
        """Create users management tab"""
        # Create user section
        create_frame = tk.LabelFrame(parent, text="Create User", padx=10, pady=10)
        create_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(create_frame, text="User Name:").pack(side=tk.LEFT, padx=5)
        self.user_name_input = tk.Entry(create_frame, width=20)
        self.user_name_input.pack(side=tk.LEFT, padx=5)
        
        create_btn = tk.Button(create_frame, text="Create User", command=self.create_user)
        create_btn.pack(side=tk.LEFT, padx=5)
        
        # User list section
        list_frame = tk.LabelFrame(parent, text="User List", padx=10, pady=10)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Listbox with scrollbar
        list_container = tk.Frame(list_frame)
        list_container.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = tk.Scrollbar(list_container)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.user_listbox = tk.Listbox(list_container, yscrollcommand=scrollbar.set)
        self.user_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.user_listbox.bind('<Double-Button-1>', self.show_user_groups)
        
        scrollbar.config(command=self.user_listbox.yview)
        
        # Buttons
        btn_frame = tk.Frame(list_frame)
        btn_frame.pack(fill=tk.X, pady=5)
        
        refresh_btn = tk.Button(btn_frame, text="Refresh Users", command=self.refresh_user_list)
        refresh_btn.pack(side=tk.LEFT, padx=5)
        
        remove_btn = tk.Button(btn_frame, text="Remove Selected", command=self.remove_user)
        remove_btn.pack(side=tk.LEFT, padx=5)
        
    def create_groups_tab(self, parent):
        """Create groups management tab"""
        # Create group section
        create_frame = tk.LabelFrame(parent, text="Create Group", padx=10, pady=10)
        create_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(create_frame, text="Group Name:").pack(side=tk.LEFT, padx=5)
        self.group_name_input = tk.Entry(create_frame, width=20)
        self.group_name_input.pack(side=tk.LEFT, padx=5)
        
        create_btn = tk.Button(create_frame, text="Create Group", command=self.create_group)
        create_btn.pack(side=tk.LEFT, padx=5)
        
        # Group list section
        list_frame = tk.LabelFrame(parent, text="Group List", padx=10, pady=10)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Listbox with scrollbar
        list_container = tk.Frame(list_frame)
        list_container.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = tk.Scrollbar(list_container)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.group_listbox = tk.Listbox(list_container, yscrollcommand=scrollbar.set)
        self.group_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.group_listbox.bind('<Double-Button-1>', self.show_group_users)
        
        scrollbar.config(command=self.group_listbox.yview)
        
        # Buttons
        btn_frame = tk.Frame(list_frame)
        btn_frame.pack(fill=tk.X, pady=5)
        
        refresh_btn = tk.Button(btn_frame, text="Refresh Groups", command=self.refresh_group_list)
        refresh_btn.pack(side=tk.LEFT, padx=5)
        
        remove_btn = tk.Button(btn_frame, text="Remove Selected", command=self.remove_group)
        remove_btn.pack(side=tk.LEFT, padx=5)
        
    def create_membership_tab(self, parent):
        """Create membership management tab"""
        info = tk.Label(parent, text="Add users to groups by selecting from dropdowns", 
                       wraplength=300, justify=tk.LEFT)
        info.pack(pady=10)
        
        # Add user to group section
        add_frame = tk.LabelFrame(parent, text="Add User to Group", padx=10, pady=10)
        add_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # User dropdown
        user_frame = tk.Frame(add_frame)
        user_frame.pack(fill=tk.X, pady=5)
        tk.Label(user_frame, text="User:", width=10).pack(side=tk.LEFT, padx=5)
        self.membership_user_combo = ttk.Combobox(user_frame, state='readonly', width=40)
        self.membership_user_combo.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        # Group dropdown
        group_frame = tk.Frame(add_frame)
        group_frame.pack(fill=tk.X, pady=5)
        tk.Label(group_frame, text="Group:", width=10).pack(side=tk.LEFT, padx=5)
        self.membership_group_combo = ttk.Combobox(group_frame, state='readonly', width=40)
        self.membership_group_combo.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        # Refresh button
        refresh_btn = tk.Button(add_frame, text="Refresh Lists", command=self.refresh_membership_dropdowns)
        refresh_btn.pack(pady=5)
        
        # Add button
        add_btn = tk.Button(add_frame, text="Add User to Group", command=self.add_user_to_group)
        add_btn.pack(pady=10)
        
        # View section
        view_frame = tk.LabelFrame(parent, text="View Membership", padx=10, pady=10)
        view_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Selection dropdown
        select_frame = tk.Frame(view_frame)
        select_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(select_frame, text="Select:").pack(side=tk.LEFT, padx=5)
        self.view_type = tk.StringVar(value="user")
        tk.Radiobutton(select_frame, text="User's Groups", variable=self.view_type, 
                      value="user", command=self.update_view_dropdown).pack(side=tk.LEFT, padx=5)
        tk.Radiobutton(select_frame, text="Group's Users", variable=self.view_type, 
                      value="group", command=self.update_view_dropdown).pack(side=tk.LEFT, padx=5)
        
        dropdown_frame = tk.Frame(view_frame)
        dropdown_frame.pack(fill=tk.X, pady=5)
        self.view_combo = ttk.Combobox(dropdown_frame, state='readonly', width=40)
        self.view_combo.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.view_combo.bind('<<ComboboxSelected>>', self.show_membership_details)
        
        view_btn = tk.Button(dropdown_frame, text="View", command=lambda: self.show_membership_details(None))
        view_btn.pack(side=tk.LEFT, padx=5)
        
        # Display area
        self.membership_display = scrolledtext.ScrolledText(view_frame, height=8, wrap=tk.WORD)
        self.membership_display.pack(fill=tk.BOTH, expand=True, pady=5)
        
    def create_chat_panel(self, parent):
        """
        Create the right chat panel of the GUI.
        
        This panel handles all chat-related functionality including:
        - Active user selection
        - Message display area
        - Group selection for sending messages
        - Message input and sending
        
        Features:
        - Real-time message updates
        - Support for multiple chat groups
        - Message history per user/group
        - Clear chat functionality
        
        Args:
            parent (tk.Frame): The parent frame to contain the chat panel
        """
        # Title
        title = tk.Label(parent, text="Chat Panel", font=("Arial", 14, "bold"))
        title.pack(pady=10)
        
        # User selection section
        user_select_frame = tk.LabelFrame(parent, text="Active User", padx=10, pady=10)
        user_select_frame.pack(fill=tk.X, padx=10, pady=5)
        
        select_frame = tk.Frame(user_select_frame)
        select_frame.pack(fill=tk.X)
        
        tk.Label(select_frame, text="View messages as:").pack(side=tk.LEFT, padx=5)
        self.active_user_combo = ttk.Combobox(select_frame, width=35, state='readonly')
        self.active_user_combo.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.active_user_combo.bind('<<ComboboxSelected>>', self.on_active_user_changed)
        
        refresh_active_btn = tk.Button(select_frame, text="↻", width=3, command=self.refresh_active_user_dropdown)
        refresh_active_btn.pack(side=tk.LEFT, padx=5)
        
        # Message display
        display_frame = tk.LabelFrame(parent, text="Messages", padx=10, pady=10)
        display_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.message_display = scrolledtext.ScrolledText(display_frame, wrap=tk.WORD, 
                                                         font=("Courier", 10), state=tk.DISABLED)
        self.message_display.pack(fill=tk.BOTH, expand=True)
        
        # Send message section
        send_frame = tk.LabelFrame(parent, text="Send Message", padx=10, pady=10)
        send_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Group selection
        group_frame = tk.Frame(send_frame)
        group_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(group_frame, text="To Group:").pack(side=tk.LEFT, padx=5)
        self.msg_group_combo = ttk.Combobox(group_frame, width=35, state='readonly')
        self.msg_group_combo.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.msg_group_combo.bind('<<ComboboxSelected>>', self.on_group_selected)
        
        refresh_btn = tk.Button(group_frame, text="↻", width=3, command=self.refresh_message_dropdowns)
        refresh_btn.pack(side=tk.LEFT, padx=5)
        
        # Message row
        msg_frame = tk.Frame(send_frame)
        msg_frame.pack(fill=tk.X, pady=5)
        
        self.message_input = tk.Entry(msg_frame)
        self.message_input.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.message_input.bind('<Return>', lambda e: self.send_message())
        
        send_btn = tk.Button(msg_frame, text="Send", command=self.send_message)
        send_btn.pack(side=tk.LEFT, padx=5)
        
        # Clear button
        clear_btn = tk.Button(parent, text="Clear Chat", command=self.clear_chat)
        clear_btn.pack(pady=5)
        
        # Initialize message storage for each user
        self.user_messages = {}  # {user_id: [messages]}
        
    # User management methods
    def create_user(self):
        """Create a new user"""
        user_name = self.user_name_input.get().strip()
        if not user_name:
            messagebox.showwarning("Error", "Please enter a user name")
            return
        
        user_id = self.shell.app.create_chatter(user_name=user_name)
        messagebox.showinfo("Success", f"User '{user_name}' created with ID: {user_id}")
        
        # Initialize message storage for this user
        self.user_messages[user_id] = []
        
        # Start message polling thread for this user
        threading.Thread(
            target=lambda: self.poll_messages(user_id),
            daemon=True
        ).start()
        
        self.user_name_input.delete(0, tk.END)
        self.refresh_user_list()
        self.refresh_active_user_dropdown()
    
    def poll_messages(self, user_id):
        """
        Continuously poll for new messages for a specific user.
        
        This method runs in a separate thread for each user and:
        - Periodically checks for new messages
        - Processes and stores messages in both user and group caches
        - Updates the display if messages are for the active user
        
        Args:
            user_id (str): The ID of the user to poll messages for
            
        Note:
            This method runs indefinitely until the thread is terminated
        """
        import time
        while True:
            try:
                messages = self.shell.app.get_rcvd_messages(user_id=user_id)
                if messages:
                    for msg_data in messages:
                        group_id = msg_data.get('group_id', '')
                        sender_id = msg_data.get('sender_id', '')
                        message = msg_data.get('msg', '')

                        msg_entry = {
                            'group_id': group_id,
                            'sender_id': sender_id,
                            'message': message,
                            'is_sent': False
                        }

                        # Store per user
                        if user_id not in self.user_messages:
                            self.user_messages[user_id] = []
                        self.user_messages[user_id].append(msg_entry)

                        # Store per group
                        if group_id not in self.group_messages:
                            self.group_messages[group_id] = []
                        self.group_messages[group_id].append(msg_entry)

                        # Display immediately if this user is active
                        if self.get_active_user_id() == user_id:
                            self.root.after(0, lambda g=group_id, s=sender_id, m=message: 
                                            self.display_message(g, s, m, is_sent=False))

                time.sleep(0.5)

            except Exception as e:
                print(f"Error polling messages for user {user_id}: {e}")
                time.sleep(1)

    
    def remove_user(self):
        """Remove selected user"""
        selection = self.user_listbox.curselection()
        if not selection:
            messagebox.showwarning("Error", "Please select a user to remove")
            return
        
        user_id = self.user_data[selection[0]]
        status = self.shell.app.remove_user(user_id=user_id)
        
        if status == -1:
            messagebox.showwarning("Error", f"User with ID {user_id} does not exist")
        elif status == 0:
            messagebox.showinfo("Success", f"User with ID {user_id} deleted successfully")
            self.refresh_user_list()
    
    def show_user_groups(self, event):
        """Show groups for selected user"""
        selection = self.user_listbox.curselection()
        if not selection:
            return
        
        user_id = self.user_data[selection[0]]
        user_name = self.user_listbox.get(selection[0]).split(" - ")[1]
        
        user_groups_dict = self.shell.app.get_user_groups(user_id=user_id)
        
        if user_groups_dict == -1:
            messagebox.showwarning("Error", f"User with ID {user_id} does not exist")
        else:
            groups_text = "\n".join([f"Group ID: {gid}, Name: {name}" 
                                    for gid, name in user_groups_dict.items()])
            if not groups_text:
                groups_text = "Not a member of any groups"
            messagebox.showinfo(f"Groups for {user_name}", groups_text)
    
    # Group management methods
    def create_group(self):
        """Create a new group"""
        group_name = self.group_name_input.get().strip()
        if not group_name:
            messagebox.showwarning("Error", "Please enter a group name")
            return
        
        group_id = self.shell.app.create_group(group_name=group_name)
        messagebox.showinfo("Success", f"Group '{group_name}' created with ID: {group_id}")
        
        self.group_name_input.delete(0, tk.END)
        self.refresh_group_list()
    
    def remove_group(self):
        """Remove selected group"""
        selection = self.group_listbox.curselection()
        if not selection:
            messagebox.showwarning("Error", "Please select a group to remove")
            return
        
        group_id = self.group_data[selection[0]]
        status = self.shell.app.remove_group(group_id=group_id)
        
        if status == -1:
            messagebox.showwarning("Error", f"Group with ID {group_id} does not exist")
        elif status == 0:
            messagebox.showinfo("Success", f"Group with ID {group_id} deleted successfully")
            self.refresh_group_list()
    
    def show_group_users(self, event):
        """Show users in selected group"""
        selection = self.group_listbox.curselection()
        if not selection:
            return
        
        group_id = self.group_data[selection[0]]
        group_name = self.group_listbox.get(selection[0]).split(" - ")[1]
        
        group_users_dict = self.shell.app.get_group_users(group_id=group_id)
        
        if group_users_dict == -1:
            messagebox.showwarning("Error", f"Group with ID {group_id} does not exist")
        else:
            users_text = "\n".join([f"User ID: {uid}, Name: {name}" 
                                   for uid, name in group_users_dict.items()])
            if not users_text:
                users_text = "No users in this group"
            messagebox.showinfo(f"Users in {group_name}", users_text)
    
    # Membership management
    def add_user_to_group(self):
        """Add user to group"""
        user_selection = self.membership_user_combo.get()
        group_selection = self.membership_group_combo.get()
        
        if not user_selection or not group_selection:
            messagebox.showwarning("Error", "Please select both a User and a Group")
            return
        
        # Extract ID from the selection (format: "ID: xxx - Name")
        user_id = user_selection.split(" - ")[0].replace("ID: ", "")
        group_id = group_selection.split(" - ")[0].replace("ID: ", "")
        
        status = self.shell.app.add_user_to_group(user_id=user_id, group_id=group_id)
        
        if status == -2:
            messagebox.showwarning("Error", f"User with ID {user_id} does not exist")
        elif status == -1:
            messagebox.showwarning("Error", f"Group with ID {group_id} does not exist")
        elif status == 0:
            messagebox.showinfo("Success", 
                               f"User {user_id} added to Group {group_id} successfully")
            self.membership_user_combo.set('')
            self.membership_group_combo.set('')
    
    # Chat methods
    def send_message(self):
        """
        Send a message from the active user to the selected group.
        
        This method:
        1. Validates the active user and selected group
        2. Checks if the user is a member of the selected group
        3. Sends the message through the DDS system
        4. Updates the local message cache and display
        
        Error conditions handled:
        - No active user selected
        - No group selected
        - Empty message
        - User not in selected group
        - Non-existent user/group
        """
        # Get active user
        active_user_selection = self.active_user_combo.get()
        if not active_user_selection:
            messagebox.showwarning("Error", "Please select an active user first")
            return
        
        group_selection = self.msg_group_combo.get()
        message = self.message_input.get().strip()
        
        if not group_selection or not message:
            messagebox.showwarning("Error", "Please select a group and enter a message")
            return
        
        # Extract IDs
        user_id = active_user_selection.split(" - ")[0].replace("ID: ", "")
        group_id = group_selection.split(" - ")[0].replace("ID: ", "")
        
        # Check if active user is in the selected group
        user_groups = self.shell.app.get_user_groups(user_id=user_id)
        if user_groups != -1 and group_id not in user_groups:
            messagebox.showwarning("Error", "Active user is not a member of this group. Please add them first.")
            return
        
        status = self.shell.app.send_message(group_id=group_id, user_id=user_id, msg=message)
        
        if status == -2:
            messagebox.showwarning("Error", f"User with ID {user_id} does not exist")
        elif status == -1:
            messagebox.showwarning("Error", f"Group with ID {group_id} does not exist")
        elif status == 0:
            
            # Store the sent message in the central group store
            # This ensures it's available when switching users
            msg_entry = {
                'group_id': group_id,
                'sender_id': user_id,
                'message': message,
                'is_sent': True # Mark this as the original "sent" message
            }
            if group_id not in self.group_messages:
                self.group_messages[group_id] = []
            
            self.group_messages[group_id].append(msg_entry)
            
            # Display the sent message immediately
            self.display_message(group_id, user_id, message, is_sent=True)
            self.message_input.delete(0, tk.END)
    
    def display_message(self, group_id, sender_id, message, is_sent=False):
        """Display a message in the chat"""
        active_user_id = self.get_active_user_id()
        
        # Store message for active user
        if active_user_id:
            message_data = {
                'group_id': group_id,
                'sender_id': sender_id,
                'message': message,
                'is_sent': is_sent
            }
            if active_user_id not in self.user_messages:
                self.user_messages[active_user_id] = []
            self.user_messages[active_user_id].append(message_data)
        
        self.message_display.config(state=tk.NORMAL)
        
        if is_sent:
            # Message sent by active user
            self.message_display.insert(tk.END, f"[Group {group_id}] You: {message}\n")
        else:
            # Message received by active user
            self.message_display.insert(tk.END, f"[Group {group_id}] User {sender_id}: {message}\n")
        
        self.message_display.see(tk.END)
        self.message_display.config(state=tk.DISABLED)
    
    def clear_chat(self):
        """Clear the chat display for current active user"""
        active_user_id = self.get_active_user_id()
        if active_user_id and active_user_id in self.user_messages:
            # Clear stored messages for this user
            self.user_messages[active_user_id] = []
        
        self.message_display.config(state=tk.NORMAL)
        self.message_display.delete(1.0, tk.END)
        self.message_display.config(state=tk.DISABLED)
    
    def get_active_user_id(self):
        """Get the currently active user's ID"""
        selection = self.active_user_combo.get()
        if not selection:
            return None
        return selection.split(" - ")[0].replace("ID: ", "")
    
    def on_active_user_changed(self, event=None):
        active_user_id = self.get_active_user_id()
        if not active_user_id:
            return

        self.message_display.config(state=tk.NORMAL)
        self.message_display.delete(1.0, tk.END)

        # Fetch groups for this user
        user_groups = self.shell.app.get_user_groups(user_id=active_user_id)
        if user_groups != -1:
            all_messages = []
            for group_id in user_groups:
                messages = self.group_messages.get(group_id, [])
                all_messages.extend(messages)
            
            
            # Process and display all messages for this user's groups
            for msg_data in all_messages:
                msg_text = msg_data.get('message', '') 

                if msg_data['sender_id'] == active_user_id:
                    # If the active user is the sender, display "You"
                    self.message_display.insert(tk.END,
                        f"[Group {msg_data['group_id']}] You: {msg_text}\n")
                else:
                    # Otherwise, display the sender's ID
                    self.message_display.insert(tk.END,
                        f"[Group {msg_data['group_id']}] User {msg_data['sender_id']}: {msg_text}\n")
            
        self.message_display.see(tk.END)
        self.message_display.config(state=tk.DISABLED)

        # Update group dropdown
        self.update_group_dropdown_for_active_user()
    
    def update_group_dropdown_for_active_user(self):
        """Update group dropdown to show only groups the active user is in"""
        active_user_id = self.get_active_user_id()
        if not active_user_id:
            self.msg_group_combo['values'] = []
            return
        
        user_groups = self.shell.app.get_user_groups(user_id=active_user_id)
        
        if user_groups == -1 or not user_groups:
            self.msg_group_combo['values'] = []
            self.msg_group_combo.set('')
        else:
            group_list = [f"ID: {gid} - {gname}" for gid, gname in user_groups.items()]
            self.msg_group_combo['values'] = group_list
            self.msg_group_combo.set('')
    
    def refresh_active_user_dropdown(self):
        """Refresh the active user dropdown"""
        users = self.shell.app.get_chatters()
        user_list = [f"ID: {user['user_id']} - {user['user_name']}" for user in users.values()]
        self.active_user_combo['values'] = user_list
    
    # List refresh methods
    def refresh_lists(self):
        """Refresh all lists"""
        self.refresh_user_list()
        self.refresh_group_list()
        self.refresh_membership_dropdowns()
        self.refresh_message_dropdowns()
    
    def refresh_user_list(self):
        """Refresh the user list"""
        self.user_listbox.delete(0, tk.END)
        self.user_data = []
        
        users = self.shell.app.get_chatters()
        for user in users.values():
            self.user_listbox.insert(tk.END, f"ID: {user['user_id']} - {user['user_name']}")
            self.user_data.append(user['user_id'])
    
    def refresh_group_list(self):
        """Refresh the group list"""
        self.group_listbox.delete(0, tk.END)
        self.group_data = []
        
        groups = self.shell.app.get_groups()
        for group in groups.values():
            self.group_listbox.insert(tk.END, f"ID: {group.group_id} - {group.group_name}")
            self.group_data.append(group.group_id)
    
    def refresh_membership_dropdowns(self):
        """Refresh the dropdowns in the membership tab"""
        # Refresh users dropdown
        users = self.shell.app.get_chatters()
        user_list = [f"ID: {user['user_id']} - {user['user_name']}" for user in users.values()]
        self.membership_user_combo['values'] = user_list
        
        # Refresh groups dropdown
        groups = self.shell.app.get_groups()
        group_list = [f"ID: {group.group_id} - {group.group_name}" for group in groups.values()]
        self.membership_group_combo['values'] = group_list
    
    def refresh_message_dropdowns(self):
        """Refresh the dropdowns in the send message section"""
        # Group dropdown is now handled by update_group_dropdown_for_active_user
        # which is called when active user changes
        self.update_group_dropdown_for_active_user()
    
    def on_group_selected(self, event=None):
        """When a group is selected, validate that active user is a member"""
        group_selection = self.msg_group_combo.get()
        active_user_id = self.get_active_user_id()
        
        if not group_selection or not active_user_id:
            return
        
        # Group dropdown already filtered to show only user's groups
        # So no additional validation needed here
    
    def update_view_dropdown(self):
        """Update the view dropdown based on selected type"""
        view_type = self.view_type.get()
        
        if view_type == "user":
            # Show users
            users = self.shell.app.get_chatters()
            items = [f"ID: {user['user_id']} - {user['user_name']}" for user in users.values()]
        else:
            # Show groups
            groups = self.shell.app.get_groups()
            items = [f"ID: {group.group_id} - {group.group_name}" for group in groups.values()]
        
        self.view_combo['values'] = items
        self.view_combo.set('')
        self.membership_display.delete(1.0, tk.END)
    
    def show_membership_details(self, event=None):
        """Show membership details based on selection"""
        selection = self.view_combo.get()
        if not selection:
            return
        
        self.membership_display.delete(1.0, tk.END)
        
        # Extract ID
        item_id = selection.split(" - ")[0].replace("ID: ", "")
        item_name = " - ".join(selection.split(" - ")[1:])
        
        if self.view_type.get() == "user":
            # Show groups for this user
            user_groups_dict = self.shell.app.get_user_groups(user_id=item_id)
            
            if user_groups_dict == -1:
                self.membership_display.insert(tk.END, f"User with ID {item_id} does not exist")
            else:
                self.membership_display.insert(tk.END, f"Groups for User '{item_name}' (ID: {item_id}):\n\n")
                if user_groups_dict:
                    for gid, gname in user_groups_dict.items():
                        self.membership_display.insert(tk.END, f"  • ID: {gid} - {gname}\n")
                else:
                    self.membership_display.insert(tk.END, "  Not a member of any groups\n")
        else:
            # Show users in this group
            group_users_dict = self.shell.app.get_group_users(group_id=item_id)
            
            if group_users_dict == -1:
                self.membership_display.insert(tk.END, f"Group with ID {item_id} does not exist")
            else:
                self.membership_display.insert(tk.END, f"Users in Group '{item_name}' (ID: {item_id}):\n\n")
                if group_users_dict:
                    for uid, uname in group_users_dict.items():
                        self.membership_display.insert(tk.END, f"  • ID: {uid} - {uname}\n")
                else:
                    self.membership_display.insert(tk.END, "  No users in this group\n")


def main():
    """
    Main entry point for the DDS Chat System GUI application.
    
    Creates the main window and starts the tkinter event loop.
    The application will run until the window is closed.
    """
    root = tk.Tk()
    ChatGUI(root)  # Initialize the main application GUI
    root.mainloop()  # Start the event loop


if __name__ == "__main__":
    main()