# Trusted Evaluation：一种基于python语言和ollama项目的自动评估大语言模型的正确性与鲁棒性的方法

本项目旨在提供一种不占用显卡资源，尽量少的人工参与下，轻量级大语言模型的本地部署与自动测试方法。

## 运行环境
- Python>=3.10
- Ollama>=0.1.34
- Windows >=10
- 另外本项目是基于Ollama项目做的，在内存与CPU上运行大语言模型，请确保电脑测试时可用内存大小大于或等于待测模型的大小的2倍。如果您有更优的运行大模型的方式,或者要测试的大模型不包含在Ollama项目中，则不必通过本项目来进行自动评估。然而，本项目中的测试集，对抗文本生成以及指标计算方法等环节也值得参考。

## 开始
克隆项目到本地。
```
git clone git@github.com:likely-dog/TrustedEvaluation.git
```
安装Ollama，安装链接与使用方法详见：
https://github.com/ollama/ollama

本项目的测试集中提供了受攻击后的测试集，在文件夹test_set/attack/中，可以直接使用。
注意：由于翻译限额的原因，句意级攻击生成的测试集只有30条；如果您有更合适的翻译方法，可在

如果需要本地生成对抗性文本且需要中文词语级的攻击方法，请下载中文近义词工具包Synonmys：
https://github.com/chatopera/Synonyms

如果不需要，在Demo.py文件中将：
```
import TextAttack
```
注释掉即可。

运行Demo.py,按照指定输入信息开始测试。

