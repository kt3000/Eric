#coding:utf8


def load_baike_attr_name(attr_dic):
    fr = open(attr_dic, 'r')
    attrs = []
    line = fr.readline()
    while line:
        attrs.append(line.strip())
        line = fr.readline()
    fr.close()
    return attrs


def load_synonyms_word_in_attr(word, synsdic, attr):
    fr = open(synsdic, 'r')
    tar_word = ''
    line = fr.readline().strip()
    while line:
        words = line.split(" ")
        if word in words:
            for w in words:
                if w in attr:
                    tar_word = w
                    break
        if tar_word != '':
            break
        line = fr.readline()
    fr.close()
    if tar_word == '':
        tar_word = 'Empty'
    return tar_word