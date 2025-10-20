import cProfile
import pstats
from main import main
import sys
import os


def ensure_directory(directory):
    """确保目录存在"""
    if not os.path.exists(directory):
        os.makedirs(directory)


def profile_generation():
    """性能分析：题目生成"""
    print("=== 性能分析：题目生成 ===")

    # 确保性能分析目录存在
    ensure_directory('performance_analysis')

    # 临时修改命令行参数
    original_argv = sys.argv
    sys.argv = ['main.py', '-n', '100', '-r', '10']

    # 运行性能分析
    profiler = cProfile.Profile()
    profiler.enable()

    main()  # 调用主函数

    profiler.disable()

    # 保存性能数据到 performance_analysis 文件夹
    profile_path = os.path.join('performance_analysis', 'generate_profile.prof')
    profiler.dump_stats(profile_path)

    # 恢复原始参数
    sys.argv = original_argv

    print(f"性能分析完成！生成文件: {profile_path}")

    # 生成统计报告
    generate_stats_report(profile_path, '题目生成性能分析')


def profile_checking():
    """性能分析：题目批改"""
    print("=== 性能分析：题目批改 ===")

    # 确保性能分析目录存在
    ensure_directory('performance_analysis')

    # 临时修改命令行参数
    original_argv = sys.argv
    sys.argv = ['main.py', '-e', 'Exercises.txt', '-a', 'Answers.txt']

    profiler = cProfile.Profile()
    profiler.enable()

    main()  # 调用主函数

    profiler.disable()

    # 保存性能数据到 performance_analysis 文件夹
    profile_path = os.path.join('performance_analysis', 'check_profile.prof')
    profiler.dump_stats(profile_path)

    # 恢复原始参数
    sys.argv = original_argv

    print(f"性能分析完成！生成文件: {profile_path}")

    # 生成统计报告
    generate_stats_report(profile_path, '题目批改性能分析')


def generate_stats_report(profile_path, title):
    """生成文本格式的性能统计报告"""
    stats = pstats.Stats(profile_path)

    # 生成统计报告文件
    report_path = profile_path.replace('.prof', '_report.txt')

    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(f"=== {title} ===\n")
        f.write("=" * 50 + "\n\n")

        f.write("按累计时间排序（前20个函数）：\n")
        f.write("-" * 40 + "\n")
        stats.sort_stats('cumulative')
        stats.stream = f
        stats.print_stats(20)

        f.write("\n\n按内部时间排序（前20个函数）：\n")
        f.write("-" * 40 + "\n")
        stats.sort_stats('tottime')
        stats.stream = f
        stats.print_stats(20)

    print(f"统计报告已生成: {report_path}")


def generate_snakeviz_command():
    """生成使用snakeviz查看报告的指令"""
    print("\n" + "=" * 60)
    print("使用以下命令查看性能分析报告：")
    print("1. 查看题目生成性能分析：")
    print("   snakeviz performance_analysis/generate_profile.prof")
    print("\n2. 查看题目批改性能分析：")
    print("   snakeviz performance_analysis/check_profile.prof")
    print("=" * 60)


if __name__ == "__main__":
    # 运行生成题目的性能分析
    profile_generation()

    # 运行批改的性能分析
    profile_checking()

    # 显示查看报告的指令
    generate_snakeviz_command()