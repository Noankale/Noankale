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

    for i in range(num):
      # 生成一道题目
      exercise,answer = self.generate_expression(3)
      if exercise.startswith('(') and exercise.endswith(')'):
        exercise = exercise[1:-1]
      if self.is_Unique(exercise):
        exercise = f"{i+1}. {exercise}"
        exercises.append(f"{exercise} = ")
        answer = f"{i+1}. {answer}"
        answers.append(str(answer))
      

    return exercises,answers 

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

  # 检查题目方法
  def check_answers(exerciseFile,answerFile):
    correct = []
    wrong = []

    # 打开习题和答案，利用等号进行分割字符处理
    try:

      with open(exerciseFile,'r',encoding='utf-8') as ef:
        exercises = []
        for line in ef:
          exercise = line.strip()
          if exercise:
            exercises.append(exercise.replace(' =',''))

      with open(answerFile,'r',encoding='utf-8') as af:
        answers = []
        for line in af:
          answer = line.strip()
          if answer:
            answers.append(answer)
        return
      
      if len(exercises) != len(answers):
        raise Exception("错误：题目与答案数量不匹配。")

      for i in range(length):
        exercise = exercises[i]
        answer = answers[i]

        if "=" not in exercise:
          raise Exception()
      
    except Exception as e:
      print(e)
    return