import pytest
import main
import math

class TestTextProcess:
    # 测试文本处理

    def test_text_process_normal(self):
        # 正常文本
        text = "今天天气真好！Hello World!"
        result = main.text_process(text)
        assert isinstance(result,list)
    
    def test_text_process_empty(self):
        # 空文本
        text = ""
        result = main.text_process(text)
        assert result == []
    
    def test_text_process_only_punctuation(self):
        # 只有标点符号的文本
        text = "!@#$%^&*()"
        result = main.text_process(text)
        assert result == []
    
    def test_text_process_mixed_case(self):
        # 混合大小写的英文
        text = "Hello WORLD Python"
        result = main.text_process(text)
        print(result)
        assert result == ['hello', 'world', 'python']

class TestCosineSimilarity:
    # 测试余弦相似度函数
    
    def test_cosine_similarity_identical(self):
        # 完全相同文本
        words1 = ['今天', '天气', '真好']
        words2 = ['今天', '天气', '真好']
        result = main.cosine_similarity(words1, words2)
        assert abs(result - 1.0) < 0.0001
    
    def test_cosine_similarity_different(self):
        # 完全不同文本
        words1 = ['苹果', '香蕉']
        words2 = ['汽车', '房子']
        result = main.cosine_similarity(words1, words2)
        assert abs(result - 0.0) < 0.0001
    
    def test_cosine_similarity_partial(self):
        # 部分相似文本
        words1 = ['苹果', '香蕉', '橙子']
        words2 = ['苹果', '梨', '葡萄']
        result = main.cosine_similarity(words1, words2)
        assert 0 < result < 1
    
    def test_cosine_similarity_empty_first(self):
        # 第一个向量为空"
        words1 = []
        words2 = ['苹果', '香蕉']
        result = main.cosine_similarity(words1, words2)
        assert result == 0
    
    def test_cosine_similarity_empty_second(self):
        # 第二个向量为空
        words1 = ['苹果', '香蕉']
        words2 = []
        result = main.cosine_similarity(words1, words2)
        assert result == 0
    
    def test_cosine_similarity_both_empty(self):
        # 两个向量都为空
        words1 = []
        words2 = []
        result = main.cosine_similarity(words1, words2)
        assert result == 0

class TestJaccardSimilarity:
    # 测试Jaccard相似度函数
    
    def test_jaccard_similarity_identical(self):
        # 完全相同文本
        words1 = ['今天', '天气', '真好']
        words2 = ['今天', '天气', '真好']
        result = main.jaccard_similarity(words1, words2)
        assert abs(result - 1.0) < 0.0001
    
    def test_jaccard_similarity_different(self):
        # 完全不同文本
        words1 = ['苹果', '香蕉']
        words2 = ['汽车', '房子']
        result = main.jaccard_similarity(words1, words2)
        assert abs(result - 0.0) < 0.0001
    
    def test_jaccard_similarity_partial(self):
        # 部分相似文本
        words1 = ['苹果', '香蕉', '橙子']
        words2 = ['苹果', '梨', '葡萄']
        result = main.jaccard_similarity(words1, words2)
        assert abs(result - 0.2) < 0.0001
    
    def test_jaccard_similarity_empty_first(self):
        # 第一个集合为空
        words1 = []
        words2 = ['苹果', '香蕉']
        result = main.jaccard_similarity(words1, words2)
        assert result == 0
    
    def test_jaccard_similarity_empty_second(self):
        # 第二个集合为空
        words1 = ['苹果', '香蕉']
        words2 = []
        result = main.jaccard_similarity(words1, words2)
        assert result == 0
    
    def test_jaccard_similarity_both_empty(self):
        # 两个集合都为空
        words1 = []
        words2 = []
        result = main.jaccard_similarity(words1, words2)
        assert result == 0

class TestLevenshteinSimilarity:
    # 测试Levenshtein相似度函数
    
    def test_levenshtein_similarity_identical(self):
        # 完全相同文本
        words1 = ['今天', '天气', '真好']
        words2 = ['今天', '天气', '真好']
        result = main.levenshtein_similarity(words1, words2)
        assert abs(result - 1.0) < 0.0001
    
    def test_levenshtein_similarity_different(self):
        # 完全不同文本
        words1 = ['苹果', '香蕉']
        words2 = ['汽车', '房子', '电脑']
        result = main.levenshtein_similarity(words1, words2)
        assert abs(result - 0.0) < 0.0001
    
    def test_levenshtein_similarity_partial(self):
        # 部分相似文本
        words1 = ['苹果', '香蕉', '橙子']
        words2 = ['苹果', '梨', '葡萄']
        result = main.levenshtein_similarity(words1, words2)
        assert 0 < result < 1
    
    def test_levenshtein_similarity_empty_first(self):
        # 第一个序列为空
        words1 = []
        words2 = ['苹果', '香蕉']
        result = main.levenshtein_similarity(words1, words2)
        assert result == 0
    
    def test_levenshtein_similarity_empty_second(self):
        # 第二个序列为空
        words1 = ['苹果', '香蕉']
        words2 = []
        result = main.levenshtein_similarity(words1, words2)
        assert result == 0
    
    def test_levenshtein_similarity_both_empty(self):
        # 两个序列都为空
        words1 = []
        words2 = []
        result = main.levenshtein_similarity(words1, words2)
        assert result == 1.0


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--cov=main", "--cov-report=term-missing"])