# 函数使用下划线，变量使用小驼峰，常量使用全大写。

#  导入
import math
import jieba;
import re;
from collections import Counter

# 处理文本函数
def text_process(text):

  # 将文本中的英语转成小写并去除标点
  textRemovePunctuation = re.sub(r'[^\w\s]','',text.lower())
  # 分词处理
  textDivide = list(jieba.cut(textRemovePunctuation,cut_all = False))

  return textDivide

def cosine_similarity(words1,words2):
  #  创建余弦向量
  vec1 = Counter(words1)
  vec2 = Counter(words2)

  words = set(vec1).union(set(vec2))
  
  # 计算分母，若为0则直接返回
  denominator1 = math.sqrt(sum(vec1.get(word, 0)**2 for word in words ))
  if denominator1 == 0:
    return 0;
  denominator2 = math.sqrt(sum(vec2.get(word, 0)**2 for word in words ))
  if denominator2 == 0:
    return 0;

# 计算分子
  molecule = sum(vec1.get(word,0)*vec2.get(word,0) for word in words )

  return molecule/(denominator1*denominator2)

def jaccard_similarity(words1,words2):
  # 计算Jaccard相似度
  set1 = set(words1)
  set2 = set(words2)
  
  # 统计总词数，若为零则直接返回
  words = len(set1.union(set2))
  if words == 0:
    return 0
  
  # 统计重复词数
  intersection = len(set1.intersection(set2))

  return intersection/words

# 计算相似度
def cal_similarity(words1,words2):

  similarity1 = cosine_similarity(words1,words2)
  similarity2 =  jaccard_similarity(words1,words2)

  # 加权计算相似度
  similarity = (similarity1 + similarity2)/2

  print(f'文本余弦相似度为：{similarity1}')
  print(f'文本jaccard相似度为：{similarity2}')
  return similarity

# 程序主要逻辑
def main():
  # 输入文件路径
  # originalPath = input("请输入论文原文件路径：") 
  # addPath = input("请输入修改后的论文文件路径：") 

  # # 打开文件
  # with open(originalPath,'r','utf8') as f:
  #   originalText = f.read()
  # with open(addPath,'r','utf8') as f:
  #   addText = f.read()

  # 处理文本
  orignalTextList = text_process("今天真是好天气啊，我想出去玩，但是好热太阳好晒。还是在家吹空调舒服。there is some english word I WaNt to see")
  addTextList = text_process("今天天气真好，我想出去玩，但是外面好热。还是在家吹空调舒服。there is some english word I WaNt to see")

  # 计算相似度
  similarity = cal_similarity(orignalTextList,addTextList)

  # 输出结果
  print(similarity)


  return 


if __name__ == '__main__':
  main()