## 详细介绍
### 流程图
![image](https://github.com/likely-dog/TrustedEvaluation/assets/72387024/80542b51-a4bf-4945-be49-17441bbbfe30)

### 测试集选择依据与介绍

原数据集保存original_dataset文件夹，测试集保存在test_set文件夹，可以直接使用，也可以按需要使用原数据集构造
#### CODAH
CODAH(COmmonsense Dataset Adversarially-authored by Humans)数据集是一个用于测试常识的对抗性构建的评估数据集。它是对最近提出的SWAG数据集的一个具有挑战性的扩展，该数据集使用描述视频中观察到的情况的句子完成问题来测试常识类知识。常识推理是一项关键的指标，但构建测试常识的具有挑战性的数据集很困难。为了生成更困难的数据集，数据集的作者引入了一种新颖的问题获取程序，旨在针对最先进的神经问答系统的弱点的问题。该数据集目前已经开源，本文选取该数据集中的500条作为测试集，用来测试大语言模型对于常识知识的推理能力。
该数据集是一个英文数据集。它的问答方式为一个叙述句，后面附有固定数量的可选项，很适合作为选择题格式。数据集中包含正确选项的标签且经过人工标注，不需要再去筛选，但需要人工检查一次标注的正确性。预处理后生成一个csv文件，文件中包含问题,choice0-choice3四个选项，以及正确的标签六个属性。

####  Flipkart Product reviews with sentiment Dataset
Flipkart是一个外国的购物网站，Flipkart Product reviews with sentiment Dataset（后文简称为Flipkart）数据集是爬取了该网站的商品评论，并由人工标注情绪后的生成的数据集。该数据集包含有关 csv 格式的产品名称、产品价格、价格、评论、摘要和情绪的信息。该数据集目前已经开源，本文选取该数据集中的500条作为测试集，用来测试大语言模型对于情感的判断能力，这里面包括了234条标记为negative与266条标记为positive的叙述。
该数据集是一个英文数据集。每一行包含了产品名称、产品价格、价格、评论、摘要和情绪的信息。数据集中包含正确选项的标签且经过人工标注，不需要再去筛选，但需要人工检查一次标注的正确性。预处理后生成一个csv文件，包含评论和情绪，以及情绪标签三个属性，情绪标签中positive为1，negative为0。


####  Math23K
Math23K是一个为解决数学应用题而创建的数据集，包含从互联网上爬取的23、162个中文问题，问题难度相当于中国小学生水平。由于原数据集是用来训练模型的分词能力，因此没有对爬取的答案进行人工标注，问题的答案不一定准确。由于该数据集训练模型的分词能力而非作为验证集，实验中首先利用专有模型gpt-3.5-turbo, ERNIE-3.5-8K（文心一言的主要模型）,星火大模型V3.5测试了100条该问题，确保该数据集的内容可以被大语言模型接受。该数据集目前已经开源，本文选取该数据集中的500条作为测试集，用来测试大语言模型对于数学计算的能力。
该数据集是一个中文数据集。每一行包含了问题id,问题，分词情况，计算过程，答案。数据集的答案正确性不能保证，预处理中进行了人工标注。

####  Translation2019zh
Translation2019zh是开源在百度飞桨上的一个中英文数据集，格式为json，包含大量的中英文数据对。由于该数据集主要是用来训练模型而非验证，实验中首先利用专有模型gpt-3.5-turbo, ERNIE-3.5-8K（文心一言的主要模型）,星火大模型V3.5测试了100条该问题并检测结果，确保该数据集的内容可以被大语言模型接受。该数据集目前已经开源，本文选取该数据集中的500条作为测试集，用来测试部分大语言模型的双语能力。
该数据集是一个双语数据集。一个数据对包含了英文及其中文译文，翻译质量较高不用人工标注。预处理后生成一个csv文件,包含英文与中文两个属性。

####  TruthfulQA
TruthfulQA是一个测试模型如何说假话的基准，该基准涵盖多个类别，包括健康、法律、金融和政治。TruthfulQA包含了一个模仿了流行的误解，并且有可能欺骗人类数据集。该基准已经开源，本文利用它的数据集生成两个包含500条问答的测试集，分别为单项选择与多项选择，用来测试模型是否会说假话。
该数据集是一个英文数据集。一条问答包含一个问题以及多条可选项，回答的可选项数量多且可选项数量每道题都不固定，这为预处理提出了挑战。预处理中选择可选项条数最多的一个作为总选项数，其他选项数少的问题，对应选项位置为空。预处理后生成csv文件,包含问题，选项以及答案标记的属性。

### 提示词设计
依据测试集的特征，推断出每一个测试集问答中最可能的受众群体，采用“角色-任务”模式，包含在ZPrompts.json与FSamples.json中，分别对应着零样本测试与少样本测试两种方法。
这两个文件包含在test_set文件夹中，可以不做修改直接用，也可以根据需要修改；如果您需要使用其他的测试集，也可以采取“角色-任务”模式生成提示词。

### 攻击注入方法介绍
攻击注入包含三种程度：字符级，词语级，句意级。对于任务清晰且不太严格要求语义的任务中，三级攻击方法都适用；对于严格要求语义的任务中，只建议使用字符级攻击方法，因为其他两种方法会导致语义的变化，增加人工审核的工作量。
- 字符级攻击方法：本方法中的字符将键盘上的符号以及单个语气词包含在Python列表中。Demo中模仿键盘输入时可能产生的误触现象，随机注入符号。在中文方法中，Demo中提供了常见的单字语气词以及其他符号；在英文方法中，Demo中提供了单个字母以及ASCII码中包含的其他符号。注入采取完全随机方法，根据单词数量或者汉字数量决定注入数量，具体来说是：当单词数量或者汉字数量小于15，注入数量为2；大于15时，按照每十个单词或汉字注入一个对抗性字符。利用字符级攻击返回结果是攻击后的问题列表以及攻击次数的列表，以供人工检查是否破坏了关键数据（如34经攻击后变成了3/4，可能会造成结果的异常）。
- 词语级攻击方法：本方法采用了两个开源的词库。Demo中采取替换同义词的方法进行词语级攻击。在中文方法中，Demo采用了目前最受欢迎的中文分词工具——jieba库进行分词，然后使用Synonyms中文近义词表同义词替换。在英文方法中，由于英文的特点，不需要进行分词工具。Demo采用了Python语言的nltk包中的Wordnet进行近义词替换。注入采取完全随机方法，根据单词数量或者汉字数量决定注入数量，具体来说是：当单词数量或者汉字数量小于15，注入数量为2；大于15时，按照每十个单词或汉字注入一个对抗性字符。利用词语级攻击返回结果是攻击后的问题列表，攻击次数的列表以及替换的同义词对列表，以满足语义评审是否因为替换词语而导致关键词的修改。
- 句意级攻击方法：本方法采用开源的翻译工具。Demo采取回译的方法进行句意级攻击。回译方法即将原问题翻译为其他语言，再翻译回原语言的方法，常用于句意攻击。Demo中利用了google translator提供的python接口，该接口每日有5000字符的无条件翻译限额，您也可以替换其他的翻译程序。利用句意级攻击返回结果是攻击后的问题列表，以满足语义评审是否因为替换词语而导致关键词的修改。

### 日志记录以及日志恢复
日志记录的是每次模型运行得出结果的时间，输入问题以及测试结果，保存在log.txt文件中。日志格式是单数行为问题回答的时间，偶数行为该问题的问题和答案的结果对。日志文件不会自动删除，当运行一定量的数据集且没出现异常时，可以手动删除日志记录来减少存储占用。日志数据恢复实现细节在LogRecovery.py中，作用是当测试模型出现异常而退出程序时，手动恢复已经运行的数据，从而避免重复运行相同问题导致的资源浪费，确保数据的完整性。

### 数据处理与指标计算
  数据清理的实现细节在DataCleaning.py中，对生成的结果进行提取，使提取的内容便于自动检测。Demo中针对上述五个测试集，提供了一种关键词匹配的方法和两种正则表达式提取结果的方法。其中关键词匹配用于处理Flipkart测试集结果中顾客态度的回答。两种正则表达式匹配分别为提取最后一个数字，用于处理Math23k测试集结果中计算题最终答案，以及单项选择题中大语言模型给出的选项，这一方法是根据大部分大语言模型使用过程中的生成特点表现的，即大语言模型回答问题时很可能先是对问题做出很多解释，而这些解释是在评测过程中一般不需要考虑的；同时模型倾向于在最后复述一遍结果，因此对于数字类答案题，选取最后一个数字的效率高且提取成功率高；另外，该方法还可以轻微修改后变成提取第一个数字，方法使用前需要试验该模型平时的输出格式。另一种方式提取回答列表中的所有0与1并生成一个列表，这个列表表示模型对于多选题答案的答案向量，用于TruthfulQA的多项选择题部分。

  指标计算的实现细节在CalScores.py，函数调用在Demo.py中。指标包含了准确性，F1分数，rouge分数，精确匹配分数，余弦相似度等，计算结果保存在.txt文件中，txt文件的命名为：答案集名称+“score.txt”。同时还将标注后的答案写入一个.csv文件中，该文件的命名为：答案集名称+“checked.csv”。

## 未来展望
- 提供更多测试集，丰富指标计算方法。
- 尝试将评估标准由大语言模型扩展到更多种的生成式人工智能，如图片生成，语音识别等。
- 邀请更多拥有不同专业知识背景的人加入评估流程。
