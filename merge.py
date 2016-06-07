# -*- coding: utf-8 -*-
import re
import sys
import io
import csv
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

files = {"hatena":"hatena_keywords.csv", "wiki":"jawiki-latest-all-titles-in-ns0"}

def input_check(text):
    return not (re.match(r"^[+-.$()?*/&%!\"'_,]+/", text) or re.match(r"^[-.0-9]+$", text) or \
    re.match(r"曖昧さ回避", text) or re.match(r"_\(", text) or re.match(r"^PJ:", text) or \
    re.match(r"の登場人物", text) or re.match(r"一覧", text) or re.match(r"^page_title$", text))

def convert():
    with open("dic.csv", "w") as fw:
        writer = csv.writer(fw)
        for k, f in files.items():
            with open(f, "r") as fr:
                for text in fr:

                    if k == "hatena":
                        text = text.split('\t')[1]

                    text = text.strip()
                    if not input_check(text):
                        continue;

                    noun_len = len(text)

                    if noun_len > 3:
                        score = int(max([-36000.0, -400 * (noun_len ** 1.5)]))
                        writer.writerow([text, None, None, score, '名詞', '一般', '*', '*', '*', '*', text, '*', '*', k])

if __name__ == "__main__":
    convert()
