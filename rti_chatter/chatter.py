"""
RTI Connext DDS Chat Implementation Module

This module implements the core DDS (Data Distribution Service) chat functionality
using RTI Connext DDS. It provides a Chatter class that handles message publishing
and subscribing in a distributed chat system.

The implementation uses DDS topics for message distribution and supports:
- User identification and management
- Group-based messaging
- Real-time message publishing and subscribing
- Unique message identification
"""

from idl_structs import Member, Message
import rti.connextdds as dds
from uuid import uuid4

# Initialize DDS infrastructure
participant = dds.DomainParticipant(domain_id=0)  # Using domain 0 for communication
topic = dds.Topic(participant=participant, topic_name="MessageTopic", type=Message)  # Main message topic



class Chatter:
    """
    A class representing a chat participant in the DDS chat system.
    
    This class manages a chat participant's ability to:
    - Join chat groups
    - Send messages to groups
    - Receive messages from groups they're part of
    
    Attributes:
        member (Member): The member information including ID, name, and group memberships
        reader (dds.DataReader): DDS reader for receiving messages
        writer (dds.DataWriter): DDS writer for sending messages
    """

    def __init__(self, user_id: str, user_name: str):
        """
        Initialize a new chat participant.
        
        Args:
            user_id (str): Unique identifier for the user
            user_name (str): Display name of the user
        """
        # Initialize member with empty group list
        self.member = Member(user_id=user_id, user_name=user_name, participating_groups_id=[])

        # Set up DDS readers and writers for message communication
        self.reader = dds.DataReader(topic=topic)
        self.writer = dds.DataWriter(topic=topic)
    
    def add_group(self, group_id: str):
        """
        Add the user to a new chat group.
        
        This method adds the user to a new group for message reception.
        Note: Content filtering is currently commented out but could be
        implemented for more efficient message filtering.
        
        Args:
            group_id (str): The ID of the group to join
            
        Note:
            The commented code shows how to implement DDS content filtering
            which could be used to filter messages at the middleware level
        """
        if group_id not in self.member.participating_groups_id:
            self.member.participating_groups_id.append(group_id)

        # Implementation of DDS content filtering (currently disabled)
        # group_filters = " OR ".join([f"group_id = '{gid}'" for gid in self.member.participating_groups_id])
        # my_filter = dds.Filter(group_filters)

        # filtered_topic = dds.ContentFilteredTopic(topic, f"FilteredChat_{self.member.user_id}", my_filter)

        # self.reader.close()  # close old reader
        # self.reader = dds.DataReader(filtered_topic)

          
    def send_message(self, group_id: str, msg: str):
        """
        Send a message to a specific group.
        
        Creates a new Message object with a unique ID and publishes it
        to the DDS network for distribution to group members.
        
        Args:
            group_id (str): The ID of the group to send the message to
            msg (str): The message content to send
        """
        # Create message object with unique ID and metadata
        msg_object = Message(msg_id=str(uuid4()),
                       sender_id=self.member.user_id, 
                       group_id=group_id,
                       msg=msg)
        
        # Publish the message using DDS writer
        self.writer.write(msg_object)


    def receive_messages(self):
        """
        Receive and process new messages for this user.
        
        Reads all available messages from the DDS reader and filters them based on:
        - Message validity
        - Not being the sender
        - Being a member of the message's target group
        
        Returns:
            dict: A dictionary containing received messages organized by user ID
                 Format: {
                     user_id: [
                         {
                             "group_id": str,
                             "sender_id": str,
                             "msg": str
                         },
                         ...
                     ]
                 }
        """
        msgs_dict = {self.member.user_id: []}

        # Process all available messages
        for sample in self.reader.take():
            # Filter messages: valid, not self-sent, and in user's groups
            if (sample.info.valid and 
                sample.data.sender_id != self.member.user_id and 
                sample.data.group_id in self.member.participating_groups_id):
                
                # Debug printing
                print(f"FROM SENDER {sample.data.sender_id} TO RECEIVER {self.member.user_id} IN GROUP {sample.data.group_id}: ")
                print(sample.data.msg)

                # Store message in result dictionary
                msgs_dict[self.member.user_id].append({
                    "group_id": sample.data.group_id,
                    "sender_id": sample.data.sender_id,
                    "msg": sample.data.msg
                })
        
        return msgs_dict
            
        






