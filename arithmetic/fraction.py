from fractions import Fraction as PyFraction


class Fraction:
    def __init__(self, numerator, denominator=1, integerPart=0):
        """初始化分数（支持整数、真分数、带分数）"""
        if denominator == 0:
            raise ValueError("分母不能为0")
        # 处理负带分数：整数部分为负时，分数部分也应为负
        if integerPart < 0:
            numerator = -abs(numerator)  # 分数部分取负
        total_numerator = integerPart * denominator + numerator
        self.frac = PyFraction(total_numerator, denominator)

    @classmethod
    def from_string(cls, s):
        """从字符串解析分数（支持负带分数、负纯分数）"""
        if "'" in s:
            integer_part_str, fraction_part = s.split("'")
            integer_part = int(integer_part_str)
        else:
            integer_part = 0
            fraction_part = s

        if "/" in fraction_part:
            num_str, den_str = fraction_part.split("/")
            numerator = int(num_str)
            denominator = int(den_str)
        else:
            numerator = int(fraction_part)
            denominator = 1

        return cls(numerator, denominator, integer_part)

    def to_improper(self):
        return self.frac

    def is_zero(self):
        return self.frac == 0

    # ---------------------- 四则运算 ----------------------
    def __add__(self, other):
        if not isinstance(other, Fraction):
            other = Fraction(other)
        result = self.frac + other.frac
        return Fraction(result.numerator, result.denominator)

    def __sub__(self, other):
        if not isinstance(other, Fraction):
            other = Fraction(other)
        if self.frac < other.frac:
            return None  # 禁止负数结果
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
            return None  # 禁止除以零
        result = self.frac / other.frac
        return Fraction(result.numerator, result.denominator)

    # ---------------------- 比较运算符 ----------------------
    def _convert_other(self, other):
        if not isinstance(other, Fraction):
            try:
                other = Fraction(other)
            except (ValueError, TypeError):
                raise TypeError(f"无法比较 Fraction 与 {type(other).__name__} 类型")
        return other

    def __lt__(self, other):
        other = self._convert_other(other)
        return self.frac < other.frac

    def __gt__(self, other):
        other = self._convert_other(other)
        return self.frac > other.frac

    def __eq__(self, other):
        other = self._convert_other(other)
        return self.frac == other.frac

    def __le__(self, other):
        other = self._convert_other(other)
        return self.frac <= other.frac

    def __ge__(self, other):
        other = self._convert_other(other)
        return self.frac >= other.frac

    # ---------------------- 字符串格式化 ----------------------
    def __str__(self):
        if self.is_zero():
            return "0"

        numerator = self.frac.numerator
        denominator = self.frac.denominator

        # 处理负数：区分负纯分数和负带分数
        if numerator < 0:
            abs_num = abs(numerator)
            abs_integer = abs_num // denominator  # 绝对值的整数部分
            abs_remainder = abs_num % denominator  # 绝对值的分数部分分子

            # 情况1：负纯分数（整数部分为0）→ 格式：-分子/分母
            if abs_integer == 0:
                return f"-{abs_remainder}/{denominator}"
            # 情况2：负带分数（整数部分非0）→ 格式：-整数'分数
            else:
                return f"-{abs_integer}'{abs_remainder}/{denominator}"

        # 处理正数：区分正纯分数和正带分数
        integer_part = numerator // denominator
        remainder = numerator % denominator

        # 情况1：正整数
        if remainder == 0:
            return str(integer_part)
        # 情况2：正纯分数
        elif integer_part == 0:
            return f"{remainder}/{denominator}"
        # 情况3：正带分数
        else:
            return f"{integer_part}'{remainder}/{denominator}"