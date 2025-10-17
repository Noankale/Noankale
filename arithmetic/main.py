# 函数使用_，变量使用小驼峰
import argparse
from generator import ExerciseGenerator,ExerciseChecker

def write_to_file(filename, content):
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            for line in content:
                f.write(line + '\n')
        return True
    except Exception as e:
        print(f"写入文件 {filename} 失败: {e}")
        return False

def main():
  # 检查用户命令行输入
  parser = argparse.ArgumentParser(description="一个四则运算生成程序")
  parser.add_argument('-n',type=int,help='题目数量')
  parser.add_argument('-r',type=int,help='题目范围')
  parser.add_argument('-e',type=int,help='题目路径')
  parser.add_argument('-a',type=int,help='答案路径')

  args = parser.parse_args()

  # 检查输入参数
  try:
    if args.n is not None and args.r is not None:
      if args.r < 1:
        raise Exception("参数错误：范围参数 r 必须是大于等于1的自然数")
      
    # 若为生成模式 -> 调用生成题目函数
      print(f"正在生成题目……")
      generator = ExerciseGenerator(args.r)
      exercise,answers = generator.generate_exercise(args.n)
    # 将题目和答案分别导出
      if write_to_file('Exercises.txt', exercise):
              print("题目已写入Exercises.txt")
      if write_to_file('Answers.txt', answers):
              print("答案已写入Answers.txt")

    # 若为批改模式 -> 调用批改函数
    elif args.e is not None and args.a is not None:
        print(f"正在批改……")
        correct, wrong = ExerciseChecker.check_answers(args.e, args.a)

    else:
        raise Exception("输入参数错误！")
    
  except Exception as e:
      print(e)

  # 导出批改结果
  return

if __name__ == "__main__":
    main()