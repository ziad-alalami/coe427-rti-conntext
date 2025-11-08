from idl_structs import Member, Message
import rti.connextdds as dds
from uuid import uuid4


participant = dds.DomainParticipant(domain_id= 0)
topic = dds.Topic(participant= participant, topic_name= "MessageTopic", type = Message)





class Chatter:

    def __init__(self, user_id: str, user_name: str):

        self.member = Member(user_id= user_id, user_name = user_name, participating_groups_id = [])

        self.reader = dds.DataReader(topic= topic)
        self.writer = dds.DataWriter(topic = topic)
    
    def add_group(self, group_id: str):

        if group_id not in self.member.participating_groups_id:
            self.member.participating_groups_id.append(group_id)

        # group_filters = " OR ".join([f"group_id = '{gid}'" for gid in self.member.participating_groups_id])
        # my_filter = dds.Filter(group_filters)

        # filtered_topic = dds.ContentFilteredTopic(topic, f"FilteredChat_{self.member.user_id}", my_filter)

        # self.reader.close()  # close old reader
        # self.reader = dds.DataReader(filtered_topic)

          
    def send_message(self, group_id: str, msg: str):

        msg_object = Message(msg_id = str(uuid4()),
                       sender_id = self.member.user_id, 
                       group_id = group_id,
                       msg = msg)
        
        self.writer.write(msg_object)


    def receive_messages(self):
        msgs_dict = {self.member.user_id : []}

        for sample in self.reader.take():
            if sample.info.valid and sample.data.sender_id != self.member.user_id and sample.data.group_id in self.member.participating_groups_id:
                print(f"FROM SENDER {sample.data.sender_id} TO RECEIVER {self.member.user_id} IN GROUP {sample.data.group_id}: ")
                print(sample.data.msg)

                msgs_dict[self.member.user_id].append({
                    "group_id" : sample.data.group_id,
                    "sender_id": sample.data.sender_id,
                    "msg": sample.data.msg
                })
        
        return msgs_dict
            
        






