# -*- coding: utf-8 -*-
import imports

foldername = '..\originaldataset'
ZSname = '..\originaldataset\ZPrompts.json'
FSname = '..\originaldataset\FSamples.json'

# 生成带提示的问题序列
# 输入：问题列表，数据集名称
# 输出：加入提示词的问题列表，分为Zero Shot和Few Shot两种，
# 其中Zero Shot只会提供一句提示词，Few Shot除了提示语外，还会提供1-2个样本
# 下一步工作：调用Ollama方式询问模型得到结果


def ZeroShot_prompt(questions, datasetname):
    with open(ZSname,'r',encoding='utf-8') as fp:
        prompts = imports.json.load(fp)
    prompt = prompts[datasetname]
    Zquestions = []
    for question in questions:
        zquestion = prompt +'\n'+ question
        Zquestions.append(zquestion)
    return Zquestions


def FewShot_prompt(questions, datasetname):
    with open(ZSname, 'r', encoding='utf-8') as fp:
        prompts = imports.json.load(fp)
    prompt = prompts[datasetname]

    with open(FSname,'r',encoding='utf-8') as dp:
        samples = imports.json.load(dp)
    sample = samples[datasetname]

    Fquestions=[]
    for question in questions:
        Fquestion = prompt+sample+question
        Fquestions.append(Fquestion)

    return Fquestions

