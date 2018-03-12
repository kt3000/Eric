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


def get_noun(query):
    keywords = []
    words = pos_tag(query)
    for k in words:
        if k.flag.__contains__("n"):
            keywords.append(k.word)
    return keywords


def check_input_message(text):
    text = text.strip()
    if text == "":
        return "无"
    else:
        return text


def decode_text_utf8(text):
    return text.decode('utf8')

