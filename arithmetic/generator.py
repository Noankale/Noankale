import random
import hashlib
import re
from fraction import Fraction


class ExerciseGenerator:
    """生成算术练习题及答案"""

    def __init__(self, range_val):
        self.range = range_val  # 数字范围
        self.operators = ['+', '-', '×', '÷']  # 支持的运算符
        self.hashList = set()  # 用于存储题目哈希值，确保唯一性

    def generate_exercise(self, num):
        """生成指定数量的练习题及答案"""
        exercises = []
        answers = []
        count = 0
        i = 0

        # 最多尝试10*num次生成，防止无限循环
        max_attempts = num * 10
        while count < num and i < max_attempts:
            try:
                exercise, answer = self.generate_expression(3)
                # 去除外层括号
                if exercise.startswith('(') and exercise.endswith(')'):
                    exercise = exercise[1:-1]
                # 检查唯一性
                if self.is_Unique(exercise):
                    count += 1
                    exercises.append(f"{count}. {exercise} = ")
                    answers.append(f"{count}. {answer}")
            except (ValueError, ZeroDivisionError):
                # 忽略生成过程中的异常，继续尝试
                pass
            i += 1

        return exercises, answers

    def normalized_exercise(self, exercise):
        # 校验表达式格式
        exercise = exercise.strip()
        # 检查基本格式：数字、运算符、括号的正确组合
        if not re.fullmatch(r'^([\d/\'\(\)]+\s*[\+\-×÷]\s*)*[\d/\'\(\)]+$', exercise):
            raise ValueError("无效的表达式格式")

        # 检查括号匹配
        stack = []
        for char in exercise:
            if char == '(':
                stack.append(char)
            elif char == ')':
                if not stack:
                    raise ValueError("无效的表达式格式")
                stack.pop()
        if stack:
            raise ValueError("无效的表达式格式")

        try:
            # 处理加法交换律
            if '+' in exercise and '(' not in exercise and exercise.count('+') == 1:
                parts = exercise.split(' + ')
                if len(parts) == 2:
                    left, right = parts
                    if left > right:
                        return f"{right} + {left}"

            # 处理乘法交换律
            if '×' in exercise and '(' not in exercise and exercise.count('×') == 1:
                parts = exercise.split(' × ')
                if len(parts) == 2:
                    left, right = parts
                    if left > right:
                        return f"{right} × {left}"

            return exercise
        except:
            return exercise

    def is_Unique(self, exercise: str):
        try:
            normalized = self.normalized_exercise(exercise)
        except ValueError:
            normalized = exercise  # 格式错误时使用原始字符串

        # 计算哈希值
        hash_val = hashlib.md5(normalized.encode()).hexdigest()
        if hash_val not in self.hashList:
            self.hashList.add(hash_val)
            return True
        return False

    def generate_number(self):
        """生成自然数或真分数"""
        is_integer = random.choice([True, False])

        if is_integer:
            # 生成自然数
            integer_part = random.randint(1, self.range - 1)
            return Fraction(numerator=0, denominator=1, integerPart=integer_part)
        else:
            # 生成真分数
            denominator = random.randint(2, self.range - 1)
            numerator = random.randint(1, denominator - 1)
            return Fraction(numerator=numerator, denominator=denominator, integerPart=0)

    def generate_expression(self, max_op_count):
        """递归生成算术表达式"""
        if max_op_count == 0:
            # 基础数字（无运算符）
            num = self.generate_number()
            return (str(num), num)

        # 随机生成运算符数量
        op_count = random.randint(1, max_op_count)
        # 拆分左右表达式的运算符数量
        left_op_count = random.randint(0, op_count - 1)
        right_op_count = op_count - 1 - left_op_count

        # 递归生成左右表达式
        left_expr, left_val = self.generate_expression(left_op_count)
        right_expr, right_val = self.generate_expression(right_op_count)

        # 随机选择运算符
        operator = random.choice(self.operators)
        result = None

        # 计算结果
        match operator:
            case '+':
                result = left_val + right_val
            case '-':
                # 确保减法结果非负
                if left_val < right_val:
                    left_expr, right_expr = right_expr, left_expr
                    left_val, right_val = right_val, left_val
                result = left_val - right_val
            case '×':
                result = left_val * right_val
            case '÷':
                # 确保除数不为0
                if right_val.is_zero():
                    return self.generate_expression(max_op_count)
                result = left_val / right_val
            case _:
                raise ValueError(f"不支持的运算符 '{operator}'")

        # 包装为带括号的表达式
        return (f"({left_expr} {operator} {right_expr})", result)


