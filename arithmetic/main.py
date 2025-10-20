# 函数使用，变量使用小驼峰
import argparse
from generator import ExerciseGenerator, ExerciseChecker


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
    parser = argparse.ArgumentParser(description="一个四则运算法生成程序")
    parser.add_argument('-n', type=int, help='题目数量')
    parser.add_argument('-r', type=int, help='题目范围')
    parser.add_argument('-e', type=str, help='题目路径')
    parser.add_argument('-a', type=str, help='答案路径')

    args = parser.parse_args()

    # 检查输入参数
    try:
        # 检查是否同时提供了生成和批改参数（这是不允许的）
        has_generation_args = args.n is not None or args.r is not None
        has_grading_args = args.e is not None or args.a is not None

        if has_generation_args and has_grading_args:
            raise Exception("输入参数错误！不能同时使用生成模式和批改模式参数。")

        # 检查生成模式参数是否完整
        if has_generation_args:
            if args.n is None or args.r is None:
                raise Exception("输入参数错误！生成模式需要同时提供 -n 和 -r 参数。")
            if args.n < 1:
                raise Exception("参数错误：题目数量 n 必须是大于等于1的自然数")
            if args.r < 1:
                raise Exception("参数错误：范围参数 r 必须是大于等于1的自然数")

            # 生成模式 -> 调用生成题目函数
            print(f"正在生成题目……")
            generator = ExerciseGenerator(args.r)
            exercises, answers = generator.generate_exercise(args.n)

            # 将题目和答案分别导出
            if write_to_file('Exercises.txt', exercises):
                print("题目已写入Exercises.txt")
            else:
                print("题目写入失败")

            if write_to_file('Answers.txt', answers):
                print("答案已写入Answers.txt")
            else:
                print("答案写入失败")

        # 检查批改模式参数是否完整
        elif has_grading_args:
            if args.e is None or args.a is None:
                raise Exception("输入参数错误！批改模式需要同时提供 -e 和 -a 参数。")

            print(f"正在批改……")
            try:
                correct, wrong = ExerciseChecker.check_answers(args.e, args.a)
                print(f"Correct: {len(correct)} ({', '.join(sorted(correct, key=int))})")
                print(f"Wrong: {len(wrong)} ({', '.join(sorted(wrong, key=int))})")
            except Exception as e:
                print(f"批改错误: {e}")
                return 1

        else:
            raise Exception("输入参数错误！请提供生成模式(-n, -r)或批改模式(-e, -a)参数。")

    except Exception as e:
        print(e)
        return 1

    return 0


if __name__ == "__main__":
    main()

# python main.py -e Exercises.txt -a Answers.txt
# python main.py -n 10 -r 10