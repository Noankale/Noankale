# 题目相关处理模块
import random
import hashlib
from fraction import Fraction

# 生成题目与答案
class ExerciseGenerator:
  
  # 初始化
  def __init__(self,range):
    self.range = range
    self.operators = ['+','-','×','÷']
    self.exercises = set()
    self.hashList = set()
    pass

  # 生成题目方法
  def generate_exercise(self,num):
    exercises = []
    answers = []
    count = 0
    i = 0

    while count < num and i < num * 2:  # 防止无限循环
        # 生成一道题目
        exercise, answer = self.generate_expression(3)
        if exercise.startswith('(') and exercise.endswith(')'):
            exercise = exercise[1:-1]
        if self.is_Unique(exercise):
            count += 1
            exercise_str = f"{count}. {exercise}"
            exercises.append(f"{exercise_str} = ")
            answer_str = f"{count}. {answer}"
            answers.append(str(answer_str))
        i += 1
    
    # print(f"实际生成题目数量: {count} (尝试次数: {i})")
    return exercises, answers

  # 标准化题目
  def normalized_exercise(self,exercise):
    try:
        # 检查是否是简单的二元运算
        if exercise.count('+') == 1 and '(' not in exercise and '×' not in exercise and '-' not in exercise and '÷' not in exercise:
            left, right = exercise.split(' + ')
            if left > right:
                exercise = f"{right} + {left}"
                
        if exercise.count('×') == 1 and '(' not in exercise and '+' not in exercise and '-' not in exercise and '÷' not in exercise:
            left, right = exercise.split(' × ')
            if left > right:
                exercise = f"{right} × {left}"
                
        # 使用哈希简化比较
        return hashlib.md5(exercise.encode()).hexdigest()
    except:
        return hashlib.md5(exercise.encode()).hexdigest()


  def is_Unique(self,exercise:str):
    normalizedExercise = self.normalized_exercise(exercise)
    if normalizedExercise not in self.hashList:
       self.hashList.add(normalizedExercise)
       return True
    return False
    pass

  # 通过分数类生成一个数字
  def generate_number(self):
    isInteger = random.choice([True,False])

    if isInteger:
      integerPart = random.randint(1,self.range)
      return Fraction(
        numerator = 0,
        denominator = 1,
        integerPart = integerPart
        )
    else:
      denominator = random.randint(2,self.range)
      numerator = random.randint(1,denominator - 1)
      return Fraction(
        numerator = numerator, 
        denominator = denominator,
        integerPart = 0
        )

  # 生成算术表达式
  def generate_expression(self,maxOpCount):
    if maxOpCount == 0:
      num = self.generate_number()
      return (str(num),num)
    
    # 随机生成表达式操作符数量
    opCount = random.randint(1,maxOpCount)
    # 递归生成左右表达式
    leftOpCount = random.randint( 0,opCount - 1 )
    rightOpCount = opCount - 1 - leftOpCount
    leftExpression, leftVal = self.generate_expression(leftOpCount)
    rightExpression, rightVal = self.generate_expression(rightOpCount)

    # 随机当前操作符
    operator = random.choice(self.operators)

    result = None
    match operator:
      case '+':
        result = leftVal + rightVal
      case '-':
        if leftVal < rightVal:
          leftExpression, rightExpression = rightExpression, leftExpression
          leftVal, rightVal = rightVal, leftVal  
        result = leftVal - rightVal
      case '×':
        result = leftVal * rightVal
      case '÷':
        if rightVal == 0:
           return self.generate_expression(maxOpCount)
        temp = leftVal/rightVal
        result = temp
      case _:
        raise Exception("运算符错误")
      
    expression = f"({leftExpression} {operator} {rightExpression})"
    return (expression, result)


