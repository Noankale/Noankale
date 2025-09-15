# 函数使用下划线，变量使用小驼峰，常量使用全大写。

#  导入库
import jieba;
import re;

# 处理文本函数
def text_process(text):

  # 去除标点
  textRemovePunctuation = re.sub(r'[^\w\s]','',text)
  # 分词
  textDivide = jieba.cut(textRemovePunctuation,cut_all=True)

  return textDivide


# 程序主要逻辑
def main():
  # 输入文件路径
  originalPath = input("请输入论文原文件路径：") 
  addPath = input("请输入修改后的论文文件路径：") 

  # 打开文件
  with open(originalPath,'r','utf8') as f:
    originalText = f.read()
  with open(addPath,'r','utf8') as f:
    addText = f.read()

  # 处理文本
  orignalTextList = text_process("今天真是好天气啊，我想出去玩，但是好热太阳好晒。还是在家吹空调舒服。")

  # addTextList = jieba.cut(addText,cut_all=True)

  # 计算相似度


  # 输出结果
  print("/".join(orignalTextList))


  return 


if __name__ == '__main__':
  main()