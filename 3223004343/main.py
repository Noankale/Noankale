# 函数使用下划线，变量使用小驼峰，常量使用全大写。

#  导入
import math
import jieba
import Levenshtein
import re
import sys
from collections import Counter

# 处理文本函数
def text_process(text):
  try:
    # 检查输入类型
    if not isinstance(text,str):
      raise TypeError("输入必须为字符串类型。")
    # 将字符串中的英语转成小写并去除标点
    textRemovePunctuation = re.sub(r'[^\w\s]','',text.lower())
    # 分词处理
    textDivide = list(jieba.cut(textRemovePunctuation,cut_all = False))
    # 除去英文部分导致的 ‘ ’
    result =  list(filter(lambda x: x.strip(), textDivide))
    # print(result)
    return result
  except Exception as e:
    print(f"文本处理过程中发生错误：{e}")
    return []

# 计算余弦相似度
def cosine_similarity(words1,words2):
  #  创建余弦向量
  vec1 = Counter(words1)
  vec2 = Counter(words2)

  words = set(vec1).union(set(vec2))
  
  # 计算分母，若为0则直接返回
  denominator1 = math.sqrt(sum(vec1.get(word, 0)**2 for word in words ))
  denominator2 = math.sqrt(sum(vec2.get(word, 0)**2 for word in words ))

# 计算分子
  molecule = sum(vec1.get(word,0)*vec2.get(word,0) for word in words )

  return molecule/(denominator1*denominator2)


# 计算Jaccard相似度
def jaccard_similarity(words1,words2):
  set1 = set(words1)
  set2 = set(words2)
  
  # 统计总词数，若为零则直接返回
  words = len(set1.union(set2))
  if words == 0:
    return 0
  
  # 统计重复词数
  intersection = len(set1.intersection(set2))

  return intersection/words


# 计算Levenshtein相似度
def levenshtein_similarity(words1,words2):   
  str1 = ''.join(words1)
  str2 = ''.join(words2)

  distance = Levenshtein.distance(str1,str2)
  maxLength = max(len(str1),len(str2))

  return 1-(distance/maxLength)


# 程序主要逻辑
def main():
  # 输入文件路径
  if len(sys.argv) != 4:
    print("错误：请传入三个文件路径！")
    print("使用格式：python main.py 原文件路径 对比文件路径 答案文件路径")
    sys.exit(1)

  # 从命令行获取文件路径，格式为 python main.py [原文文件] [抄袭版论文的文件]
  originalPath = sys.argv[1]
  addPath = sys.argv[2]
  resultPath = sys.argv[3] 

  # 打开文件
  try:
    with open(originalPath,'r',encoding='utf8') as f:
      originalText = f.read()
    with open(addPath,'r',encoding='utf8') as f:
      addText = f.read()
  except Exception as e:
    print(f"读取文件时发生错误：{e}")
    sys.exit(1)

  # 处理文本
  originalTextList = text_process(originalText)
  addTextList = text_process(addText)

  # 计算相似度
  try:
    # 输入的特殊清空
    if not originalTextList and not addTextList:
      print(f"输入文本均为空，相似度为1。")
      output = (f"输入文本均为空，相似度为1。")
      try:
        with open(resultPath, 'w', encoding='utf8') as f:
            f.write(output)
        print(f"结果已成功写入到答案文件：{resultPath}")
        exit(0)
      except Exception as e:
        print(f"写入答案文件时发生错误：{e}")
        sys.exit(1)
    elif not originalTextList or not addTextList:
      print(f"输入文本之一为空，相似度为0。")
      output = (f"输入文本之一为空，相似度为0")
      try:
        with open(resultPath, 'w', encoding='utf8') as f:
            f.write(output)
        print(f"结果已成功写入到答案文件：{resultPath}")
        exit(0)
      except Exception as e:
        print(f"写入答案文件时发生错误：{e}")
        sys.exit(1)
      

    cosineSimilarity = cosine_similarity(originalTextList, addTextList)
    jaccardSimilarity = jaccard_similarity(originalTextList, addTextList)
    levenshteinSimilarity = levenshtein_similarity(originalTextList, addTextList)

    avgSimilarity = (cosineSimilarity + jaccardSimilarity + levenshteinSimilarity) / 3

  except Exception as e:
    print(f"计算相似度时发生错误：{e}")
    sys.exit(1)

  # 输出结果
  output = (
        f"文本余弦相似度为：{cosineSimilarity:.2f}\n"
        f"文本Jaccard相似度为：{jaccardSimilarity:.2f}\n"
        f"文本Levenshtein相似度为：{levenshteinSimilarity:.2f}\n"
        f"综合相似度：{avgSimilarity:.2f}\n"
        "\n"
        f"源文件分词结果：{originalTextList}\n"
        f"抄袭文件分词结果：{addTextList}"
    )
 # 写入答案文件
  try:
      with open(resultPath, 'w', encoding='utf8') as f:
          f.write(output)
      print(f"\n结果已成功写入到答案文件：{resultPath}")
  except Exception as e:
      print(f"写入答案文件时发生错误：{e}")
      sys.exit(1)
  
  return 


if __name__ == '__main__':
  main()