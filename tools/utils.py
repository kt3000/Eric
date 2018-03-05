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

