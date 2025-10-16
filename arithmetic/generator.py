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
      if self.is_Unique(exercise):
        exercises.append(f"{exercise} = ")
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
                
        # 对于更复杂的表达式，我们可以使用哈希来简化比较
        return hashlib.md5(exercise.encode()).hexdigest()
    except:
        return hashlib.md5(exercise.encode()).hexdigest()


  def is_Unique(self,exercise:str):
    if exercise.startswith('(') and exercise.endswith(')'):
      exercise = exercise[1:-1]
    normalizedExercise = self.normalized_exercise(exercise)
    if normalizedExercise not in self.hashList:
       self.hashList.add(normalizedExercise)
       return True
    return False
    pass

  # 通过分数类生成一个数字
  def generate_number(self):
    return random.randint()

  # 生成算术表达式
  def generate_expression(self,maxOpCount):
    if maxOpCount == 0:
      num = self.generate_number()
      return (str(num),num)
    
    # 随机生成表达式操作符数量
    opCount = random.randint(1,maxOpCount)
    # 递归生成左右表达式
    leftExpression, leftVal = self.generate_expression(opCount - 1)
    rightExpression, rightVal = self.generate_expression(opCount - 1)

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
      
      
    except Exception as e:
      print(e)
    return