import time

import pandas as pd

import imports
import PromptDesign
import RequestGeneration
import TextAttack
import RunModels
import DataCleaning
import CalScores
import FileProcess

codahfolder = '../test_sets'
flipkartfolder = '../test_sets'
math23kfolder = '../test_sets'
translatefolder = '../test_sets'
TQAfolder = '../test_sets'

modelname = ['gemma:2b', 'gemma:7b', 'llama2:7b', 'llama2:13b', 'llama2-chinese:7b', 'llama2-chinese:13b' 'mistral:7b', 'qwen:4b', 'qwen:7b', 'qwen:14b', 'qwen:32b']
datasetname = ['codah', 'flipkart', 'math23k', 'translation', 'tqas', 'tqam']
attackmode = ['character', 'word', 'sentence']

# """
# 任务：生成对抗数据集
# 格式：csv
# 输入：数据集所在文件地址,攻击模式
# 输出：对抗数据集,csv格式
# 返回值：生成的对抗数据集的文件地址
# """

def Adversarial_Dataset(filename, mode):
    attques = None
    attnum = None
    attpairs = None
    filepath = ''
    file = FileProcess.getfilepath(filename)
    requestname = f"RequestGeneration.{filename}_request"
    ques, ans = eval(requestname)(isattacking=True, isattacked=False, filepath=file)
    quesattacked = TextAttack.attack(ques, mode)
    if quesattacked[0]: attques = pd.DataFrame({'attacked_question': quesattacked[0]})
    if quesattacked[1]: attnum = pd.DataFrame({'attack_num': quesattacked[1]})
    if quesattacked[2]: attpairs = pd.DataFrame({'synword_pairs': quesattacked[2]})
    if filename == 'codah':
        ori = pd.read_csv(codahfolder+'/CODAHtest.csv')
        data = pd.concat([ori, attques],axis=1)
        if attnum is not None:
            data = pd.concat([data, attnum], axis=1)
        if attpairs is not None:
            data = pd.concat([data, attpairs], axis=1)
        folder_name = codahfolder+'/attacked'
        if not imports.os.path.exists(folder_name):
            imports.os.mkdir(folder_name)
        data.to_csv(codahfolder+f'/attacked/CODAH_under{mode}attack.csv', index=False)
        filepath = codahfolder+f'/attacked/CODAH_under{mode}attack.csv'

    if filename == 'flipkart':
        ori = pd.read_csv(flipkartfolder + '/Flipkarttest.csv')
        data = pd.concat([ori, attques], axis=1)
        if attnum is not None:
            data = pd.concat([data, attnum], axis=1)
        if attpairs is not None:
            data = pd.concat([data, attpairs], axis=1)
        folder_name = flipkartfolder + '/attacked'
        if not imports.os.path.exists(folder_name):
            imports.os.mkdir(folder_name)
        data.to_csv(flipkartfolder + f'/attacked/Flipkart_under{mode}attack.csv', index=False)
        filepath = flipkartfolder + f'/attacked/Flipkart_under{mode}attack.csv'

    if filename == 'math23k':
        ori = pd.read_csv(math23kfolder + '/Math23Ktest.csv')
        data = pd.concat([ori, attques], axis=1)
        if attnum is not None:
            data = pd.concat([data, attnum], axis=1)
        if attpairs is not None:
            data = pd.concat([data, attpairs], axis=1)
        folder_name = math23kfolder + '/attacked'
        if not imports.os.path.exists(folder_name):
            imports.os.mkdir(folder_name)
        data.to_csv(math23kfolder + f'/attacked/Math23K_under{mode}attack.csv', index=False)
        filepath = math23kfolder + f'/attacked/Math23K_under{mode}attack.csv'

    if filename == 'translation':
        ori = pd.read_csv(translatefolder + '/translation2019zhtest.csv')
        data = pd.concat([ori, attques], axis=1)
        if attnum is not None:
            data = pd.concat([data, attnum], axis=1)
        if attpairs is not None:
            data = pd.concat([data, attpairs], axis=1)
        folder_name = translatefolder + '/attacked'
        if not imports.os.path.exists(folder_name):
            imports.os.mkdir(folder_name)
        data.to_csv(translatefolder + f'/attacked/translation_under{mode}attack.csv', index=False)
        filepath = translatefolder + f'/attacked/translation_under{mode}attack.csv'

    if filename == 'tqas':
        ori = pd.read_csv(TQAfolder + '/TruthfulQASinglectest.csv')
        data = pd.concat([ori, attques], axis=1)
        if attnum is not None:
            data = pd.concat([data, attnum], axis=1)
        if attpairs is not None:
            data = pd.concat([data, attpairs], axis=1)
        folder_name = TQAfolder + '/singleattacked'
        if not imports.os.path.exists(folder_name):
            imports.os.mkdir(folder_name)
        data.to_csv(TQAfolder + f'/singleattacked/TruthfulQASinglectest_under{mode}attack.csv', index=False)
        filepath = TQAfolder + f'/singleattacked/TruthfulQASinglectest_under{mode}attack.csv'

    if filename == 'tqam':
        ori = pd.read_csv(TQAfolder + '/TruthfulQAMultictest.csv')
        data = pd.concat([ori, attques], axis=1)
        if attnum is not None:
            data = pd.concat([data, attnum], axis=1)
        if attpairs is not None:
            data = pd.concat([data, attpairs], axis=1)
        folder_name = TQAfolder + '/multiattacked'
        if not imports.os.path.exists(folder_name):
            imports.os.mkdir(folder_name)
        data.to_csv(TQAfolder + f'/multiattacked/TruthfulQAMultictest_under{mode}attack.csv', index=False)
        filepath = TQAfolder + f'/multiattacked/TruthfulQAMultictest_under{mode}attack.csv'
    return filepath


