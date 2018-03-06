# coding:utf8

import tools.utils as utils
import aiml
import bot.bot as bot


def start(chat_bot):
    # start chat bot service in command line
    while True:
        input_message = raw_input("Enter your message >> ")
        check_result = utils.check_input_message(input_message)
        bot.process_chat(check_result)


def initialize():
    # initialize service
    utils.jieba_initialize()
    chat_bot = aiml.Kernel()
    # TODO(mickey.zhou add learn file for bot)
    return chat_bot


if __name__ == '__main__':
    bot = initialize()
    start(bot)
