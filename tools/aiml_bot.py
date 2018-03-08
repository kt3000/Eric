# coding:utf8

import aiml
import os


def start():
    aiml_bot = aiml.Kernel()
    # TODO(mickey.zhou refactor follow code as For loop)
    aiml_bot.learn(os.path.split(os.path.realpath(__file__))[0] + "/resources/std-startup.xml")
    aiml_bot.learn(os.path.split(os.path.realpath(__file__))[0] + "/resources/bye.aiml")
    aiml_bot.learn(os.path.split(os.path.realpath(__file__))[0] + "/resources/tools.aiml")
    aiml_bot.learn(os.path.split(os.path.realpath(__file__))[0] + "/resources/bad.aiml")
    aiml_bot.learn(os.path.split(os.path.realpath(__file__))[0] + "/resources/funny.aiml")
    aiml_bot.learn(os.path.split(os.path.realpath(__file__))[0] + "/resources/OrdinaryQuestion.aiml")
    aiml_bot.learn(os.path.split(os.path.realpath(__file__))[0] + "/resources/Common conversation.aiml")
    return aiml_bot
