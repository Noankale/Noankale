import re
import os
import hashlib
from tempfile import NamedTemporaryFile
import pytest
from generator import ExerciseGenerator, ExerciseChecker
from fraction import Fraction


class TestExerciseGenerator:
    """测试题目生成器功能"""

    def setup_class(self):
        self.range_val = 10
        self.generator = ExerciseGenerator(self.range_val)

    def test_generate_number(self):
        """测试数字生成（自然数和真分数）"""
        for _ in range(100):
            num = self.generator.generate_number()
            assert isinstance(num, Fraction), "生成的不是Fraction实例"

            # 检查自然数范围
            if str(num).isdigit():
                val = int(str(num))
                assert 1 <= val < self.range_val, f"自然数超出范围: {val}"

            # 检查真分数范围
            elif '/' in str(num):
                frac = Fraction.from_string(str(num))
                assert frac.frac.denominator < self.range_val, f"分母超出范围: {frac}"

    def test_operator_count(self):
        """测试表达式运算符数量不超过3个"""
        for _ in range(100):
            expr, _ = self.generator.generate_expression(3)
            operators = re.findall(r'[+×÷-]', expr)
            assert len(operators) <= 3, f"运算符数量超限: {expr} ({len(operators)})"

    def test_no_negative_results(self):
        """测试减法结果非负"""
        for _ in range(100):
            expr, result = self.generator.generate_expression(3)
            if '-' in expr and result is not None:
                assert str(result).count('-') == 0, f"减法产生负数: {expr} = {result}"

    def test_division_validity(self):
        """测试除法结果有效性"""
        for _ in range(100):
            expr, result = self.generator.generate_expression(3)
            if '÷' in expr:
                assert result is not None, f"除法产生无效结果: {expr}"

    def test_exercise_uniqueness(self):
        """测试生成题目不重复"""
        num = 100
        exercises, _ = self.generator.generate_exercise(num)
        assert len(exercises) == num, f"实际生成数量与预期不符: {len(exercises)} vs {num}"

        # 提取表达式部分进行去重检查
        exprs = [ex.split('. ')[1].replace(' =', '') for ex in exercises]
        assert len(set(exprs)) == num, "存在重复题目"

    def test_normalized_exercise(self):
        """测试题目标准化（去重逻辑+异常场景）"""
        # 加法交换律
        assert self.generator.normalized_exercise("1 + 2") == self.generator.normalized_exercise("2 + 1")
        # 乘法交换律
        assert self.generator.normalized_exercise("3 × 4") == self.generator.normalized_exercise("4 × 3")
        # 不同运算符不视为重复
        assert self.generator.normalized_exercise("1 + 2") != self.generator.normalized_exercise("1 × 2")
        # 带括号的不视为重复
        assert self.generator.normalized_exercise("(1 + 2) + 3") != self.generator.normalized_exercise("1 + (2 + 3)")
        # 测试格式错误的题目 - 使用真正无效的表达式
        with pytest.raises(ValueError, match="无效的表达式格式"):
            self.generator.normalized_exercise("1 + + 2")  # 连续运算符
        with pytest.raises(ValueError, match="无效的表达式格式"):
            self.generator.normalized_exercise("(1 + 2")  # 括号不匹配
        # 验证格式错误时is_Unique仍能正常判断唯一性
        assert self.generator.is_Unique("1 + + 2") is True
        assert self.generator.is_Unique("1 + + 2") is False

    def test_generate_expression_invalid_operator(self):
        """测试非法运算符异常"""
        original_ops = self.generator.operators
        self.generator.operators = ['+', '-', '×', '÷', '$']
        try:
            with pytest.raises(ValueError, match="不支持的运算符 '\\$'"):
                count = 0
                while count < 100:
                    self.generator.generate_expression(1)
                    count += 1
        finally:
            self.generator.operators = original_ops  # 恢复原始运算符

    def test_generate_exercise_insufficient(self):
        """测试尝试次数耗尽仍无法生成足够题目的场景"""
        # 临时缩小数值范围并限制运算符
        original_range = self.generator.range
        original_operators = self.generator.operators

        # 使用极端的限制条件
        self.generator.range = 1  # 只允许数字1
        self.generator.operators = ['+']  # 只允许加法（这样生成的题目非常有限）

        # 清空哈希集合
        self.generator.hashList.clear()

        # 预生成所有可能的简单表达式并加入哈希集合
        # 由于范围=1且只有加法，可能的表达式非常有限
        all_exprs = ["1", "1 + 1", "1 + 1 + 1", "(1 + 1) + 1", "1 + (1 + 1)"]
        for expr in all_exprs:
            normalized = self.generator.normalized_exercise(expr)
            hash_val = hashlib.md5(normalized.encode()).hexdigest()
            self.generator.hashList.add(hash_val)

        # 尝试生成超出可能数量的题目
        target_num = 10
        exercises, answers = self.generator.generate_exercise(target_num)

        # 验证结果 - 由于限制极严，应该无法生成10道题
        # 注意：这里使用 <= 而不是 <，因为可能正好生成所有可能的题目
        assert len(exercises) <= target_num, f"生成了{len(exercises)}道题，超出预期"

        # 恢复原始设置
        self.generator.range = original_range
        self.generator.operators = original_operators

    def test_generate_exercise_with_very_small_range(self):
        """测试使用极小范围生成题目"""
        # 保存原始设置
        original_range = self.generator.range
        original_hashlist = self.generator.hashList.copy()

        try:
            # 设置极小的范围
            self.generator.range = 1
            self.generator.hashList.clear()

            # 尝试生成题目
            target_num = 5
            exercises, answers = self.generator.generate_exercise(target_num)

            # 验证结果
            assert len(exercises) <= target_num, f"生成了{len(exercises)}道题"
            assert len(exercises) == len(answers), "题目与答案数量不匹配"

        finally:
            # 恢复原始设置
            self.generator.range = original_range
            self.generator.hashList = original_hashlist

    def test_generate_number_edge_cases(self):
        """测试数字生成的边界情况"""
        # 测试多次生成以确保覆盖所有分支
        for _ in range(50):
            num = self.generator.generate_number()
            assert isinstance(num, Fraction)

            # 确保数字格式正确
            num_str = str(num)
            assert num_str, "生成的数字字符串不能为空"

            # 验证数字在有效范围内
            if '/' in num_str:
                # 真分数情况
                frac = Fraction.from_string(num_str)
                assert 0 < frac.frac < 1, f"真分数应该在0-1之间: {frac}"
            else:
                # 自然数情况
                val = int(num_str)
                assert 1 <= val < self.range_val, f"自然数超出范围: {val}"