# """
# 任务：使用ollama的方式加载模型,并运行数据集
# 输入：模型名称，数据集路径，是否为受攻击的文件,提示类型
# 输出：生成答案结果的csv文件，以及模型的回答结果所保存的地址


def RunModel(dataset, modelname, filepath, isattacked, prompt):
    replylist = []
    ques = []
    ans = []

    requestname = f"RequestGeneration.{dataset}_request"
    ques, ans = eval(requestname)(False, isattacked, filepath)
    # print(ques,ans)
    if prompt == 0:
        pques = PromptDesign.ZeroShot_prompt(ques, dataset)
    elif prompt == 1:
        pques = PromptDesign.FewShot_prompt(ques, dataset)

    replylist = RunModels.ollama_req(modelname, pques)


    rfilename, rfile_extension = imports.os.path.splitext(filepath)
    prompttype = "F"if prompt ==1 else "Z"
    modelname = modelname.replace(":","")
    new_filename = f"{rfilename}_{modelname}_{prompttype}_results"
   
    new_filepath = str(new_filename + rfile_extension)
    max_len = max(len(pques), len(ans), len(replylist))
    pques += [''] * (max_len - len(pques))
    ans += [''] * (max_len - len(ans))
    replylist += [''] * (max_len - len(replylist))

    content = {'question': pques, 'answer': ans, 'result': replylist}
    df = pd.DataFrame(content)
    # print(content)
    df.to_csv(new_filepath, index=False, encoding='utf-8')
    return new_filepath

