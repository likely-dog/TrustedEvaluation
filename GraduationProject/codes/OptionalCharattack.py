# 本模块提供另一种可选的字符级攻击方法
# Demo中采纳了在不破坏原词语结构的情况下，插入随机字符的方法： this is a dog-->this is W a dog.
# 本方法是nlpaug的字符级替换，会破坏单词结构：cat-->c@t
# 详细信息见 https://github.com/makcedward/nlpaug

import nlpaug.augmenter.char as nac
aug = nac.KeyboardAug()
data = 'We also introduce the concept of harmonic embeddings, and a harmonic triplet loss, which describe different versions of face embeddings (produced by different networks) that are compatible to each other and allow for direct comparison between each other.'
result = aug.augment(data)
print(result)