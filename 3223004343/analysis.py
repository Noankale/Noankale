# profile_main.py
from line_profiler import LineProfiler
import cProfile
import pstats
import sys
from main import text_process, cosine_similarity, jaccard_similarity, levenshtein_similarity,main

def setup_profiler():
  # 创建性能分析器
  profiler = LineProfiler()
  
  # 分析各函数性能
  profiler.add_function(text_process)
  profiler.add_function(cosine_similarity)
  profiler.add_function(jaccard_similarity)
  profiler.add_function(levenshtein_similarity)
  profiler.add_function(main)
  
  return profiler

# 测试性能
def test_complete_performance():
    # 备份原始参数
    original_argv = sys.argv.copy()
    
    # 设置测试参数
    sys.argv = ['main.py', r'D:\work\rjgc\orig.txt', r'D:\work\rjgc\orig_0.8_del.txt', r'D:\work\rjgc\orig_result.txt']
    
    try:
        # 运行完整的main函数
        main()
    finally:
        # 恢复原始参数
        sys.argv = original_argv

if __name__ == '__main__':
    print("开始性能分析...")
    
    # 方法2: 使用cProfile进行详细分析
    print("\n" + "="*50)
    print("cProfile性能分析结果:")
    print("="*50)
    
    profiler = cProfile.Profile()
    profiler.enable()
    test_complete_performance()
    profiler.disable()
    
    stats = pstats.Stats(profiler)
    stats.sort_stats('cumulative')
    stats.print_stats(15)
    
    # 方法3: LineProfiler逐行分析
    print("\n" + "="*50)
    print("LineProfiler逐行分析结果:")
    print("="*50)
    
    line_profiler = setup_profiler()
    line_profiler_wrapper = line_profiler(test_complete_performance)
    line_profiler_wrapper()
    line_profiler.print_stats()