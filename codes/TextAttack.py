# -*- coding: utf-8 -*-

import synonyms
from translate import Translator
import imports
import string
from nltk.corpus import wordnet
# '''
# 对抗问题生成实现方法：
# 1.随机加入语气词/标点符号/单个字母模拟打字错误---字符级
# 2.同义词替换---词语级
# 3.回译---语义级
# 支持中文，英文
# '''

cntyperror = ['嗯', '啊', '哎','了', '哦', '呃', '呐', '咳', '额', '嘛','唉', '哇']

punctuations = ['!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/', ':',
               ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`', '{', '|', '}', '~']

entyperror = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

ennoise = entyperror + punctuations
cnnoise = cntyperror + punctuations

# 中文近义词工具包
# cite:
# @online{Synonyms:hain2017,
#   author = {Hai Liang Wang, Hu Ying Xi},
#   title = {中文近义词工具包Synonyms},
#   year = 2017,
#   url = {https://github.com/chatopera/Synonyms},
#   urldate = {2017-09-27}
# }
def synonyms_cn(word):
    result = synonyms.nearby(word)[0]
    print(result)
    if len(result) == 0:
        return word
    else:
        return result[0] if len(result) == 1 else result[1]

def synonyms_en(word):
    synonyms = set()
    for syn in wordnet.synsets(word):
        print(syn)
        for lemma in syn.lemmas():
            print(lemma)
            if not imports.re.search(r'_', lemma.name()):
                synonyms.add(lemma.name())
    return list(synonyms)

def char_noise(sentence, lang):
    if lang == 'cn':
        words = list(imports.jieba.cut(sentence))
    elif lang == 'en':
        words = sentence.split()
    num_words = len(words)
    num = 2 if num_words < 15 else int(num_words/10)
    indices = imports.random.sample(range(num_words), min(num, num_words))
    if lang == 'cn':
        for index in sorted(indices, reverse=True):
            words.insert(index, imports.random.choice(cnnoise))
            return ''.join(words), len(indices)
    elif lang == 'en':
        for index in sorted(indices, reverse=True):
            words.insert(index, imports.random.choice(ennoise))
            return ' '.join(words), len(indices)


def word_noise(sentence,lang):
    if lang == 'cn':
        words = list(imports.jieba.cut(sentence))
    elif lang == 'en':
        words = sentence.split()
    num_words = len(words)

    num = 2 if num_words < 15 else int(num_words/10)
    indices = imports.random.sample(range(num_words), min(num, num_words))

    changewords = {}
    if lang == 'cn':
        for index in sorted(indices, reverse=True):
            synword = synonyms_cn(words[index])
            changewords[words[index]] = synword
            words[index] = synword
        return ''.join(words),  len(indices), changewords
    elif lang == 'en':
        for index in sorted(indices, reverse=True):
            changed_word = words[index].rstrip(string.punctuation)
            changed_word = changed_word.lower()
            synonymss = synonyms_en(changed_word)
            if synonymss:
                changewords[words[index]] = synonymss[0]
                print(words[index],synonymss[0])
                words[index] = synonymss[0]
            else:
                changewords[words[index]] = words[index]
                words[index] = words[index]

        return ' '.join(words), len(indices), changewords

# 基于google translation api
# 使用限额：任何人--5000 char/天
# 限额说明：https://mymemory.translated.net/doc/usagelimits.php
#


def transback_noise(sentences, lang):
    trans = []
    translator1 = Translator(from_lang="zh", to_lang="en")
    translator2 = Translator(from_lang="en", to_lang="zh")
    if lang == 'cn':
        for sentence in sentences:
            translation1 = translator1.translate(sentence)
            tran = translator2.translate(translation1)
            trans.append(tran)
    elif lang == 'en':
        for sentence in sentences:
            translation2 = translator2.translate(sentence)
            tran = translator1.translate(translation2)
            trans.append(tran)
    return trans

# a = word_noise("甲乙两辆汽车同时从同一地点向相反的方向行驶，4小时后两车相距300千米，已知甲车每小时行40千米，乙车每小时行多少千米？",lang='cn')
# print(a)
# 输入：问题列表，攻击模式
# 输出：攻击后的问题列表,攻击次数列表和替换词对列表（如果有的话）
def attack(sentences, mode):
    result = []
    attack_num = []
    changelist = []
    for c in sentences[0]:
        if '\u4e00' <= c <= '\u9fff':
            lang = 'cn'
            break
        elif 'a' <= c.lower() <= 'z':
            lang = 'en'
            break
    if mode == 'character':
        for sentence in sentences:
            temp1, temp2 = char_noise(sentence, lang)
            result.append(temp1)
            attack_num.append(temp2)
    elif mode == 'word':
        for sentence in sentences:
            temp1, temp2, temp3 = word_noise(sentence,lang)
            result.append(temp1)
            attack_num.append(temp2)
            changelist.append(temp3)
    elif mode == 'sentence':
        result = transback_noise(sentences,lang)

    return result, attack_num if len(attack_num) > 0 else None , changelist if len(changelist)> 0 else None

# temp = attack_cn(["甲乙两辆汽车同时从同一地点向相反的方向行驶，4小时后两车相距300千米，已知甲车每小时行40千米，"], "sentence")
# print(temp)

