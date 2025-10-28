# type: ignore
from telebot import types as tl
from telebot.types import CallbackQuery as call
import telebot, os, logging
from dotenv import load_dotenv

from classes.Messages import Main as m

load_dotenv()

BOT_TOKEN = os.getenv('TKN')

# i couldnt be bothered to make .env file
# so i have to go along with this. I dont mind though.
bot = telebot.TeleBot(token=BOT_TOKEN)
log = logging.Logger(__name__)

Messages = m(bot)

@bot.message_handler(commands=['start','settings'])
def responseToCommands(message:tl.Message):
    spl = message.text.lower().split(None)

    # for the love of FUCKING god
     # STOP. forgetting. that it starts from 0 index,
      # NOT ONEEE.
    print(spl)
    if spl[0] == '/start':
        success, result = Messages.startMessage(message)
        if not success:
            log.error(result)
    elif spl[0] == '/settings':
        success, result = Messages.settingsMessage(message)
        if not success:
            log.error(result)
    
@bot.callback_query_handler(func=lambda call: call.data in {"lang", "notif", "advanced", "help", "about"})
def responseToCallback(call:call):
    bot.answer_callback_query(call.id)
    print(call.data)

if __name__=='__main__':
    bot.polling(non_stop=True)