# 批改题目
class ExerciseChecker:
    
    @staticmethod
    # 在运算符未替换时执行分词
    def tokenize(exercise):
        tokens = []
        current = ""
        for char in exercise:
            if char in '()+-×÷':  
                if current and current.strip():
                    tokens.append(current.strip())
                    current = ""
                tokens.append(char)
            else:
                current += char
        if current and current.strip():
            tokens.append(current.strip())
        return tokens
    
    @staticmethod
    # 将分词出的数字转换为Fraction
    def parse_fraction(token):
        try:
            return Fraction.from_string(token)
        except:
            return None
    
    @staticmethod
    # 解析题目
    def parse_exercise(exercise):
        # 对原题目进行分词，得到运算符和数字
        tokens = ExerciseChecker.tokenize(exercise)
        # print(f"分词结果: {expression} -> {tokens}")
        
        def find_matching_parenthesis(tokens, start):
            count = 1
            for i in range(start + 1, len(tokens)):
                if tokens[i] == '(':
                    count += 1
                elif tokens[i] == ')':
                    count -= 1
                    if count == 0:
                        return i
            return -1
        
        def evaluate(tokens):
            if not tokens:
                return None
                
            # 处理括号表达式
            i = 0
            while i < len(tokens):
                if tokens[i] == '(':
                    j = find_matching_parenthesis(tokens, i)
                    if j == -1:
                        return None  # 缺少右括号
                    
                    # 递归计算括号内的表达式
                    inner_result = evaluate(tokens[i+1:j])
                    if inner_result is None:
                        return None
                    
                    # 用结果替换括号表达式
                    tokens = tokens[:i] + [str(inner_result)] + tokens[j+1:]
                else:
                    i += 1
            
            # 如果只有一个token，就是数字
            if len(tokens) == 1:
                return ExerciseChecker.parse_fraction(tokens[0])
            
            # 先处理乘除
            for i in range(len(tokens)-1, -1, -1):
                if tokens[i] in ['×', '÷']:
                    left = evaluate(tokens[:i])
                    right = evaluate(tokens[i+1:])
                    if left is None or right is None:
                        return None
                    
                    if tokens[i] == '×':
                        result = left * right
                        # print(f"  乘法: {left} × {right} = {result}")
                        return result
                    elif tokens[i] == '÷':
                        if right.is_zero():
                            return None
                        result = left / right
                        # print(f"  除法: {left} ÷ {right} = {result}")
                        return result
            
            # 再处理加减
            for i in range(len(tokens)-1, -1, -1):
                if tokens[i] in ['+', '-']:
                    left = evaluate(tokens[:i])
                    right = evaluate(tokens[i+1:])
                    if left is None or right is None:
                        return None
                    
                    if tokens[i] == '+':
                        result = left + right
                        # print(f"  加法: {left} + {right} = {result}")
                        return result
                    elif tokens[i] == '-':
                        result = left - right
                        if result is None or result.frac < 0:
                            return None
                        # print(f"  减法: {left} - {right} = {result}")
                        return result
            
            return None
        
        return evaluate(tokens)
    
    @staticmethod
    def check_answers(exerciseFile, answerFile):
        correct = []
        wrong = []
        
        try:
            with open(exerciseFile,'r',encoding='utf-8') as ef:
                exercises = []
                for line in ef:
                    exercise = line.strip()
                    if exercise:
                        temp = exercise.split('.',1)
                        if len(temp) == 2:
                            temp1 = temp[1].strip().replace(' =','')
                            exercises.append(temp1)

            with open(answerFile,'r',encoding='utf-8') as af:
                answers = []
                for line in af:
                    answer = line.strip()
                    if answer:
                        temp = answer.split('.',1)
                        if len(temp) == 2:
                            temp1 = temp[1].strip()
                            answers.append(temp1)

            # print(f"读取到的题目数量: {len(exercises)}")
            # print(f"读取到的题目数量: {len(answers)}")
            
            if len(exercises) != len(answers):
                raise Exception("错误：题目与答案数量不匹配。")

            length = len(exercises)
            for i in range(length):
                exercise = exercises[i]
                answer = answers[i]
                
                # 计算表达式结果
                calculated_result = ExerciseChecker.parse_exercise(exercise)
                user_answer = ExerciseChecker.parse_fraction(answer)
                
                # print(f"\n第{i+1}题:")
                # print(f"  表达式: {exercise}")
                # print(f"  计算结果: {calculated_result}")
                # print(f"  期望答案: {user_answer}")
                
                # 安全地比较结果
                if (calculated_result is not None and 
                    user_answer is not None and 
                    calculated_result == user_answer):
                    correct.append(str(i+1))
                    # print("正确\n\n")
                else:
                    wrong.append(str(i+1))
                    # print("错误\n\n")
            
            # 输出结果到Grade.txt
            with open('Grade.txt', 'w', encoding='utf-8') as gf:
                gf.write(f"Correct: {len(correct)} ({', '.join(sorted(correct, key=int))})\n")
                gf.write(f"Wrong: {len(wrong)} ({', '.join(sorted(wrong, key=int))})\n")
            
            print(f"\n最终结果:")
            print(f"Correct: {len(correct)} ({', '.join(sorted(correct, key=int))})")
            print(f"Wrong: {len(wrong)} ({', '.join(sorted(wrong, key=int))})")
                
            return correct, wrong
          
        except Exception as e:
            print(f"检查答案时出错: {e}")
            import traceback
            traceback.print_exc()
            return correct, wrong
        
