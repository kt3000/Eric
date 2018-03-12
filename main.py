# coding:utf8

import tools.utils as utils
import bot.bot as bot
import tools.aiml_bot as aimlBot


def initialize():
    # initialize service
    utils.jieba_initialize()


if __name__ == '__main__':
    initialize()
    aimlbot = aimlBot.AIMLBot()
    chat_bot = bot.Bot(aimlbot)
    chat_bot.start()