
# WARNING: THIS FILE IS AUTO-GENERATED. DO NOT MODIFY.

# This file was generated from chat.idl
# using RTI Code Generator (rtiddsgen) version 4.5.0.
# The rtiddsgen tool is part of the RTI Connext DDS distribution.
# For more information, type 'rtiddsgen -help' at a command shell
# or consult the Code Generator User's Manual.

from dataclasses import field
import rti.idl as idl




@idl.struct(

    member_annotations = {
        'msg_id': [idl.key, ],
        'msg': [idl.bound(2048),],
    }
)
class Message:
    msg_id: str = ""
    sender_id: str = ""
    group_id: str = ""
    msg: str = ""

@idl.struct(

    member_annotations = {
        'user_id': [idl.key, ],
        'username': [idl.bound(64),],
        'participating_groups_id': [idl.bound(100)],
    }
)
class Member:
    user_id: str = ""
    user_name: str = ""
    participating_groups_id: list[str] = field(default_factory=list)

@idl.struct(

    member_annotations = {
        'group_id': [idl.key, ],
        'group_name': [idl.bound(64),],
        'participating_chatters_id': [idl.bound(100)],
    }
)
class Group:
    group_id: str = ""
    group_name: str = ""
    participating_chatters_id: list[str] = field(default_factory=list)
