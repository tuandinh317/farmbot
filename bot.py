import telebot
from config import BOT_TOKEN
import os

bot = telebot.TeleBot(BOT_TOKEN)

from commands import start, farm, plant, harvest, invite

start.register(bot)
farm.register(bot)
plant.register(bot)
harvest.register(bot)
invite.register(bot)



if __name__ == "__main__":
    print("Bot đang chạy...")
    bot.infinity_polling()