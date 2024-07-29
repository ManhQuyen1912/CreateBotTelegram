import os 
import telebot
from dotenv import load_dotenv, dotenv_values 
from utility import get_daily_horoscope
# loading variables from .env file
load_dotenv() 
 
# accessing and printing value
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot= telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start','hello'])
def send_welcome(message):
    bot.reply_to(message,"Hi, how r u doing?")

@bot.message_handler(commands=['horoscope'])
def sign_handler(message):
    text = "What's your Zodiac Sign?\nChoose one: *Aries*, *Taurus*, *Gemini*, *Cancer*, *Leo*, *Virgo*, *Libra*, *Scorpion*, *Sagittarius*, *Capricorn*, *Aquarius*, and *Pisces*."
    send_msg = bot.send_message(
        message.chat.id, text, parse_mode="Markdown")
    bot.register_next_step_handler(
        send_msg, day_handler)

def day_handler(message):
    sign = message.text
    text = "What day do you want to know?\nChoose one: *TODAY*, *TOMORROW*, *YESTERDAY*, or a date in format YYYY-MM-DD."
    sent_msg = bot.send_message(
        message.chat.id, text, parse_mode="Markdown")
    bot.register_next_step_handler(
        sent_msg, fetch_horoscope, sign.capitalize())

def fetch_horoscope(message,sign):
    day = message.text
    horoscope = get_daily_horoscope(sign, day)
    data = horoscope["data"]
    horoscope_message = f'*Horoscope:* {data["horoscope_data"]}\n*Sign:* {sign}\n*Day:* {data["date"]}'
    bot.send_message(message.chat.id, "Here's ur horoscope!")
    bot.send_message(message.chat.id, horoscope_message, parse_mode="Markdown") 

@bot.message_handler(func=lambda msg:True)
def echo_all(message):
    bot.reply_to(message,message.text)

bot.infinity_polling()
