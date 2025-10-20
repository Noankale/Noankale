import pytest
import tempfile
import os
from unittest.mock import patch, MagicMock
from main import write_to_file, main


class TestMain:
    """测试主程序功能"""

    def test_write_to_file_success(self):
        """测试文件写入成功"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            temp_file = f.name

        try:
            content = ["line1", "line2", "line3"]
            result = write_to_file(temp_file, content)
            assert result is True

            # 验证文件内容
            with open(temp_file, 'r', encoding='utf-8') as f:
                written_content = f.read()
            expected_content = "line1\nline2\nline3\n"
            assert written_content == expected_content
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)

    def test_write_to_file_failure(self):
        """测试文件写入失败"""
        # 尝试写入到受保护的目录（应该会失败）
        content = ["test"]
        result = write_to_file("/root/test_write.txt", content)
        assert result is False

    def test_main_generation_mode_success(self):
        """测试生成模式成功"""
        with patch('main.ExerciseGenerator') as mock_generator:
            mock_instance = MagicMock()
            mock_generator.return_value = mock_instance
            mock_instance.generate_exercise.return_value = (
                ["1. 1 + 1 =", "2. 2 + 2 ="],
                ["1. 2", "2. 4"]
            )

            # 模拟文件写入成功
            with patch('main.write_to_file') as mock_write:
                mock_write.return_value = True

                with patch('sys.argv', ['main.py', '-n', '10', '-r', '10']):
                    with patch('builtins.print') as mock_print:
                        result = main()

                        assert result == 0
                        mock_generator.assert_called_once_with(10)
                        mock_instance.generate_exercise.assert_called_once_with(10)
                        assert mock_write.call_count == 2

    def test_main_generation_mode_file_write_failure(self):
        """测试生成模式文件写入失败"""
        with patch('main.ExerciseGenerator') as mock_generator:
            mock_instance = MagicMock()
            mock_generator.return_value = mock_instance
            mock_instance.generate_exercise.return_value = (
                ["1. 1 + 1 ="],
                ["1. 2"]
            )

            # 模拟文件写入失败
            with patch('main.write_to_file') as mock_write:
                mock_write.return_value = False

                with patch('sys.argv', ['main.py', '-n', '5', '-r', '5']):
                    with patch('builtins.print') as mock_print:
                        result = main()

                        assert result == 0  # 主程序应该继续执行
                        mock_write.assert_called()

    def test_main_grading_mode_success(self):
        """测试批改模式成功"""
        with patch('main.ExerciseChecker') as mock_checker:
            mock_checker.check_answers.return_value = (['1', '3'], ['2', '4'])

            with patch('sys.argv', ['main.py', '-e', 'exercises.txt', '-a', 'answers.txt']):
                with patch('builtins.print') as mock_print:
                    result = main()

                    assert result == 0
                    mock_checker.check_answers.assert_called_once_with('exercises.txt', 'answers.txt')

    def test_main_invalid_arguments_both_modes(self):
        """测试同时提供生成和批改参数"""
        with patch('sys.argv', ['main.py', '-n', '10', '-r', '10', '-e', 'exercises.txt']):
            with patch('builtins.print') as mock_print:
                result = main()

                assert result == 1
                # 检查最后一次调用是否包含错误消息
                last_call_args = mock_print.call_args_list[-1][0][0]
                assert "不能同时使用生成模式和批改模式参数" in str(last_call_args)

    def test_main_generation_mode_missing_args(self):
        """测试生成模式缺少参数"""
        test_cases = [
            (['main.py', '-n', '10'], "缺少 -r 参数"),
            (['main.py', '-r', '10'], "缺少 -n 参数"),
        ]

        for argv, expected_error in test_cases:
            with patch('sys.argv', argv):
                with patch('builtins.print') as mock_print:
                    result = main()

                    assert result == 1
                    # 验证错误消息包含关键信息
                    last_call_args = mock_print.call_args_list[-1][0][0]
                    assert "生成模式需要同时提供" in str(last_call_args)

    def test_main_grading_mode_missing_args(self):
        """测试批改模式缺少参数"""
        test_cases = [
            (['main.py', '-e', 'exercises.txt'], "缺少 -a 参数"),
            (['main.py', '-a', 'answers.txt'], "缺少 -e 参数"),
        ]

        for argv, expected_error in test_cases:
            with patch('sys.argv', argv):
                with patch('builtins.print') as mock_print:
                    result = main()

                    assert result == 1
                    last_call_args = mock_print.call_args_list[-1][0][0]
                    assert "批改模式需要同时提供" in str(last_call_args)

    def test_main_invalid_range_parameter(self):
        """测试无效的范围参数"""
        test_cases = [
            (['main.py', '-n', '10', '-r', '0'], "范围参数 r 必须是大于等于1的自然数"),
            (['main.py', '-n', '10', '-r', '-5'], "范围参数 r 必须是大于等于1的自然数"),
            (['main.py', '-n', '0', '-r', '10'], "题目数量 n 必须是大于等于1的自然数"),
        ]

        for argv, expected_error in test_cases:
            with patch('sys.argv', argv):
                with patch('builtins.print') as mock_print:
                    result = main()

                    assert result == 1
                    last_call_args = mock_print.call_args_list[-1][0][0]
                    assert "必须是大于等于1的自然数" in str(last_call_args)

    def test_main_no_arguments(self):
        """测试没有提供任何参数"""
        with patch('sys.argv', ['main.py']):
            with patch('builtins.print') as mock_print:
                result = main()

                assert result == 1
                last_call_args = mock_print.call_args_list[-1][0][0]
                assert "输入参数错误" in str(last_call_args)

    def test_main_generator_exception(self):
        """测试生成器抛出异常的情况"""
        with patch('main.ExerciseGenerator') as mock_generator:
            mock_generator.side_effect = Exception("生成器内部错误")

            with patch('sys.argv', ['main.py', '-n', '10', '-r', '10']):
                with patch('builtins.print') as mock_print:
                    result = main()

                    assert result == 1
                    # 检查最后一次调用是否包含错误消息
                    last_call_args = mock_print.call_args_list[-1][0][0]
                    assert "生成器内部错误" in str(last_call_args)

    def test_main_checker_exception(self):
        """测试批改器抛出异常的情况"""
        with patch('main.ExerciseChecker.check_answers') as mock_checker:
            mock_checker.side_effect = Exception("批改器内部错误")

            with patch('sys.argv', ['main.py', '-e', 'exercises.txt', '-a', 'answers.txt']):
                with patch('builtins.print') as mock_print:
                    result = main()

                    assert result == 1
                    # 检查最后一次调用是否包含错误消息
                    last_call_args = mock_print.call_args_list[-1][0][0]
                    assert "批改器内部错误" in str(last_call_args)

    def test_main_file_not_found(self):
        """测试文件不存在的情况"""
        with patch('sys.argv', ['main.py', '-e', 'nonexistent.txt', '-a', 'nonexistent.txt']):
            with patch('builtins.print') as mock_print:
                result = main()

                assert result == 1
                # 检查最后一次调用是否包含错误消息
                last_call_args = mock_print.call_args_list[-1][0][0]
                # 文件不存在的错误应该被捕获并打印
                assert "No such file or directory" in str(last_call_args)

    def test_main_generation_with_negative_number(self):
        """测试生成模式负数参数"""
        with patch('sys.argv', ['main.py', '-n', '-5', '-r', '10']):
            with patch('builtins.print') as mock_print:
                result = main()

                assert result == 1
                last_call_args = mock_print.call_args_list[-1][0][0]
                assert "必须是大于等于1的自然数" in str(last_call_args)