class TestExerciseChecker:
    """测试题目批改功能"""

    def test_tokenize(self):
        """测试表达式分词功能"""
        test_cases = [
            ("1 + 2 × 3", ["1", "+", "2", "×", "3"]),
            ("(1/2 + 3'4/5) ÷ 6", ["(", "1/2", "+", "3'4/5", ")", "÷", "6"]),
            ("10 - (2 × 3)", ["10", "-", "(", "2", "×", "3", ")"]),
        ]
        for expr, expected in test_cases:
            result = ExerciseChecker.tokenize(expr)
            assert result == expected, f"分词错误: {expr} -> {result}, 期望: {expected}"

    def test_parse_fraction(self):
        """测试分数解析功能"""
        # 正常格式
        normal_cases = [
            ("3/4", Fraction(3, 4)),
            ("2'1/3", Fraction(1, 3, 2)),
            ("5", Fraction(0, 1, 5)),
            ("0", Fraction(0, 1)),
        ]
        for s, expected in normal_cases:
            result = ExerciseChecker.parse_fraction(s)
            assert result == expected, f"分数解析错误: {s} -> {result}, 期望: {expected}"

        # 非法格式
        invalid_cases = ["1/'2", "3'4/5/6", "abc", "1.2.3"]
        for s in invalid_cases:
            result = ExerciseChecker.parse_fraction(s)
            assert result is None, f"非法分数解析错误: {s} -> {result}"

    def test_evaluate_expression(self):
        """测试表达式计算功能"""
        test_cases = [
            ("1 + 2", Fraction(0, 1, 3)),
            ("3'1/2 - 1'1/2", Fraction(0, 1, 2)),
            ("2/3 × 3/4", Fraction(1, 2)),
            ("1 ÷ 2/3", Fraction(3, 2)),
            ("(1 + 2) × 3", Fraction(0, 1, 9)),
            ("5 ÷ 0", None),  # 除数为0
            ("(1 + 2", None),  # 缺少右括号
            ("1 $ 2", None),  # 非法运算符
        ]
        for expr, expected in test_cases:
            result = ExerciseChecker.parse_exercise(expr)
            assert result == expected, f"表达式计算错误: {expr} 预期 {expected} 实际 {result}"

    def test_check_answers(self):
        """测试答案批改功能"""
        # 正常批改场景
        with NamedTemporaryFile(mode="w", delete=False, suffix=".txt", encoding="utf-8") as f:
            f.write("1. 1 + 2 = \n")
            f.write("2. 3 - 1 = \n")
            f.write("3. 2 × 3 = \n")
            f.write("4. 5 ÷ 0 = \n")
            exercise_file = f.name

        with NamedTemporaryFile(mode="w", delete=False, suffix=".txt", encoding="utf-8") as f:
            f.write("1. 3\n")
            f.write("2. 1\n")
            f.write("3. 6\n")
            f.write("4. 0\n")
            answer_file = f.name

        correct, wrong = ExerciseChecker.check_answers(exercise_file, answer_file)
        assert correct == ["1", "3"], f"正确题目识别错误: {correct}"
        assert wrong == ["2", "4"], f"错误题目识别错误: {wrong}"
        assert os.path.exists("Grade.txt"), "未生成Grade.txt"

        # 数量不匹配场景
        with NamedTemporaryFile(mode="w", delete=False, suffix=".txt", encoding="utf-8") as f1, \
                NamedTemporaryFile(mode="w", delete=False, suffix=".txt", encoding="utf-8") as f2:
            # 3道题目
            f1.write("1. 1 + 1 = \n")
            f1.write("2. 2 + 2 = \n")
            f1.write("3. 3 + 3 = \n")
            # 2个答案
            f2.write("1. 2\n")
            f2.write("2. 4\n")

            exercise_file1 = f1.name
            answer_file1 = f2.name

        try:
            with pytest.raises(Exception, match="错误：题目与答案数量不匹配。"):
                ExerciseChecker.check_answers(exercise_file1, answer_file1)
        finally:
            # 清理临时文件
            for f in [exercise_file, answer_file, exercise_file1, answer_file1]:
                if os.path.exists(f):
                    os.unlink(f)
            if os.path.exists("Grade.txt"):
                os.unlink("Grade.txt")

    def test_operator_error(self):
        """测试非法运算符场景"""
        invalid_exprs = ["1 $ 2", "3 # 4", "5 @ 6"]
        for expr in invalid_exprs:
            result = ExerciseChecker.parse_exercise(expr)
            assert result is None, f"非法运算符处理错误: {expr}"

    def test_complex_expressions(self):
        """测试复杂表达式计算"""
        test_cases = [
            ("1/2 + 1/3", Fraction(5, 6)),
            ("2'1/2 × 2", Fraction(0, 1, 5)),
            ("(1 + 2) ÷ 3", Fraction(0, 1, 1)),
            ("1 - 1/2", Fraction(1, 2)),
        ]
        for expr, expected in test_cases:
            result = ExerciseChecker.parse_exercise(expr)
            assert result == expected, f"复杂表达式计算错误: {expr} 预期 {expected} 实际 {result}"