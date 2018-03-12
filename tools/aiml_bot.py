# coding:utf8

import aiml
import os
import tools.web as web


class AIMLBot:
    aiml_bot = aiml.Kernel()

    def __init__(self):
        self.webParser = web.WebParser()

    def start(self):
        resources_path = os.path.join(os.path.abspath('.'), "resources")

        # TODO(mickey.zhou refactor follow code as use std-startup.xml)
        self.aiml_bot.learn(os.path.join(resources_path, "bye.aiml"))
        self.aiml_bot.learn(os.path.join(resources_path, "tools.aiml"))
        self.aiml_bot.learn(os.path.join(resources_path, "bad.aiml"))
        self.aiml_bot.learn(os.path.join(resources_path, "funny.aiml"))
        self.aiml_bot.learn(os.path.join(resources_path, "OrdinaryQuestion.aiml"))
        self.aiml_bot.learn(os.path.join(resources_path, "Common conversation.aiml"))

    @staticmethod
    def reply(msg):
        return 'Eric:' + msg

    def process_chat(self, msg):
        aiml_resp = self.aiml_bot.respond(msg)
        if aiml_resp == "":
            return self.reply('找不到答案')
        elif aiml_resp[0] == '#':

            return self.reply(self.webParser.web_process(aiml_resp, msg, self.aiml_bot))
        else:
            return aiml_resp



