# -*- coding: utf-8 -*-

# 输入：测试集名称：codah,flipkart,math23k,translation,tqas,tqam,分别代表六个数据集
# 输出：测试集文件路径
def getfilepath(filename):
    if filename == 'codah':
        filepath = '../test_sets/CODAHtest.csv'
    elif filename == 'flipkart':
        filepath = '../test_sets/Flipkarttest.csv'
    elif filename == 'math23k':
        filepath = '../test_sets/Math23Ktest.csv'
    elif filename == 'translation':
        filepath = '../test_sets/translation2019zhtest.csv'
    elif filename == 'tqas':
        filepath = '../test_sets/TruthfulQAMultictest.csv'
    elif filename == 'tqam':
        filepath = '../test_sets/TruthfulQAMultictest.csv'
    else:
        raise ValueError("测试集不存在")
    return filepath

