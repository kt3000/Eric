# coding:utf8

import tools.utils as utils
import tools.aiml_bot as aiml


def start(chat_bot):
    # start chat bot service in command line
    while True:
        input_message = raw_input("Enter your message >> ")
        checked_result = utils.check_input_message(input_message)
        print chat_bot.process_chat(checked_result)


def initialize():
    # initialize service
    utils.jieba_initialize()
    bot = aiml.AIMLBot()
    bot.start()
    return bot


if __name__ == '__main__':
    bot = initialize()
    start(bot)
