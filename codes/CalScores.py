import imports

from collections import Counter
from math import sqrt
from rouge import Rouge
import CnSimilarity

def en2cn_emscore(sentences1, sentences2):
    emscore = []
    for sentence1, sentence2 in zip(sentences1, sentences2):
        if sentence1 == sentence2:
            emscore.append(1)
        else:
            emscore.append(0)
    return emscore

def en2cn_similarity(sentences1, sentences2):

    similarity = 0
    answerlist = CnSimilarity.calculate_similarity(sentences1, sentences2)
    for x in answerlist:
        similarity += x

    return similarity/min(len(sentences1), len(sentences2))

# en2cn_similarity(['你好','这是一条小狗','你说什么'],['你好呀','这是一只小狗'])
def en2cn_rouge(sentences, references):
    rouge = Rouge()
    scores = []
    for sentence, reference in zip(sentences, references):
        sentence = ' '.join(imports.jieba.cut(sentence))
        reference = ' '.join(imports.jieba.cut(reference))
        score = rouge.get_scores(sentence, reference)
        scores.append(score)
    list1 = [item[0]['rouge-1']['f'] for item in scores]
    list2 = [item[0]['rouge-2']['f'] for item in scores]
    listl = [item[0]['rouge-l']['f'] for item in scores]
    return list1, list2, listl

def singlec_precision(answerlist,referencelist):
    iscorrect = []
    rcnt = 0

    if len(referencelist) != len(answerlist):
        raise ValueError("参考答案列表和结果列表长度不一致")

    total = len(referencelist)
    for ref_answer, res_answer in zip(referencelist, answerlist):
        if ref_answer == res_answer:
            iscorrect.append(1)
            rcnt += 1
        else :
            iscorrect.append(0)

    precision = float(rcnt/total)
    return iscorrect, precision

def singlec_similarity(referencelist, answerlist):
    similarity = 0
    for ref_answer, res_answer in zip(referencelist, answerlist):
        if ref_answer == res_answer:
            similarity += 1
    return similarity/min(len(referencelist), len(answerlist))


def multic_f1(answerlist, referencelist):
    f1_scores = []
    precisions = []
    recalls = []
    for ref_ans, res_ans in zip(referencelist, answerlist):
        tp = 0
        fp = 0
        fn = 0
        for r, s in zip(ref_ans, res_ans):
            if r == 1 and s == 1:
                tp += 1
            elif r == 0 and s == 1:
                fp += 1
            elif r == 1 and s == 0:
                fn += 1
            elif r == -1 and s == 1:
                fp += 1
            elif r == 1 and s == -1:
                fn += 1

        if tp + fp == 0 or tp + fn == 0:
            f1_scores.append(0)
            precisions.append(0)
            recalls.append(0)
        else:
            precision = tp / (tp + fp)
            recall = tp / (tp + fn)
            try:
                f1 = 2 * precision * recall / (precision + recall)
            except ZeroDivisionError:
                f1 = 0
            f1_scores.append(f1)
            precisions.append(precision)
            recalls.append(recall)
    return precisions, recalls, f1_scores

def multic_similarity(originanswers, attackedanswers):
    similarities = []
    for oanswer, aanswer in zip(originanswers, attackedanswers):
        scnt = 0
        for ref_answer, res_answer in zip(oanswer, aanswer):
            if ref_answer == res_answer:
                scnt += 1
        similarity = float(scnt/min(len(oanswer),len(aanswer)))
        similarities.append(similarity)
    return similarities