class ExerciseChecker:
    """批改练习题答案"""

    @staticmethod
    def tokenize(exercise):
        """将表达式分词"""
        tokens = []
        current = ""
        for char in exercise:
            if char in '()+-×÷':
                if current.strip():
                    tokens.append(current.strip())
                    current = ""
                tokens.append(char)
            else:
                current += char
        if current.strip():
            tokens.append(current.strip())
        return tokens

    @staticmethod
    def parse_fraction(token):
        """解析分数字符串为Fraction对象"""
        try:
            return Fraction.from_string(token)
        except:
            return None

    @staticmethod
    def parse_exercise(exercise):
        """解析并计算表达式结果"""
        try:
            valid_ops = {'+', '-', '×', '÷', '(', ')'}
            tokens = ExerciseChecker.tokenize(exercise)

            # 检查非法符号
            for token in tokens:
                if token in valid_ops:
                    continue
                if not re.fullmatch(r'^\d+$|^\d+\'\d+/\d+$|^\d+/\d+$', token):
                    return None

            # 查找匹配的括号
            def find_matching_parenthesis(tokens, start):
                count = 1
                for i in range(start + 1, len(tokens)):
                    if tokens[i] == '(':
                        count += 1
                    elif tokens[i] == ')':
                        count -= 1
                        if count == 0:
                            return i
                return -1  # 缺少右括号

            # 递归计算表达式
            def evaluate(tokens):
                if not tokens:
                    return None

                # 处理括号
                i = 0
                while i < len(tokens):
                    if tokens[i] == '(':
                        j = find_matching_parenthesis(tokens, i)
                        if j == -1:
                            return None
                        inner_result = evaluate(tokens[i + 1:j])
                        if inner_result is None:
                            return None
                        tokens = tokens[:i] + [str(inner_result)] + tokens[j + 1:]
                    else:
                        i += 1

                # 单数字直接返回
                if len(tokens) == 1:
                    return ExerciseChecker.parse_fraction(tokens[0])

                # 先处理乘除
                for i in range(len(tokens) - 1, -1, -1):
                    if tokens[i] in ['×', '÷']:
                        left = evaluate(tokens[:i])
                        right = evaluate(tokens[i + 1:])
                        if left is None or right is None:
                            return None
                        if tokens[i] == '×':
                            return left * right
                        elif tokens[i] == '÷':
                            if right.is_zero():
                                return None
                            return left / right

                # 再处理加减
                for i in range(len(tokens) - 1, -1, -1):
                    if tokens[i] in ['+', '-']:
                        left = evaluate(tokens[:i])
                        right = evaluate(tokens[i + 1:])
                        if left is None or right is None:
                            return None
                        if tokens[i] == '+':
                            return left + right
                        elif tokens[i] == '-':
                            result = left - right
                            if result is None or result.frac < 0:
                                return None
                            return result

                return None

            return evaluate(tokens)
        except:
            return None

    @staticmethod
    def check_answers(exercise_file, answer_file):
        """检查答案并生成评分结果"""
        correct = []
        wrong = []

        try:
            # 读取题目
            with open(exercise_file, 'r', encoding='utf-8') as f:
                exercises = []
                for line in f:
                    line = line.strip()
                    if line:
                        parts = line.split('.', 1)
                        if len(parts) == 2:
                            expr = parts[1].strip().replace(' =', '')
                            exercises.append(expr)

            # 读取答案
            with open(answer_file, 'r', encoding='utf-8') as f:
                answers = []
                for line in f:
                    line = line.strip()
                    if line:
                        parts = line.split('.', 1)
                        if len(parts) == 2:
                            ans = parts[1].strip()
                            answers.append(ans)

            # 校验数量匹配
            if len(exercises) != len(answers):
                raise Exception("错误：题目与答案数量不匹配。")

            # 批改每道题
            for i in range(len(exercises)):
                calc_result = ExerciseChecker.parse_exercise(exercises[i])
                user_ans = ExerciseChecker.parse_fraction(answers[i])

                if (calc_result is not None and
                        user_ans is not None and
                        calc_result == user_ans):
                    correct.append(str(i + 1))
                else:
                    wrong.append(str(i + 1))

            # 生成评分文件
            with open('Grade.txt', 'w', encoding='utf-8') as f:
                f.write(f"Correct: {len(correct)} ({', '.join(sorted(correct, key=int))})\n")
                f.write(f"Wrong: {len(wrong)} ({', '.join(sorted(wrong, key=int))})\n")

            return correct, wrong

        except Exception as e:
            print(f"批改错误: {e}")
            raise