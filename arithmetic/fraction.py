from fractions import Fraction as PyFraction

class Fraction:
  def __init__(self,numerator,denominator=1,integerPart=0):
    totalNumerator = integerPart * denominator + numerator
    self.frac = PyFraction(totalNumerator,denominator)

  @classmethod
  def from_string(cls, s):
      # 拆解分数
      if "'" in s:
          integer_part, fraction_part = s.split("'")
          integer_part = int(integer_part)
      else:
          integer_part = 0
          fraction_part = s
      
      if "/" in fraction_part:
          num, den = fraction_part.split("/")
          num, den = int(num), int(den)
      else:
          num = int(fraction_part)
          den = 1
      
      # 处理符号（整数部分为负时，分数部分也为负）
      if integer_part < 0:
          num = -num
      
      return cls(num, den, integer_part)
  
  def to_improper(self):
      # 返回假分数
      return self.frac
  
  def is_zero(self):
      return self.frac == 0
  
  def __add__(self, other):
      if not isinstance(other, Fraction):
          other = Fraction(other)
      result = self.frac + other.frac
      return Fraction(result.numerator, result.denominator)
  
  def __sub__(self, other):
      if not isinstance(other, Fraction):
          other = Fraction(other)
      if self.frac < other.frac:
          return None  # 不返回负数
      result = self.frac - other.frac
      return Fraction(result.numerator, result.denominator)
  
  def __mul__(self, other):
      if not isinstance(other, Fraction):
          other = Fraction(other)
      result = self.frac * other.frac
      return Fraction(result.numerator, result.denominator)
  
  def __truediv__(self, other):
      if not isinstance(other, Fraction):
          other = Fraction(other)
      if other.is_zero():
          return None
      result = self.frac / other.frac
      return Fraction(result.numerator, result.denominator)
  
  def __lt__(self, other):
      if not isinstance(other, Fraction):
          other = Fraction(other)
      return self.frac < other.frac
  
  def __eq__(self, other):
      if not isinstance(other, Fraction):
          other = Fraction(other)
      return self.frac == other.frac
  
  def __str__(self):
      # 转换为带分数
      if self.is_zero():
          return "0"
      
      numerator = self.frac.numerator
      denominator = self.frac.denominator
      integer_part = numerator // denominator
      remainder = numerator % denominator
      
      if remainder == 0:
          return str(integer_part)
      
      # 处理符号
      sign = "-" if integer_part < 0 or remainder < 0 else ""
      abs_integer = abs(integer_part)
      abs_remainder = abs(remainder)
      
      parts = []
      if abs_integer != 0:
          parts.append(f"{sign}{abs_integer}")
      else:
          parts.append(sign)
      
      parts.append(f"{abs_remainder}/{denominator}")
      
      # 合并带分数
      return "'".join(parts) if abs_integer != 0 else ''.join(parts)