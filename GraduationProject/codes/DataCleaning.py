import imports

import pandas as pd

# 输入：一段文字
# 输出：文字中的最后一个数字

def extract_last_number(texts):
    ans = []
    for text in texts:
        pattern = r'([-+]?\d*\.?\d+%?)\D*$'
        result = imports.re.search(pattern, text)
        if result:
            ans.append(result.group(1))
        else:
            ans.append(65535)
    return ans

# 提取0/1并生成列表
def extract_zeros_and_ones(texts):
    ans = []
    for text in texts:
        pattern = r'[01]'
        result1 = imports.re.findall(pattern, str(text))
        result2 = [int(x)for x in result1]
        result = process_list(result2)

        ans.append(result)

    return ans



# 用于处理列表函数，使得列表长度符合答案向量长度
def process_list(lst):
    count_0 = lst.count(0)
    count_1 = lst.count(1)
    total_count = count_0 + count_1
    if total_count < 24:
        lst += [-1] * (24 - total_count)
    elif total_count > 24:
        lst = lst[:24]

    return lst
# 把态度positive/negative转换成1/0数字列表
def state2number(texts):
    label = []
    for text in texts:
        if 'positive' in text and 'negative' in text:
            label.append(-1)
        elif 'positive' in text:
            label.append(1)
        elif 'negative' in text:
            label.append(0)
        else:
            label.append(-1)
    return label



