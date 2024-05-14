import imports
import pandas as pd

# ���룺һ������
# ����������е����һ������
# ����math23k����ȡ�ش�����ս��
def extract_last_number(text):
    if isinstance(text, str):
        match = imports.re.search(r'([-+]?\d*\.?\d+%?)\D*$', text)
        if match:
            return match.group(1)
        else:
            return None

def extract_zeros_and_ones(texts):
    ans = []
    for text in texts:
        pattern = r'[01]'
        result = imports.re.findall(pattern, text)
        if result:
            ans.append(result.group(1))
        else:
            ans.append([])
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
