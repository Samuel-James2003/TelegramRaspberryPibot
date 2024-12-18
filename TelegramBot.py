from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import cohere
import os


api_key=os.getenv('COHERE_TOKEN')
co = cohere.ClientV2(api_key)
BOT_TOKEN = os.getenv('BOT_TOKEN')

# Function to handle the /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    welcome_message = f"Hello, {user.first_name}! Welcome to Lou's bot. 😊\nHow can I assist you today?"
    await context.bot.send_message(chat_id=update.effective_chat.id, text=welcome_message)

# Function to handle any random message
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.business_message.text
    res = co.chat(
        model="command-r7b-12-2024",
        messages=[
            {
                "role" : "system",
                "content" : "You are a Telegram bot that replies to messages on my behalf. The following message will be something a user sent me. If you are asked how you are just reply with positively and ask them the same. You must reply as if you are me"
            },
            {
                "role" : "user",
                "content" : user_message
            }
            ])
  
    response_message = res.message.content[0].text
    await context.bot.send_message(chat_id=update.effective_chat.id, text=response_message, business_connection_id=update.business_message.business_connection_id)

def main():
    # Create the application with your bot's token
    app = Application.builder().token(BOT_TOKEN).build()

    # Add a CommandHandler for the /start command
    app.add_handler(CommandHandler("start", start))
    
    # Add a MessageHandler for handling any random message
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Run the bot
    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
