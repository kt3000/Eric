# coding:utf8

import tools.utils as utils


class Bot:
    def __init__(self, bot):
        self.bot = bot

    def start(self):
        self.bot.start()
        # start chat bot service in command line
        while True:
            input_message = raw_input("Enter your message >> ")
            print self.process_chat(input_message)

    def process_chat(self, msg):
        checked_result = utils.check_input_message(msg)
        if checked_result == "无":
            return self.bot.process_chat(checked_result)
        word_segment = utils.word_segment(checked_result)
        return self.bot.process_chat(word_segment)
