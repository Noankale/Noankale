import pytest
from fraction import Fraction


class TestFraction:
    """测试分数类的所有功能（覆盖小学场景及代码全分支）"""

    def test_initialization(self):
        """测试初始化（整数、真分数、带分数、分母非零校验）"""
        # 整数初始化
        f_int = Fraction(0, 1, 5)
        assert f_int.frac.numerator == 5
        assert f_int.frac.denominator == 1

        # 真分数初始化
        f_proper = Fraction(1, 2)
        assert f_proper.frac.numerator == 1
        assert f_proper.frac.denominator == 2

        # 带分数初始化（2'1/3 = 7/3）
        f_mixed = Fraction(1, 3, 2)
        assert f_mixed.frac.numerator == 7
        assert f_mixed.frac.denominator == 3

        # 分母为0的错误（应抛出异常）
        with pytest.raises(ValueError):
            Fraction(1, 0)

        # 补充：分子为0的真分数
        f_zero_proper = Fraction(0, 5)
        assert f_zero_proper.frac.numerator == 0
        assert f_zero_proper.frac.denominator == 1

        # 补充：分数部分为0的带分数
        f_mixed_zero = Fraction(0, 3, 2)
        assert f_mixed_zero.frac == Fraction(0, 1, 2).frac

    def test_from_string(self):
        """测试从字符串解析（纯分数、带分数、整数、负号处理）"""
        test_cases = [
            ("3/4", Fraction(3, 4)),  # 纯分数
            ("2'1/3", Fraction(1, 3, 2)),  # 带分数
            ("5", Fraction(0, 1, 5)),  # 整数
            ("-2'1/3", Fraction(1, 3, -2)),  # 负带分数
            ("-3/4", Fraction(-3, 4)),  # 负纯分数
            # 补充：特殊格式
            ("0", Fraction(0, 1)),  # 零字符串
            ("0'0/1", Fraction(0, 1, 0)),  # 零的带分数形式
            ("3'0/5", Fraction(0, 5, 3)),  # 整数的带分数形式
        ]
        for s, expected in test_cases:
            assert Fraction.from_string(s).frac == expected.frac

    def test_to_improper(self):
        """测试转换为假分数"""
        # 带分数转假分数
        f = Fraction(1, 3, 2)
        improper = f.to_improper()
        assert improper.numerator == 7
        assert improper.denominator == 3

        # 真分数转假分数（本身就是假分数形式）
        f = Fraction(1, 2)
        improper = f.to_improper()
        assert improper.numerator == 1
        assert improper.denominator == 2

        # 整数转假分数
        f = Fraction(0, 1, 5)
        improper = f.to_improper()
        assert improper.numerator == 5
        assert improper.denominator == 1

        # 补充：负带分数转假分数
        f_neg_mixed = Fraction(1, 3, -2)
        assert f_neg_mixed.to_improper().numerator == -7
        assert f_neg_mixed.to_improper().denominator == 3

    def test_arithmetic_operations(self):
        """测试四则运算（非负结果、除零保护）"""
        # 加法
        assert (Fraction(1, 2) + Fraction(1, 3)).frac == Fraction(5, 6).frac
        assert (Fraction(0, 1, 2) + Fraction(1, 2)).frac == Fraction(5, 2).frac  # 2 + 1/2 = 5/2
        assert (Fraction(1, 2) + 1).frac == Fraction(3, 2).frac  # 与int相加
        # 补充：加法结果为整数
        assert (Fraction(1, 2) + Fraction(1, 2)).frac == Fraction(0, 1, 1).frac

        # 减法（非负结果）
        assert (Fraction(3, 4) - Fraction(1, 4)).frac == Fraction(1, 2).frac
        assert (Fraction(0, 1, 5) - Fraction(0, 1, 3)).frac == Fraction(0, 1, 2).frac
        assert (Fraction(1, 2) - Fraction(3, 4)) is None  # 负数结果返回None
        assert (Fraction(3, 2) - 1).frac == Fraction(1, 2).frac  # 与int相减
        # 补充：减法结果为零
        assert (Fraction(1, 2) - Fraction(1, 2)).frac == Fraction(0, 1, 0).frac

        # 乘法
        assert (Fraction(2, 3) * Fraction(3, 4)).frac == Fraction(1, 2).frac
        assert (Fraction(0, 1, 2) * Fraction(1, 3)).frac == Fraction(2, 3).frac
        assert (Fraction(1, 2) * 3).frac == Fraction(3, 2).frac  # 与int相乘
        # 补充：乘法结果为零
        assert (Fraction(1, 2) * Fraction(0, 1, 0)).frac == Fraction(0, 1, 0).frac

        # 除法
        assert (Fraction(1, 2) / Fraction(3, 4)).frac == Fraction(2, 3).frac
        assert (Fraction(0, 1, 4) / Fraction(0, 1, 2)).frac == Fraction(0, 1, 2).frac
        assert (Fraction(3, 2) / 3).frac == Fraction(1, 2).frac  # 与int相除
        assert (Fraction(1, 2) / Fraction(0, 1, 0)) is None  # 除零返回None

    def test_comparison_operators(self):
        """测试所有比较运算符（Fraction与Fraction、Fraction与int）"""
        # Fraction与Fraction
        assert Fraction(1, 2) < Fraction(3, 4)
        assert Fraction(3, 4) > Fraction(1, 2)
        assert Fraction(0, 1, 5) == Fraction(0, 1, 5)
        assert Fraction(3, 2) >= Fraction(0, 1, 1)  # 3/2 >= 1
        assert Fraction(1, 2) <= Fraction(3, 4)

        # Fraction与int
        assert Fraction(1, 2) < 1
        assert Fraction(3, 2) > 1
        assert Fraction(5, 1) == 5
        assert Fraction(3, 2) >= 1
        assert Fraction(1, 2) <= 1

        # 补充：不同形式的相等比较
        assert Fraction(2, 4) == Fraction(1, 2)  # 可约分分数相等
        assert Fraction(0, 1, 2) == Fraction(4, 2)  # 整数与分数相等

        # 补充：负分数比较
        assert Fraction(-3, 2) < Fraction(-1, 2)
        assert Fraction(-1, 3) > Fraction(-1, 2)

        # 补充：与零比较
        assert Fraction(1, 2) > 0
        assert Fraction(-1, 2) < 0

    def test_invalid_type_comparison(self):
        """测试与无法转换的类型比较（补充未覆盖的except分支）"""
        # 与字符串比较（无法转换为Fraction）
        with pytest.raises(TypeError):
            Fraction(1, 2) < "not_a_fraction"

        # 与自定义对象比较（无法转换为Fraction）
        class InvalidType:
            pass

        with pytest.raises(TypeError):
            Fraction(1, 2) == InvalidType()

    def test_string_representation(self):
        """测试字符串格式化（纯分数、带分数、整数、负数）"""
        assert str(Fraction(0, 1, 5)) == "5"  # 整数
        assert str(Fraction(1, 2)) == "1/2"  # 纯分数
        assert str(Fraction(1, 3, 2)) == "2'1/3"  # 带分数
        assert str(Fraction(0, 1, 0)) == "0"  # 零
        assert str(Fraction(-1, 2)) == "-1/2"  # 负纯分数
        assert str(Fraction(1, 3, -2)) == "-2'1/3"  # 负带分数
        # 补充：可约分分数的格式化
        assert str(Fraction(2, 4)) == "1/2"  # 纯分数约分
        assert str(Fraction(4, 2)) == "2"  # 分数约分为整数

    def test_is_zero(self):
        """测试是否为零"""
        assert Fraction(0, 1, 0).is_zero()
        assert not Fraction(1, 2).is_zero()
        assert not Fraction(0, 1, 5).is_zero()
        assert not Fraction(-1, 2).is_zero()
        # 补充：其他零的形式
        assert Fraction(0, 5).is_zero()  # 0/5
        assert Fraction(0, 3, 0).is_zero()  # 0'0/3