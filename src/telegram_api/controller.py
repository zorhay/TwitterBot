import telebot
from src.telegram_api.config import Configuration
from src.poebot.poems.PoemBase import PoemBase

bot = telebot.TeleBot(Configuration.token)


@bot.message_handler(commands=["start"])
def start_message(message):
    bot.send_message(message.chat.id, "Hi! I am a poet bot.\n"
                                      "Press /poetry if you want to see verse.")


@bot.message_handler(commands=["poetry"])
def start_message(message):
    poem = PoemBase()
    poem.word_rand_generate(structure=[(9, 2), (8, 3), (9, 0), (8, 1)])
    poem.word_rand_generate(structure=[(9, 2), (8, 3), (9, 0), (8, 1)])

    bot.send_message(message.chat.id, poem.to_print())


if __name__ == "__main__":
    bot.polling()
