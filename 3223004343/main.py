# 函数使用下划线，变量使用小驼峰，常量使用全大写。

#  导入
import math
import jieba
import Levenshtein
import re
import sys
import os
from collections import Counter

jieba.initialize() 

# 处理文本函数
def text_process(text):
    try:
        # 检查输入类型
        if not isinstance(text, str):
            raise TypeError("输入必须为字符串类型。")
        
        # 检查文本是否为空或只包含空白字符
        if not text or text.isspace():
            return []
        
        # 将字符串中的英语转成小写并去除标点
        textRemovePunctuation = re.sub(r'[^\w\s]', '', text.lower())
        
        # 检查处理后的文本是否为空
        if not textRemovePunctuation or textRemovePunctuation.isspace():
            return []
        
        # 分词处理
        textDivide = list(jieba.cut(textRemovePunctuation, cut_all=False))
        
        # 除去英文部分导致的空字符串
        result = list(filter(lambda x: x.strip(), textDivide))
        
        return result
        
    except re.error as e:
        print(f"正则表达式处理错误：{e}")
        return []
    except Exception as e:
        print(f"文本处理过程中发生未知错误：{e}")
        return []

# 计算余弦相似度
def cosine_similarity(words1, words2):
    try:
        # 创建余弦向量
        vec1 = Counter(words1)
        vec2 = Counter(words2)

        words = set(vec1).union(set(vec2))
        
        # 计算分母，若为0则直接返回
        denominator1 = math.sqrt(sum(vec1.get(word, 0)**2 for word in words))
        denominator2 = math.sqrt(sum(vec2.get(word, 0)**2 for word in words))
        
        # 检查分母是否为0
        if denominator1 == 0 or denominator2 == 0:
            return 0.0

        # 计算分子
        molecule = sum(vec1.get(word, 0) * vec2.get(word, 0) for word in words)

        result = molecule / (denominator1 * denominator2)
        
        # 确保结果在合理范围内
        return max(0.0, min(1.0, result))
        
    except (ValueError, ZeroDivisionError) as e:
        print(f"余弦相似度计算错误：{e}")
        return 0.0
    except Exception as e:
        print(f"余弦相似度计算过程中发生未知错误：{e}")
        return 0.0

# 计算Jaccard相似度
def jaccard_similarity(words1, words2):
    try:
        set1 = set(words1)
        set2 = set(words2)
        
        # 统计总词数，若为零则直接返回
        union_set = set1.union(set2)
        if len(union_set) == 0:
            return 0.0
        
        # 统计重复词数
        intersection = len(set1.intersection(set2))

        result = intersection / len(union_set)
        return max(0.0, min(1.0, result))
        
    except (ValueError, ZeroDivisionError) as e:
        print(f"Jaccard相似度计算错误：{e}")
        return 0.0
    except Exception as e:
        print(f"Jaccard相似度计算过程中发生未知错误：{e}")
        return 0.0

# 计算Levenshtein相似度
def levenshtein_similarity(words1, words2):   
    try:
        str1 = ''.join(words1)
        str2 = ''.join(words2)
        
        # 处理空字符串情况
        if not str1 and not str2:
            return 1.0
        elif not str1 or not str2:
            return 0.0

        distance = Levenshtein.distance(str1, str2)
        maxLength = max(len(str1), len(str2))
        
        # 避免除零错误
        if maxLength == 0:
            return 1.0

        result = 1 - (distance / maxLength)
        return max(0.0, min(1.0, result))
        
    except Exception as e:
        print(f"Levenshtein相似度计算错误：{e}")
        return 0.0

# 程序主要逻辑
def main():
    # 输入文件路径
    if len(sys.argv) != 4:
        print("错误：请传入三个文件路径！")
        print("使用格式：python main.py 原文件路径 对比文件路径 答案文件路径")
        sys.exit(1)

    # 从命令行获取文件路径
    originalPath = sys.argv[1]
    addPath = sys.argv[2]
    resultPath = sys.argv[3] 
    
    # 检查文件是否存在
    for file_path in [originalPath, addPath]:
        if not os.path.exists(file_path):
            print(f"错误：文件 '{file_path}' 不存在！")
            sys.exit(1)
        if not os.path.isfile(file_path):
            print(f"错误：'{file_path}' 不是有效的文件！")
            sys.exit(1)

    # 打开文件
    try:
        with open(originalPath, 'r', encoding='utf8') as f:
            originalText = f.read()
        with open(addPath, 'r', encoding='utf8') as f:
            addText = f.read()
    except FileNotFoundError as e:
        print(f"文件未找到错误：{e}")
        sys.exit(1)
    except PermissionError as e:
        print(f"文件权限错误：{e}")
        sys.exit(1)
    except UnicodeDecodeError as e:
        print(f"文件编码错误：{e}")
        sys.exit(1)
    except Exception as e:
        print(f"读取文件时发生未知错误：{e}")
        sys.exit(1)

    # 处理文本
    originalTextList = text_process(originalText)
    addTextList = text_process(addText)

    # 计算相似度
    try:
        # 输入的特殊情况处理
        if not originalTextList and not addTextList:
            print("输入文本均为空，相似度为1。")
            output = "输入文本均为空，相似度为1。"
            cosineSimilarity = jaccardSimilarity = levenshteinSimilarity = avgSimilarity = 1.0
        elif not originalTextList or not addTextList:
            print("输入文本之一为空，相似度为0。")
            output = "输入文本之一为空，相似度为0。"
            cosineSimilarity = jaccardSimilarity = levenshteinSimilarity = avgSimilarity = 0.0
        else:
            cosineSimilarity = cosine_similarity(originalTextList, addTextList)
            jaccardSimilarity = jaccard_similarity(originalTextList, addTextList)
            levenshteinSimilarity = levenshtein_similarity(originalTextList, addTextList)
            avgSimilarity = (cosineSimilarity + jaccardSimilarity + levenshteinSimilarity) / 3
            
            # 构建输出结果
            output = (
                f"文本余弦相似度为：{cosineSimilarity:.4f}\n"
                f"文本Jaccard相似度为：{jaccardSimilarity:.4f}\n"
                f"文本Levenshtein相似度为：{levenshteinSimilarity:.4f}\n"
                f"综合相似度：{avgSimilarity:.4f}\n"
                "\n"
                f"源文件分词结果：{originalTextList}\n"
                f"抄袭文件分词结果：{addTextList}"
            )

        # 写入答案文件
        try:
            # 确保输出目录存在
            os.makedirs(os.path.dirname(resultPath), exist_ok=True)
            
            with open(resultPath, 'w', encoding='utf8') as f:
                f.write(output)
            print(f"\n结果已成功写入到答案文件：{resultPath}")
        except PermissionError as e:
            print(f"写入文件权限错误：{e}")
            sys.exit(1)
        except Exception as e:
            print(f"写入答案文件时发生错误：{e}")
            sys.exit(1)

    except Exception as e:
        print(f"计算相似度时发生错误：{e}")
        sys.exit(1)
    
    return 

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n程序被用户中断")
        sys.exit(1)
    except Exception as e:
        print(f"程序运行过程中发生未预期的错误：{e}")
        sys.exit(1)