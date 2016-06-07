# -*- coding: utf-8 -*-
from itertools import chain
from gensim import corpora, matutils
from sklearn.ensemble import RandomForestClassifier
import MeCab
import csv
import re
import os
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

mecab = MeCab.Tagger("-Owakati")
file_name = "text.dic"

def tokenize(text):
    '''
    とりあえず形態素解析して名詞だけ取り出す感じにしてる
    '''
    mecab.parse("")
    node = mecab.parseToNode(text)
    while node:
        part = node.feature.split(',')[0]
        if part == '名詞' or part == '動詞':
            yield node.surface.lower()
        node = node.next

def check_stopwords(word):
    '''
    ストップワードだったらTrueを返す
    '''
    if re.search(r'^[0-9]+$', word):  # 数字だけ
        return True
    if re.search(r'^の$', word):
        return True

    return False

if __name__ == '__main__':

    with open("test.csv", mode="r", encoding="utf-8") as fr:
        word_wrap = {}
        for row in fr:
            label, word = row.split(',')
            if not label in word_wrap:
                word_wrap[label] = []
            word_wrap[label].append([token for token in tokenize(word) if not check_stopwords(token)])

        if not os.path.exists(file_name):
            dic = corpora.Dictionary(list(chain.from_iterable(list(word_wrap.values()))))
            dic.save_as_text(file_name)
        else:
            dic = corpora.Dictionary.load_from_text(file_name)

    # 特徴抽出
    data_train = []
    label_train = []
    for label, words in word_wrap.items():
        for word in words:
            tmp = dic.doc2bow(word)
            data_train.append(list(matutils.corpus2dense([tmp], num_terms=len(dic)).T[0]))
            label_train.append(label)

    # 学習
    estimator = RandomForestClassifier()
    estimator.fit(data_train, label_train)

    while True:
        print("ワードを入力してください")
        input_word = input("> ")
        if input_word == "quit":
            break
        else:
            w = [token for token in tokenize(input_word) if not check_stopwords(token)]
            t = dic.doc2bow(w)
            d = [list(matutils.corpus2dense([t], num_terms=len(dic)).T[0])]
            print(estimator.predict_proba(d), estimator.predict(d))
            # print(t)
            # print(list(matutils.corpus2dense([t], num_terms=len(dic)).T[0]))