# """
# 任务：计算正确性与鲁棒性各指标得分
# 输入：模型的回答结果所保存的文件目录
# 输出：各项得分细节保存csv文件中，总的平均得分保存在txt文件
# """
# TODO：使用calscore模块的方法计算
def Calculate_Scores(filepath, dataset, isattacked):
    df = pd.read_csv(filepath)
    ans = df['answer'].tolist()
    result = df['result'].tolist()
    newcsvpath = filepath[:-4] + 'checked.csv'
    newtxtpath = filepath[:-4] + 'scores.txt'
    if dataset == 'flipkart':
        res = DataCleaning.state2number(result)
        reslist, precision = CalScores.singlec_precision(res, ans)
        df["precision"] = reslist
        df.to_csv(newcsvpath, index=False, encoding='utf-8')
        with open(newtxtpath, 'w', encoding='utf-8') as f:
            f.write("The precision is " + str(precision)+".")
        if isattacked:
            oripath = input("输入带结果的原测试集的文件路径:")
            try:
                fp = pd.read_csv(oripath)
            except FileNotFoundError:
                print("原测试集结果不存在！")
                return None
            orians = fp["precision"].tolist()
            similarty = CalScores.singlec_similarity(orians, reslist)
            with open(newtxtpath, 'a', encoding='utf-8') as f:
                f.write("The similarity to original test set is " + str(similarty)+".")


    elif dataset =='tqam':
        ans1 = [imports.ast.literal_eval(x)for x in ans]
        res = DataCleaning.extract_zeros_and_ones(result)
        precisions, recalls, f1_scores = CalScores.multic_f1(res, ans1)
        df["precision"] = precisions
        df["recall"] = recalls
        df["f1"] = f1_scores
        df.to_csv(newcsvpath, index=False, encoding='utf-8')
        with open(newtxtpath, 'w', encoding='utf-8') as f:
            f.write("The precision is " + str(imports.np.mean(precisions))+".")
            f.write("The recall is " + str(imports.np.mean(recalls))+".")
            f.write("The f1 score is " + str(imports.np.mean(f1_scores))+".")
        if isattacked:
            oripath = input("输入带结果的原测试集的文件路径:")
            try:
                fp = pd.read_csv(oripath)
            except FileNotFoundError:
                print("原测试集结果不存在！")
                return None
            refprecision = fp["precision"].tolist()
            refrecall = fp["recall"].tolist()
            reff1scores = fp["f1"].tolist()
            psimilarty = CalScores.singlec_similarity(refprecision, precisions)
            precall = CalScores.singlec_similarity(refrecall, recalls)
            pf1 = CalScores.singlec_similarity(reff1scores, f1_scores)
            with open(newtxtpath, 'a', encoding='utf-8') as f:
                f.write("The precision similarity to original test set is " + str(psimilarty)+".")
                f.write("The recall similarity to original test set is " + str(precall)+".")
                f.write("The f1 score similarity to original test set is " + str(pf1)+".")

    elif dataset == 'tqas'or dataset =='codah':
        res1 = DataCleaning.extract_last_number(result)
        res = []
        for x in res1:
            try:
                res.append(int(x))
            except ValueError:
                res.append(65535)
        reslist, precision = CalScores.singlec_precision(res, ans)
        df["precision"] = reslist
        df.to_csv(newcsvpath, index=False, encoding='utf-8')
        with open(newtxtpath, 'w', encoding='utf-8') as f:
            f.write("The precision is " + str(precision)+".")
        if isattacked:
            oripath = input("输入带结果的原测试集的文件路径:")
            try:
                fp = pd.read_csv(oripath)
            except FileNotFoundError:
                print("原测试集结果不存在！")
                return None
            orians = fp["precision"].tolist()
            similarty = CalScores.singlec_similarity(orians, reslist)
            with open(newtxtpath, 'a', encoding='utf-8') as f:
                f.write("The similarity to original test set is " + str(similarty)+".")

    elif dataset == 'math23k':
        res1 = DataCleaning.extract_last_number(result)
        res = []
        for x in res1:
            try:
                res.append(float(x))
            except ValueError:
                res.append(65535.0)
        reslist, precision = CalScores.singlec_precision(res,ans)
        df["precision"] = reslist
        df.to_csv(newcsvpath, index=False, encoding='utf-8')
        with open(newtxtpath, 'w', encoding='utf-8') as f:
            f.write("The correct rate is " + str(precision)+".")
        if isattacked:
            oripath = input("输入带结果的原测试集的文件路径:")
            try:
                fp = pd.read_csv(oripath)
            except FileNotFoundError:
                print("原测试集结果不存在！")
                return None
            orians = fp["precision"].tolist()
            similarty = CalScores.singlec_similarity(orians, reslist)
            with open(newtxtpath, 'a', encoding='utf-8') as f:
                f.write("The similarity to original test set is " + str(similarty) + ".")

    elif dataset == 'translation':
        res = result
        scores = []
        emscore = CalScores.en2cn_emscore(res,ans)
        rouge1, rouge2, rougeL = CalScores.en2cn_rouge(res, ans)
        for i in range(len(emscore)):
            if emscore[i] == 1:
                scores.append(1)
            else:
                rouge_product = imports.np.prod([rouge1[i], rouge2[i], rougeL[i]])
                scores.append(imports.np.power(rouge_product, 1 / 3))
        df["emscore"] = emscore
        df["rouge1"] = rouge1
        df["rouge2"] = rouge2
        df["rougeL"] = rougeL
        df["scores"] = scores
        df.to_csv(newcsvpath, index=False, encoding='utf-8')
        with open(newtxtpath, 'w', encoding='utf-8') as f:
            f.write("The exact match score is " + str(imports.np.mean(emscore)) + ".")
            f.write("The rouge-1 score is " + str(imports.np.mean(rouge1)) + ".")
            f.write("The rouge-2 score is " + str(imports.np.mean(rouge2)) + ".")
            f.write("The rouge-l score is " + str(imports.np.mean(rougeL)) + ".")
            f.write("The score is " + str(imports.np.mean(scores)) + ".")
        if isattacked:
            oripath = input("输入带结果的原测试集的文件路径:")
            try:
                fp = pd.read_csv(oripath)
            except FileNotFoundError:
                print("原测试集结果不存在！")
                return None
            orians = fp["scores"].tolist()
            similarty = CalScores.en2cn_similarity(orians, scores)
            print(similarty)
            with open(newtxtpath, 'a', encoding='utf-8') as f:
                f.write("The similarity to original test set is " + str(imports.np.mean(similarty)) + ".")

