from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import cohere
import os


API_KEY=os.getenv('COHERE_TOKEN')
BOT_TOKEN = os.getenv('BOT_TOKEN')
co = cohere.ClientV2(API_KEY)

# Function to handle the /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if len(GetAdmins()) == 0:
        WriteAdmins([str(user.id)])
        welcome_message = f"Greetings samuel. You have successfully initialized the bot"
    else:    
        welcome_message = f"Hello, {user.first_name}! Welcome to Lou's bot. 😊\nHow can I assist you today?"
    await context.bot.send_message(chat_id=update.effective_chat.id, text=welcome_message)
    
async def addChat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if not verify_permissions(f"{user.id}", "admin"):
        await context.bot.send_message(chat_id=user.id, text="Current user does not have sufficent permissions.")
        return
    newID = update.message.text.lower().replace("/addchat","").strip()
    if not isAnInt(newID):
        await context.bot.send_message(chat_id=user.id, text=f"{newID} is not a valid ID.")
        return
    chats = GetChats()
    if newID in chats:
        await context.bot.send_message(chat_id=user.id, text=f"{newID} is already in the chat list.")
        return
    chats.append(newID)
    WriteChats(chats)
    confirm_message = f"Chat added: {newID}"
    await context.bot.send_message(chat_id=update.effective_chat.id, text=confirm_message)
    return

def WriteChats(chats: list[str]):
    write_list_to_file(os.path.curdir + "/files/chat.txt", chats)

def GetChats():
    return read_list_from_file(os.path.curdir + "/files/chat.txt")

async def addAdmin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    userID = update.effective_user.id
    if not verify_permissions(userID, "admin"):
        await context.bot.send_message(chat_id=userID, text="Current user does not have sufficent permissions.")
        return
    newID = update.message.text.lower().replace("/addadmin","").strip()
    if not isAnInt(newID):
        await context.bot.send_message(chat_id=userID, text=f"{newID} is not a valid ID.")
        return
    admins = GetAdmins()
    if newID in admins:
        await context.bot.send_message(chat_id=userID, text=f"{newID} is already an admin.")
        return
    admins.append(newID)
    WriteAdmins(admins)   
    confirm_message = f"ID: {newID} added to the admin list."
    await context.bot.send_message(chat_id=userID, text=confirm_message)
    return

def WriteAdmins(admins):
    write_list_to_file(os.path.curdir + "/files/admin.txt",admins)

def GetAdmins():
    return read_list_from_file(os.path.curdir + "/files/admin.txt")

def isAnInt(value):
    try:
        int(value)
        return True
    except ValueError:
        return False

def read_list_from_file(file_path: str):
    """
    Reads a list of items from a file. Each line in the file is treated as one item in the list.
    
    :param file_path: Path to the file to read.
    :return: A list of items read from the file.
    """
    try:
        # Ensure the directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        with open(file_path, 'r', encoding='utf-8') as file:
            # Strip whitespace/newlines and return as a list
            return [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        # If the file doesn't exist, create it and return an empty list
        with open(file_path, 'a', encoding='utf-8') as file:
            pass
        return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

def write_list_to_file(file_path:str, items:list):
    """
    Writes a list of items to a file. Each item in the list is written on a new line.
    
    :param file_path: Path to the file to write.
    :param items: List of items to write to the file.
    """
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            for item in items:
                file.write(f"{item}\n")
        file.close()
        return True
    except FileNotFoundError:
        with open(file_path, 'a', encoding='utf-8') as file:
            for item in items:
                file.write(f"{item}\n")
        file.close()
        return True
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

def verify_permissions(ID:str, level:str):
    """
    Verify if the given user ID has the required permissions to execute the given level.
    
    :param ID: User ID to verify.
    :param level: Permission level to verify.
    :return: True if the user has the required permissions, False otherwise.
    """
    ID = str(ID)
    if level == "admin":
        return ID in GetAdmins()
    elif level == "user":
        return ID in GetUsers()
    elif level == "chat":
        return ID in GetChats()

def GetUsers():
    return read_list_from_file(os.path.curdir + "/files/user.txt")
# Function to handle any random message
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.business_message is not None and update.business_message.text is not None:
        # Get the business message
        if verify_permissions(update.business_message.chat_id, "chat"):
            #the chat is in the list of allowed chats
            if update.business_message.from_user.id == update.business_message.chat_id:
                #the user is not the sender
                message_string = "\n".join(read_list_from_file(f"{os.path.curdir}/files/{update.business_message.chat_id}.txt"))
                message_string += (f"\n{update.business_message.text} - {update.business_message.date} - {update.business_message.from_user.username}")
                res = co.chat(
                    model="command-r7b-12-2024",
                    messages=[
                        {
                            "role" : "system",
                            "content" : "You are a Telegram bot responding to messages on my behalf. You will receive the last three messages in a conversation. Only reply to questions that neither you (as the assistant) nor I (LouTheWolf) have previously answered. If asked how you are, respond with 'positively.' Always reply as if you are me, a human being."},
                        {
                            "role" : "user",
                            "content" : message_string
                            }])
                response_message = res.message.content[0].text
                await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=response_message, 
                    business_connection_id=update.business_message.business_connection_id)
                add_chat_history(update,response_message)
                return
            else:
                #the user is the sender
                add_chat_history(update)
                return
        else:
            #the user is not (yet) allowed
            await context.bot.send_message(chat_id=GetAdmins()[0], text=f"The current chat is not initialized. Please add the following ID to your list of approved IDs ```{update.business_message.chat_id}```")
            return
    if update.message is not None and update.message.text is not None:
        # A direct message to the bot 
        if update.message.forward_origin is not None:
            #Its a forwarded message
            await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Hi, I see you forwarded this from @{update.message.forward_origin.sender_user.username} - ```{update.message.forward_origin.sender_user.id}```")
            return

import os

def add_chat_history(update, botresponse:str=None):
    file_path = f"{os.path.curdir}/files/{update.business_message.chat_id}.txt"
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    try:
        # Read chat history
        chatHistory = read_list_from_file(file_path)
    except FileNotFoundError:
        chatHistory = []
    
    # Update chat history
    chatHistory.append(update.business_message.text.strip().replace("\n","") + f" - {update.business_message.date} - {update.business_message.from_user.username}")
    if botresponse is not None:
        chatHistory.append(f"{botresponse.strip().replace('\n','')} - {update.business_message.date} - assistant")
    
    # Limit to last 3 messages
    chatHistory = chatHistory[-3:]
    
    # Write updated history back to file
    write_list_to_file(file_path, chatHistory)

    
def main():
    # Create the application with your bot's token
    app = Application.builder().token(BOT_TOKEN).build()

    # Add a CommandHandler for the /start command
    app.add_handler(CommandHandler("start", start))
    
    # Add a CommandHandler for the /addUser command
    app.add_handler(CommandHandler("addchat", addChat))
    
    # Add a CommandHandler for the /addAdmin command
    app.add_handler(CommandHandler("addadmin", addAdmin))
    
    # Add a MessageHandler for handling any  message
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Run the bot
    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()

