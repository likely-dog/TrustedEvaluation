import imports

# 输入你想要让恢复日志的文件输出的路径
output_filepath = "YourFilepath"


with open('log.txt', 'r') as f:
    lines = f.readlines()
dict_list = [imports.json.loads(lines[i]) for i in range(1, len(lines), 2)]
df = imports.pd.DataFrame(dict_list)
df.to_csv(output_filepath, index=False, columns=['question', 'answer'])
