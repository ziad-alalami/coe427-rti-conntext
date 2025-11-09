# Contributing to DDS Chat System  [header-1](#header-1)
  
Thank you for your interest in contributing to the DDS Chat System! This document provides guidelines and instructions for contributing to this distributed chat application built on RTI Connext DDS 7.5.0.  
  
## Table of Contents  [header-2](#header-2)
  
- [Code of Conduct](#code-of-conduct)  
- [Getting Started](#getting-started)  
- [Development Environment Setup](#development-environment-setup)  
- [Project Architecture](#project-architecture)  
- [How to Contribute](#how-to-contribute)  
- [Coding Standards](#coding-standards)  
- [Testing Guidelines](#testing-guidelines)  
- [Pull Request Process](#pull-request-process)  
- [DDS-Specific Considerations](#dds-specific-considerations)  
  
## Code of Conduct  [header-3](#header-3)
  
We are committed to providing a welcoming and inclusive environment for all contributors. Please be respectful and professional in all interactions.  
  
## Getting Started  [header-4](#header-4)
  
Before contributing, please:  
  
1. Read the [README.md](README.md) to understand the project's purpose and architecture  
2. Familiarize yourself with RTI Connext DDS 7.5.0 concepts (publish-subscribe, QoS policies, topics)  
3. Review existing issues and pull requests to avoid duplicate work  
4. Join our community discussions (if applicable)  
  
## Development Environment Setup  [header-5](#header-5)
  
### Prerequisites  [header-6](#header-6)
  
Ensure you have the following installed:  
  
- **Python 3.x** (3.8 or higher recommended)  
- **RTI Connext DDS 7.5.0** with valid license  
- **uv** package manager: `pip install uv`  
- **Git** for version control  
  
### Initial Setup  [header-7](#header-7)
  
1. **Fork and clone the repository**  
   ```bash  
   git clone https://github.com/YOUR_USERNAME/coe427-rti-conntext.git  
   cd coe427-rti-conntext  
   ```  
  
2. **Install dependencies**  
   ```bash  
   uv sync  
   ```  
  
3. **Configure environment variables**  
     
   Create a `.env` file in the project root:  
   ```  
   TIME_SLEEP=0.3  
   RTI_LICENSE_FILE=/path/to/rti_license.dat  
   RTI_NC_LICENSE_ACCEPTED=yes  
   ```  
  
4. **Verify installation**  
   ```bash  
   uv run python -m main  
   ```  
     
   You should see the ChatShell prompt if everything is configured correctly.  
  
## Project Architecture  [header-8](#header-8)
  
Understanding the architecture is crucial for effective contributions:  
  
### Core Components  [header-9](#header-9)
  
- **`app/app_context.py`**: Central state manager coordinating all operations  
- **`rti_chatter/chatter.py`**: DDS abstraction layer handling publish/subscribe  
- **`utils/cmd_shell.py`**: CLI interface using Python's `cmd` module  
- **`USER_QOS_PROFILES.xml`**: DDS Quality of Service configuration  
- **`idl_structs.py`**: Generated IDL data structures (Message, Member, Group)  
  
### Key Design Patterns  [header-10](#header-10)
  
- **Publish-Subscribe**: All communication via DDS `MessageTopic`  
- **Daemon Threading**: Background message polling per user  
- **UUID-based Identity**: Unique identifiers for users, groups, and messages  
- **Application-Level Filtering**: Message filtering in `Chatter.receive_messages()`  
  
## How to Contribute  [header-11](#header-11)
  
### Types of Contributions  [header-12](#header-12)
  
We welcome:  
  
- **Bug fixes**: Resolve issues in message delivery, group management, or UI  
- **Feature enhancements**: New commands, improved filtering, performance optimizations  
- **Documentation**: Code comments, wiki pages, usage examples  
- **Testing**: Unit tests, integration tests, distributed deployment scenarios  
- **QoS improvements**: Better reliability, durability, or resource management  
  
### Finding Work  [header-13](#header-13)
  
- Check the **Issues** tab for open tasks  
- Look for issues labeled `good first issue` or `help wanted`  
- Propose new features by opening an issue first for discussion  
  
## Coding Standards  [header-14](#header-14)
  
### Python Style Guide  [header-15](#header-15)
  
Follow **PEP 8** conventions:  
  
- Use 4 spaces for indentation (no tabs)  
- Maximum line length: 100 characters  
- Use descriptive variable names: `user_id`, `group_name`, not `uid`, `gn`  
- Add docstrings to all classes and methods (see existing code for format)  
  
### Example Docstring Format  [header-16](#header-16)
  
```python  
def send_message(self, group_id: str, msg: str):  
    """  
    Send a message to a specific group.  
      
    Creates a new Message object with a unique ID and publishes it  
    to the DDS network for distribution to group members.  
      
    Args:  
        group_id (str): The ID of the group to send the message to  
        msg (str): The message content to send  
    """  
```  
  
### Naming Conventions  [header-17](#header-17)
  
- **Classes**: `PascalCase` (e.g., `AppContext`, `Chatter`)  
- **Functions/Methods**: `snake_case` (e.g., `create_user`, `send_message`)  
- **Constants**: `UPPER_SNAKE_CASE` (e.g., `TIME_SLEEP`)  
- **Private methods**: Prefix with `_` (e.g., `_validate_user`)  
  
### Import Organization  [header-18](#header-18)
  
Order imports as follows:  
1. Standard library imports  
2. Third-party imports (e.g., `rti.connextdds`)  
3. Local application imports (e.g., `from app import AppContext`)  
  
## Testing Guidelines  [header-19](#header-19)
  
### Manual Testing  [header-20](#header-20)
  
Before submitting a PR, test the following workflows:  
  
1. **User Creation and Messaging**  
   ```bash  
   > create_user "TestUser1"  
   > create_user "TestUser2"  
   > create_group "TestGroup"  
   > add_user_to_group <user1_id> <group_id>  
   > add_user_to_group <user2_id> <group_id>  
   > send_message <group_id> <user1_id> "Test message"  
   ```  
  
2. **Distributed Testing**  
   - Run multiple instances on different terminals/machines  
   - Verify messages propagate across all instances  
   - Test late-joiner scenario (start instance after messages sent)  
  
3. **GUI Testing**  
   ```bash  
   uv run python -m main_ui  
   ```  
   - Test all UI operations match CLI functionality  
   - Verify real-time message updates  
  
### Unit Testing (Future)  [header-21](#header-21)
  
When adding tests:  
- Place test files in a `tests/` directory  
- Name test files `test_*.py`  
- Use `pytest` framework  
- Mock DDS components for isolated testing  
  
## Pull Request Process  [header-22](#header-22)
  
### Before Submitting  [header-23](#header-23)
  
1. **Create a feature branch**  
   ```bash  
   git checkout -b feature/your-feature-name  
   ```  
  
2. **Make your changes**  
   - Write clean, documented code  
   - Follow coding standards  
   - Test thoroughly  
  
3. **Commit with clear messages**  
   ```bash  
   git commit -m "Add feature: brief description  
     
   - Detailed point 1  
   - Detailed point 2"  
   ```  
  
### Submitting the PR  [header-24](#header-24)
  
1. **Push to your fork**  
   ```bash  
   git push origin feature/your-feature-name  
   ```  
  
2. **Open a Pull Request** with:  
   - **Title**: Clear, concise description (e.g., "Fix message filtering bug in Chatter")  
   - **Description**:   
     - What changes were made  
     - Why they were necessary  
     - How to test the changes  
     - Any breaking changes or migration notes  
  
3. **Link related issues**: Use "Fixes #123" or "Relates to #456"  
  
### PR Review Process  [header-25](#header-25)
  
- Maintainers will review within 3-5 business days  
- Address feedback by pushing new commits to the same branch  
- Once approved, maintainers will merge your PR  
  
## DDS-Specific Considerations  [header-26](#header-26)
  
### Working with QoS Policies  [header-27](#header-27)
  
When modifying `USER_QOS_PROFILES.xml`:  
  
- **Reliability**: Keep `RELIABLE_RELIABILITY_QOS` unless you have a specific reason  
- **Durability**: `TRANSIENT_LOCAL_DURABILITY_QOS` enables late-joiner support  
- **History**: `KEEP_ALL_HISTORY_QOS` ensures no message loss  
- **Resource Limits**: Adjust carefully based on expected load  
  
Test QoS changes with:  
- Multiple concurrent users  
- Network interruptions  
- Late-joining participants  
  
### IDL Structure Changes  [header-28](#header-28)
  
If modifying data structures in `idl_structs.py`:  
  
1. Update the IDL definitions  
2. Regenerate Python bindings using RTI Code Generator  
3. Update all code that uses the modified structures  
4. Test backward compatibility if applicable  
  
### DDS Domain and Topic  [header-29](#header-29)
  
- **Domain ID**: Always use `0` for consistency  
- **Topic Name**: Keep `MessageTopic` unless creating new topics  
- **Participant**: Shared module-level instance in `rti_chatter/chatter.py`  
  
### Threading Considerations  [header-30](#header-30)
  
The `loop_messages()` function runs in daemon threads:  
  
- Ensure thread-safe access to shared dictionaries  
- Use appropriate sleep intervals (`TIME_SLEEP`)  
- Handle thread cleanup on application exit  
  
## Common Contribution Areas  [header-31](#header-31)
  
### Adding New Commands  [header-32](#header-32)
  
To add a command to `ChatShell`:  
  
1. Add method in `utils/cmd_shell.py`:  
   ```python  
   @split_args  
   def do_your_command(self, arg1, arg2):  
       """Command description for help."""  
       # Implementation  
   ```  
  
2. Update `do_help()` method with command documentation  
3. Add corresponding logic in `AppContext` if needed  
  
### Improving Message Filtering  [header-33](#header-33)
  
Current filtering is in `rti_chatter/chatter.py:receive_messages()`:  
  
- Consider implementing DDS ContentFilteredTopics for efficiency  
- Add support for message priorities or categories  
- Implement message history limits per user  
  
### Enhancing the GUI  [header-34](#header-34)
  
The GUI in `main_ui.py` uses tkinter:  
  
- Improve layout and responsiveness  
- Add message notifications  
- Implement user presence indicators  
- Add group management UI  
  
## Questions or Issues?  [header-35](#header-35)
  
- **Bug reports**: Open an issue with detailed reproduction steps  
- **Feature requests**: Open an issue describing the use case  
- **Questions**: Use GitHub Discussions or contact maintainers  
  
Thank you for contributing to DDS Chat System!
