# profile_main.py
from line_profiler import LineProfiler
import cProfile
import pstats
from main import text_process, cosine_similarity, jaccard_similarity, levenshtein_similarity

def setup_profiler():
  # 创建性能分析器
  profiler = LineProfiler()
  
  # 分析各函数性能
  profiler.add_function(text_process)
  profiler.add_function(cosine_similarity)
  profiler.add_function(jaccard_similarity)
  profiler.add_function(levenshtein_similarity)
  
  return profiler

# 测试性能
def test_performance():
  # 测试数据

  originalPath = r"D:\work\软件工程\orig.txt"
  addPath = r"D:\work\软件工程\orig_0.8_del.txt"

  with open(originalPath,'r',encoding='utf8') as f:
    originalText = f.read()
  with open(addPath,'r',encoding='utf8') as f:
    addText = f.read()

  # 处理文本
  words1 = text_process(originalText)
  words2 = text_process(addText)
  
  # 计算相似度
  cosine_similarity(words1,words2)
  jaccard_similarity(words1,words2)
  levenshtein_similarity(words1,words2)

if __name__ == '__main__':
  # 设置分析器
  profiler = setup_profiler()
  
  # 开始分析
  profiler.enable_by_count()
  
  # 运行测试
  test_performance()
  
  # 结束分析
  profiler.disable_by_count()
  
  # 输出结果
  print("\n" + "="*50)
  print("逐行性能分析结果:")
  print("="*50)
  profiler.print_stats()