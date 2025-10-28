# type: ignore
from telebot import types as tl
from telebot.types import CallbackQuery as call
import telebot, os, time, logging



from classes.MessagesHandler import Main as m
from classes.SettingsClass import Main as s

token1 = int(input('First part of the token >> '))
token2 = input('Second part of the token >> ')

# i couldnt be bothered to make .env file
# so i have to go along with this. I dont mind though.
bot = telebot.TeleBot(token=f'{token1}:{token2}')
log = logging.Logger(__name__)

Settings = s()
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