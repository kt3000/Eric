# coding:utf8

from wxpy import *
import utils


def start():
    embed()


def build_group_bot(group_name):
    bot = Bot(cache_path=True)
    bot.enable_puid()
    group = ensure_one(bot.groups(update=True).search(group_name))
    print group

    # The first matching function is registered at last,
    # and only one registration function is matched.
    register_print(bot)
    register_repeat(bot, group)
    welcome(group)


def welcome(group):
    pass
    group.send(utils.decode_text_utf8(" "))


def register_print(bot):
    @bot.register()
    def just_print(msg):
        print(msg)


def register_repeat(bot, group):
    @bot.register(group, TEXT)
    def auto_reply(msg):
        # TODO(mickey.zhou add service)
        return "Return" + msg.text


if __name__ == '__main__':
    build_group_bot(utils.decode_text_utf8("缺西"))
    start()
