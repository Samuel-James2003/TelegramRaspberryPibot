# Telegram Cohere Chatbot

This project is a Telegram bot integrated with Cohere's AI language models to manage chats, simulate user personalities, and facilitate efficient conversation management. The bot also includes admin control and custom chat history handling.

## Features

- **Start Command**: Greet users and initialize admin setup if not already done.
- **Admin Control**: Add/remove admin IDs and control permissions for chats.
- **Chat Management**: Add/remove chat IDs for approved interactions.
- **AI-Powered Responses**: Use Cohere's AI to generate responses that mimic the bot owner's personality.
- **History Handling**: Maintain chat history for context-aware replies.
- **Permissions Verification**: Validate user and chat permissions before processing commands.

## Setup

### Prerequisites

1. **Python 3.10 or higher**
2. **Cohere API Key**
3. **Telegram Bot Token**

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   - `COHERE_TOKEN`: Your Cohere API key
   - `BOT_TOKEN`: Your Telegram bot token

4. Create necessary directories and files:
   ```bash
   mkdir -p files
   touch files/admin.txt files/chat.txt files/user.txt
   ```

### Run the Bot

Execute the main script to start the bot:
```bash
python bot.py
```

## Commands

### Public Commands

- `/start`:
  - Greets the user and initializes the bot.
  - If no admins exist, the first user becomes the admin.

### Admin Commands

- `/addadmin <id>`:
  - Adds a new admin ID.
  - Example: `/addadmin 123456789`

- `/addchat <id>`:
  - Adds a new chat ID to the approved list.
  - Example: `/addchat -987654321`

### General Behavior

- **Message Handling**:
  - Direct and forwarded messages are processed.
  - Responses are AI-generated based on chat history and context.

## Code Structure

### Main Functions

- `start`: Handles the `/start` command.
- `addAdmin`: Adds a new admin.
- `addChat`: Adds a new chat.
- `handle_message`: Processes messages and generates AI-powered responses.

### Helper Functions

- `WriteChats`, `GetChats`: Manage chat list storage.
- `WriteAdmins`, `GetAdmins`: Manage admin list storage.
- `read_list_from_file`, `write_list_to_file`: Handle file-based storage.
- `verify_permissions`: Validate user permissions.
- `add_chat_history`: Maintain and update chat history.

## Files and Directories

- **`files/`**: Directory for storing admin, chat, and user lists, as well as chat histories.
  - `admin.txt`: List of admin IDs.
  - `chat.txt`: List of approved chat IDs.
  - `user.txt`: (Optional) List of registered user IDs.

## Dependencies

- `python-telegram-bot`
- `cohere`

## Notes

- Ensure all required environment variables are correctly configured before running the bot.
- Only users with admin permissions can add new admins or chats.
- Chat history is limited to the last 3 messages for context awareness.

## Author

Samuel JAMES
