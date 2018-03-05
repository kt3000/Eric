# coding:utf8

import tools.utils as utils
import aiml


def start(chat_bot):
    # start chat bot service in command line
    while True:
        input_message = raw_input("Enter your message >> ")


def initialize():
    # initialize service
    utils.jieba_initialize()
    chat_bot = aiml.Kernel()
    # TODO(mickey.zhou add learn file for bot)
    return chat_bot


if __name__ == '__main__':
    bot = initialize()
    start(bot)
