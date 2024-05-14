import imports

def codah_request(isattacking,isattacked,filepath):
    df = imports.pd.read_csv(filepath)
    if isattacking:
        question = [str(x) for x in df['Question prompt'].tolist()]
    else:
        if not isattacked:
            questions = df['Question prompt']+'\n'
        else:
            questions = df['attacked_question']
        choices = "choice0:"+df['choice0']+"choice1:"+df['choice1']+"choice2:"+df['choice2']+"choice3:"+df['choice3']

        question = [f'{q} {c}' for q, c in zip(questions, choices)]
    # print(question)
    answer = [int(x) for x in df['answer'].tolist()]
    return question, answer

def flipkart_request(isattacking,isattacked,filepath):
    df = imports.pd.read_csv(filepath)
    if isattacking:
        question = [str(x) for x in df['Summary'].tolist()]
    else:
        if not isattacked:
            question = [str(x)for x in df['Summary'].tolist()]
        else:
            question = [str(x) for x in df['attacked_question'].tolist()]
    label = [int(x)for x in df['Label'].tolist()]
    return question, label

def math23k_request(isattacking,isattacked,filepath):
    df = imports.pd.read_csv(filepath)
    if isattacking:
        question = [str(x) for x in df['question'].tolist()]
    else:
        if not isattacked:
            question = [str(x)for x in df['question'].tolist()]
        else:
            question = [str(x) for x in df['attacked_question'].tolist()]
    answer = [float(x)for x in df['answer'].tolist()]
    return question, answer

def translation_request(isattacking,isattacked,filepath):
    df = imports.pd.read_csv(filepath)
    if isattacking:
        en = [str(x) for x in df['english'].tolist()]
    else:
        if not isattacked:
            en = [str(x) for x in df['english'].tolist()]
        else:
            en = [str(x) for x in df['attacked_question'].tolist()]
    cn = [str(x) for x in df['chinese'].tolist()]
    return en, cn

def tqam_request(isattacking,isattacked,filepath):
    df = imports.pd.read_csv(filepath)
    answer = []
    if isattacking:
        question = [str(x) for x in df['question'].tolist()]
    else:
        if not isattacked:
            question = [str(x) for x in df['question'].tolist()]
        else:
            question = [str(x) for x in df['attacked_question'].tolist()]
        answer = []
        for index, row in df.iterrows():
            temp = []
            question[index] += '\n'
            for i in range(24):
                column_name = f'answer{i}'
                if imports.pd.isna(row[column_name]):
                    temp.append(-1)
                else:
                    temp.append(int(row[column_name]))
                choice = row[f'choice{i}']
                if not imports.pd.isna(choice):
                    question[index] += f'choice{i}:{choice} '
                answer.append(temp)
    return question, answer

def tqas_request(isattacking,isattacked,filepath):
    df = imports.pd.read_csv(filepath)
    if isattacking:
        question = [str(x) for x in df['question'].tolist()]
    else:
        if not isattacked:
            question = [str(x) for x in df['question'].tolist()]
        else :
            question = [str(x) for x in df['attacked_question'].tolist()]
        answer = [int(x)for x in df['answer'].tolist()]
        for index, row in df.iterrows():
            for i in range(13):
                choice = row[f'choice{i}']
                if not imports.pd.isna(choice):
                    question[index] += f'choice{i}:{choice} '
        # questions.append(question)
    return question, answer

# que,ans = math23k_request()
# print(que[0])
# print(ans[2])