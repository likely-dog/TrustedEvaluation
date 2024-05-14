import ollama
import MyLog

# 运行ollama,获得模型输出内容
# 详见 https://ollama.com/
def ollama_req(modelname,contents):
  results = []
  times = 0
  for content in contents:

    print(content)
    response = ollama.chat(model=modelname, messages=[
      {
        'role': 'user',
        'content': content,
      },
    ])
    results.append(response['message']['content'])
    content = {content: response['message']['content']}
    MyLog.mylog(str(content))
    print(times)
    times += 1


  return results

# quary = ['I am feeling nervous about my midterm tomorrow. I fear thatchoice0:the professor will delay the midterm.choice1:I will doodle on my exam and receive points for it.choice2:my grandpa has diabetes.choice3:I will fail.','can you remember the previous question?']
# results=ollama_req('qwen:4b',quary)
# for result in results:
#   print(result)



