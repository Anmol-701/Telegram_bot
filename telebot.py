import logging
from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv
import os
import openai
import sys

class Reference:
    '''
    A class to store previously response from the chatGPT API
    '''
    def __init__(self) -> None:
        self.response = ""

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

reference = Reference()

# Telegram Bot Token
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Model name
MODEL_NAME = "gpt-3.5-turbo"

# Initialize bot and dispatcher
bot = Bot(token=TOKEN)
dispatcher = Dispatcher(bot)

def clear_past():
    """A function to clear the previous conversation and context."""
    reference.response = ""

@dispatcher.message_handler(commands=['start'])
async def welcome(message: types.Message):
    """
    This handler receives messages with `/start` command
    """
    await message.reply("Hi\nI am Telegram Bot! Created by Anmol Rana. How can I assist you?")

@dispatcher.message_handler(commands=['clear'])
async def clear(message: types.Message):
    """
    A handler to clear the previous conversation and context.
    """
    clear_past()
    await message.reply("I've cleared the past conversation and context.")

@dispatcher.message_handler(commands=['help'])
async def helper(message: types.Message):
    """
    A handler to display the help menu.
    """
    help_command = """
    Hi There, I'm chatGPT Telegram bot created by Anmol Rana! Please follow these commands:
    /start - to start the conversation
    /clear - to clear the past conversation and context.
    /help - to get this help menu.
    I hope this helps. :)
    """
    await message.reply(help_command)

@dispatcher.message_handler()
async def chatgpt(message: types.Message):
    """
    A handler to process the user's input and generate a response using the chatGPT API.
    """
    print(f">>> USER: \n\t{message.text}")

    # Prepare messages for OpenAI API
    messages = [
        {"role": "assistant", "content": reference.response},  # Previous response from the assistant (if any)
        {"role": "user", "content": message.text}  # User's input
    ]

    # Make the API call (async handling)
    response = await openai.ChatCompletion.acreate(
        model=MODEL_NAME,
        messages=messages
    )

    # Extract response content
    bot_reply = response.choices[0].message['content']

    # Store response for future references
    reference.response = bot_reply

    print(f">>> chatGPT: \n\t{bot_reply}")

    # Send reply to the user
    await bot.send_message(chat_id=message.chat.id, text=bot_reply)

if __name__ == "__main__":
    executor.start_polling(dispatcher, skip_updates=False)
