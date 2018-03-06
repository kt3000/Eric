#coding:utf8

import jieba
import jieba.posseg as pseg


def jieba_initialize(dic_path=""):
    # Initialize Jieba Segment
    if dic_path != "":
        jieba.load_userdict(dic_path)
    jieba.initialize()


def pos_tag(text):
    # Return each POS of word in text
    return pseg.cut(text)


def word_segment(text):
    text = text.strip()
    seg_list = jieba.cut(text)
    result = " ".join(seg_list)
    return result


def check_input_message(text):
    if len(text) > 60:
        return "句子长度过长"
    elif text == "":
        return "无"
    else:
        return text
