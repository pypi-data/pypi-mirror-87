# -*- coding: utf-8 -*-
"""
:集合各种计算句子间距离的函数，可以自己选择使用
"""
import distance
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from scipy.linalg import norm
import jieba
import numpy as np
import re
#for word2vec
import gensim
import jieba
import numpy as np
from scipy.linalg import norm

def edit_distance(s1, s2):
    return distance.levenshtein(s1, s2)

#jaccard
def jaccard_similarity(s1, s2):
    def add_space(s):
        return ' '.join(list(s))
    
    # 将字中间加入空格
    s1, s2 = add_space(s1), add_space(s2)
    # 转化为TF矩阵
    cv = CountVectorizer(tokenizer=lambda s: s.split())
    corpus = [s1, s2]
    vectors = cv.fit_transform(corpus).toarray()
    # 求交集
    numerator = np.sum(np.min(vectors, axis=0))
    # 求并集
    denominator = np.sum(np.max(vectors, axis=0))
    # 计算杰卡德系数
    return 1.0 * numerator / denominator

def tf_similarity(s1, s2):
    def add_space(s):
        return ' '.join(list(s))
    
    # 将字中间加入空格
    s1, s2 = add_space(s1), add_space(s2)
    # 转化为TF矩阵
    cv = CountVectorizer(tokenizer=lambda s: s.split())
    corpus = [s1, s2]
    vectors = cv.fit_transform(corpus).toarray()
    # 计算TF系数
    return np.dot(vectors[0], vectors[1]) / (norm(vectors[0]) * norm(vectors[1]))


def tfidf_similarity(s1, s2):
    def add_space(s):
        return ' '.join(list(s))
    
    # 将字中间加入空格
    s1, s2 = add_space(s1), add_space(s2)
    # 转化为TF矩阵
    cv = TfidfVectorizer(tokenizer=lambda s: s.split())
    corpus = [s1, s2]
    vectors = cv.fit_transform(corpus).toarray()
    # 计算TF系数
    return np.dot(vectors[0], vectors[1]) / (norm(vectors[0]) * norm(vectors[1]))

vectcos_cache = {}

def get_word_vector(s1,s2):
    """
    :param s1: 句子1
    :param s2: 句子2
    :return: 返回句子的余弦相似度
    """
    # 分词
    if s1 in vectcos_cache:
        list_word1 = vectcos_cache[s1]
    else:
        cut1 = jieba.cut(s1)
        list_word1 = (','.join(cut1)).split(',')
        vectcos_cache[s1] = list_word1

    if s2 in vectcos_cache:
        list_word2 = vectcos_cache[s2]
    else:
        cut2 = jieba.cut(s2)
        list_word2 = (','.join(cut2)).split(',')
        vectcos_cache[s2] = list_word2

    #print(list_word1,'###',list_word2)
    # 列出所有的词,取并集
    key_word = list(set(list_word1 + list_word2))
    # 给定形状和类型的用0填充的矩阵存储向量
    word_vector1 = np.zeros(len(key_word))
    word_vector2 = np.zeros(len(key_word))
 
    # 计算词频
    # 依次确定向量的每个位置的值
    for i in range(len(key_word)):
        # 遍历key_word中每个词在句子中的出现次数
        for j in range(len(list_word1)):
            if key_word[i] == list_word1[j]:
                word_vector1[i] += 1
        for k in range(len(list_word2)):
            if key_word[i] == list_word2[k]:
                word_vector2[i] += 1
 
    # 输出向量
    #print(word_vector1)
    #print(word_vector2)
    return word_vector1, word_vector2
 
def cos_dist(vec1,vec2):
    """
    :param vec1: 向量1
    :param vec2: 向量2
    :return: 返回两个向量的余弦相似度
    """
    dist1=float(np.dot(vec1,vec2)/(np.linalg.norm(vec1)*np.linalg.norm(vec2)))
    return dist1


def vectcos_similarity(s1, s2):
    vec1,vec2=get_word_vector(s1,s2)
    dist1=cos_dist(vec1,vec2)
    return dist1


model_file = './groupingsentences/dataset/news_12g_baidubaike_20g_novel_90g_embedding_64.bin'
model = 0
word2vector_cache = {}

def vector_similarity(s1, s2):
    def sentence_vector(s):
        global model
        if model == 0:
            model = gensim.models.KeyedVectors.load_word2vec_format(model_file, binary=True)
        words = jieba.lcut(s)
        v = np.zeros(64)
        for word in words:
            try:
                v_word = model[word]
                v += v_word
            except:
                v = v
        v /= len(words)
        return v

    if s1 in word2vector_cache:
        v1 = word2vector_cache[s1]
    else:
        v1 = sentence_vector(s1)
        word2vector_cache[s1] = v1

    if s2 in word2vector_cache:
        v2 = word2vector_cache[s2]
    else:
        v2 = sentence_vector(s2)
        word2vector_cache[s2] = v2
    print(v1)
    print(v2)
    return np.dot(v1, v2) / (norm(v1) * norm(v2))


def get_funcname_by_func_type_id(func_type_id):
    if func_type_id == 0:
        return 'vectcos_similarity'
    elif func_type_id == 1:
        return 'edit_distance'
    elif func_type_id == 2:
        return 'jaccard_similarity'
    elif func_type_id == 3:
        return 'tf_similarity'
    elif func_type_id == 4:
        return 'tfidf_similarity'
    elif func_type_id == 5:
        return 'vector_similarity'
    else:
        return 'vectcos_similarity'

def get_similarity_val_by_sentences(s1, s2, type_of_func = 0):
    """
    :param s1: 句子1
    :param s2: 句子2
    :param type_of_func 不同的相似度计算
    :return: 返回句子的相似度
    """
    if type_of_func == 0:
        return vectcos_similarity(s1, s2)
    elif type_of_func == 1:
        return edit_distance(s1, s2)
    elif type_of_func == 2:
        return jaccard_similarity(s1, s2)
    elif type_of_func == 3:
        return tf_similarity(s1, s2)
    elif type_of_func == 4:
        return tfidf_similarity(s1, s2)
    elif type_of_func == 5:
        return vector_similarity(s1, s2)
    else:
        return vectcos_similarity(s1, s2)

if __name__ == "__main__":
    strings = [
    '你在干什么',
    '你在干啥子',
    '你在做什么',
    '你好啊',
    '我喜欢吃香蕉'
    ]

    target = '你在干啥'
    
    for i in range(5):
        print('=================')
        print('type of func:', get_funcname_by_func_type_id(i))
        print('similarity to ', target)
        for string in strings:
            print(string, get_similarity_val_by_sentences(string, target, i))