if __name__ == '__main__':

    choice1 = input("入是否要攻击数据集：Y/N")
    quesfilepath = ''
    isattacked = False
    shot = 0
    if choice1 == 'Y':
        # 对抗数据集生成
        # 数据集名称：codah,flipkart,math23k,translation,tqas,tqam,分别代表六个数据集
        # 数据攻击模式：character,word,sentence,分别代表字符级，词语级，句子级攻击
        dataset, mode = input('分别输入要攻击的数据集名称和攻击模式:')
        if (dataset not in datasetname) or (mode not in attackmode):
            raise ValueError("数据集或者攻击模式不存在")
        filename = Adversarial_Dataset(dataset, mode)
        isattacked = True
    elif choice1 == 'N':
        dataset = input('输入要使用的数据集')
        if dataset not in datasetname:
            raise ValueError("数据集不存在")
        quesfilepath = FileProcess.getfilepath(dataset)
    else:
        raise ValueError("输入错误")

    model = input("输入想要测试的模型名称：")
    if model not in modelname:
        raise ValueError("模型不存在")
    prompt = input("输入提示语模式，0代表zero-shot,1代表few-shot:")
    if prompt not in [0,1]:
        raise ValueError("提示语模式不存在")
    # 原数据集测试,第三个参数输入False
    # 对抗数据集测试,第三个参数输入True
    # choice2 代表提示词模式，0代表zero-shot，提示语中将不会给出参考样例
    # 1代表few shot，会给出1-2个参考，然后询问问题
    resfilepath = RunModel(dataset,model, quesfilepath, isattacked, prompt)
    # 指标计算
    time.sleep(2)
    Calculate_Scores(resfilepath, dataset, isattacked)
