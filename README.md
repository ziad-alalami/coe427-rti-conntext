# DDS Chat System
  
A distributed, real-time group chat application built on **RTI Connext DDS 7.5.0** middleware, implementing a publish-subscribe architecture for multi-user communication across processes and machines.

[CHECK THIS FOR A FULL DOCUMENTATION ON EVERYTHING AND AN AI AGENT TO EXPLAIN EVERYTHING FOR YOU](https://deepwiki.com/ziad-alalami/coe427-rti-conntext)
  
## Overview
  
This application enables multiple users to communicate through group-based messaging using Data Distribution Service (DDS) middleware. The system operates without a central server, using DDS Domain 0 for all communication through the `MessageTopic` publish-subscribe channel.  
  
### Key Features
  
- **Multi-user chat** with unique identity management via UUIDs 
- **Group-based messaging** with flexible membership management 
- **Distributed architecture** with no central server required
- **Reliable message delivery** with late-joiner support via transient local durability<cite />  
- **Dual interface**: Command-line shell and graphical UI   
- **Real-time synchronization** across all participants  
  
## Technology Stack
  
- **RTI Connext DDS 7.5.0**: Middleware for distributed communication  
- **Python 3.x**: Implementation language  
- **IDL (Interface Definition Language)**: Data structure definitions  
- **tkinter**: GUI framework  
  
## Architecture
  
The system follows a layered architecture with four main components:  
  
### Core Components
  
1. **AppContext** (`app/app_context.py`): Central coordinator managing all state and operations
   - Maintains `chatters_dict`, `groups_dict`, and `chatters_rcvd_messages`  
   - Handles user/group lifecycle and message routing  
  
2. **Chatter** (`rti_chatter/chatter.py`): DDS publish-subscribe abstraction layer   
   - Encapsulates DDS DataReader and DataWriter  
   - Manages group membership and message filtering  
  
3. **ChatShell** (`utils/cmd_shell.py`): Interactive command-line interface   
   - Provides user-facing commands for all operations  
   - Uses `cmd.Cmd` for command processing  
  
4. **QoS Configuration** (`USER_QOS_PROFILES.xml`): DDS behavior policies<cite />  
   - Reliable delivery, transient local durability, keep-all history  
  
### Data Model
  
Three IDL-defined structures enable distributed communication:  
  
- **Message**: `msg_id`, `sender_id`, `group_id`, `msg`<cite />  
- **Member**: `user_id`, `user_name`, `participating_groups_id`  
- **Group**: `group_id`, `group_name`, `participating_chatters_id`<cite />  
  
## Installation
  
### Prerequisites
  
- Python 3.x  
- RTI Connext DDS 7.5.0
- uv installed
  To install uv on your device run the following:
  ```bash
    pip install uv
  ``` 
  
  
### Setup
  
1. Clone the repository  
2. Install dependencies using uv:
   ```bash
     uv sync
   ```
4. Configure environment variables in `.env`:  
   ```  
   TIME_SLEEP=0.3  # Message polling interval in seconds
   RTI_LICENSE_FILE= <Path to rti_license.dat>
   RTI_NC_LICENSE_ACCEPTED= yes  
   ``` 
  
## Usage
  
### Command-Line Interface
  
Run the CLI application:  
```bash  
uv run python -m main  
```
  
#### Available Commands  
  
- `create_user <user_name>`: Create a new user and start message polling   
- `create_group <group_name>`: Create a new group   
- `add_user_to_group <user_id> <group_id>`: Add user to group    
- `send_message <group_id> <user_id> <msg>`: Send a message<cite />  
- `list_users`: Display all users   
- `list_groups`: Display all groups    
- `get_groups <user_id>`: Show user's groups   
- `get_users <group_id>`: Show group's members 
- `help`: Display command reference<cite />  
  
#### Example Workflow  
  
```bash  
> create_user "Alice"  
USER Alice CREATED SUCCESSFULLY WITH ID: abc-123-def  
  
> create_user "Bob"  
USER Bob CREATED SUCCESSFULLY WITH ID: xyz-789-uvw  
  
> create_group "Team Chat"  
GROUP Team Chat CREATED SUCCESSFULLY WITH ID: group-456  
  
> add_user_to_group abc-123-def group-456  
USER WITH ID abc-123-def ADDED TO GROUP WITH ID group-456 SUCCESSFULLY.  
  
> send_message group-456 abc-123-def "Hello everyone!"  
```  
  
### Graphical User Interface
  
Run the GUI application:  
```bash  
uv run python -m main_ui  
```
  
The GUI provides a two-panel design with management features on the left and chat functionality on the right.<cite />  
  
## Message Flow
  
1. **User Creation**: Creates `Chatter` instance with DDS DataReader/Writer 
2. **Background Polling**: Daemon thread continuously polls for messages every `TIME_SLEEP` seconds  
3. **Message Send**: Creates `Message` with UUID and publishes via DDS writer
4. **Message Receive**: Filters messages by validity, sender, and group membership 
  
## Distributed Deployment
  
The system supports multiple application instances running simultaneously on different machines or processes. All instances communicate through DDS Domain 0 using the shared `MessageTopic`. [1](#0-0)  No central server or coordinator is required - DDS middleware handles discovery and message routing automatically.<cite />  
  
## Configuration
  
### Environment Variables 
  
- `TIME_SLEEP`: Polling interval in seconds (default: 0.3)
- `RTI_LICENSE_FILE`: Path to rti_license.dat file
- `RTI_NC_LICENSE_ACCEPTED`: Set it to "yes"
  
### QoS Policies
  
The `ChatterLibrary` profile defines critical DDS behaviors:  
- **Reliability**: `RELIABLE_RELIABILITY_QOS` ensures no message loss<cite />  
- **Durability**: `TRANSIENT_LOCAL_DURABILITY_QOS` keeps data for late joiners<cite />  
- **History**: `KEEP_ALL_HISTORY_QOS` maintains all unread messages<cite />  
- **Resource Limits**: 100 samples per instance, 10 instances maximum<cite />  
  
## Project Structure
  
```  
.  
├── app/  
│   └── app_context.py          # Central application coordinator  
├── rti_chatter/  
│   └── chatter.py              # DDS communication wrapper  
├── utils/  
│   └── cmd_shell.py            # CLI interface  
├── main.py                     # CLI entry point  
├── main_ui.py                  # GUI entry point  
├── USER_QOS_PROFILES.xml       # DDS QoS configuration  
└── idl_structs.py              # Generated IDL structures  
```  

  

