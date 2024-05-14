# -*- coding:utf-8 -*-

import jieba
from collections import Counter
from math import sqrt

def cosine_similarity(vec1, vec2):
    dot_product = sum(a * b for a, b in zip(vec1, vec2))
    norm1 = sqrt(sum(a * a for a in vec1))
    norm2 = sqrt(sum(b * b for b in vec2))
    return dot_product / (norm1 * norm2)

def tokenize(text):
    return list(jieba.cut(text))

def build_vocab(texts):
    vocab = set()
    for text in texts:
        vocab |= set(tokenize(text))
    return sorted(list(vocab))

def text_to_vector(text, vocab):
    words = tokenize(text)
    word_count = Counter(words)
    return [word_count[word] for word in vocab]

def calculate_similarity(ref_list, res_list):
    vocab = build_vocab(ref_list + res_list)
    ref_vectors = [text_to_vector(text, vocab) for text in ref_list]
    res_vectors = [text_to_vector(text, vocab) for text in res_list]
    anslist = [cosine_similarity(ref_vec, res_vec) for ref_vec, res_vec in zip(ref_vectors, res_vectors)]
    return anslist
