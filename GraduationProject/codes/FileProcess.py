# -*- coding: utf-8 -*-

# 输入：测试集名称：codah,flipkart,math23k,translation,tqas,tqam,分别代表六个数据集
# 输出：测试集文件路径
def getfilepath(filename):
    if filename == 'codah':
        filepath = '../originaldataset/CODAH/CODAHtest.csv'
    elif filename == 'flipkart':
        filepath = '../originaldataset/Flipkart/Flipkarttest.csv'
    elif filename == 'math23k':
        filepath = '../originaldataset/Math23K/Math23Ktest.csv'
    elif filename == 'translation':
        filepath = '../originaldataset/translation2019zh/translation2019zhtest.csv'
    elif filename == 'tqas':
        filepath = '../originaldataset/TruthfulQAdata/TruthfulQAMultictest.csv'
    elif filename == 'tqam':
        filepath = '../originaldataset/TruthfulQAdata/TruthfulQAMultictest.csv'
    else:
        raise ValueError("数据集不存在")
    return filepath

# path = getfilepath(input("输入文件夹名字:"))
# print(path)
