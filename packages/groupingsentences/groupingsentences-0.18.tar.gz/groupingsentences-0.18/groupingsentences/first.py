# encoding=utf-8
import jieba
import xlrd
import xlwt
import math
import re
import json
import datetime
import sys, getopt
import os
from sklearn.feature_extraction.text import  TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.cluster import MiniBatchKMeans

#for word2vec
import gensim
import jieba
import numpy as np
from scipy.linalg import norm

from groupingsentences.ssdistance import get_similarity_val_by_sentences
from groupingsentences.ssdistance import get_funcname_by_func_type_id
from groupingsentences.fileload import load_cells_from_file

#1：词向量文本分类，这套程序的核心思路是：
#a: 两两比对词库里的关键词
#b: 比对时计算两者之间的余弦值
#c: 根据返回的余弦值选择是否归为一类（修改该关键词所处顺序）
#d: 输出排序后的结果放在文档里


def cells_to_groups(cells, type_of_func = 0 , threshold = 0.55):
    groups = {}
    sentences_processed = set()

    for sentence1 in cells:
        if sentence1 not in sentences_processed:
            sentence_related = set()
            groups[sentence1] = sentence_related
            sentences_processed.add(sentence1)
            for sentence2 in cells:
                #print(sentence1)
                if sentence2 not in sentences_processed:
                    dist1 = get_similarity_val_by_sentences(sentence1, sentence2, type_of_func)
                    if dist1 > threshold:
                        #related
                        sentence_related.add(sentence2)
                        sentences_processed.add(sentence2)
    return groups

def cells_kmeans_to_groups_000(cells, level = 0, model_file_path = './groupingsentences/dataset/news_12g_baidubaike_20g_novel_90g_embedding_64.bin'):
    def jieba_tokenize(text):
        return jieba.lcut(text) 

    def sentence_vector(s):
        words = jieba.lcut(s)
        v = np.zeros(64)
        for word in words:
            try:
                v += model[word]
            except:
                v = v
        v /= len(words)
        return v
    ts = datetime.datetime.now().timestamp() 

    model_file = model_file_path
    if os.path.isfile(model_file) == False:
        print('word2vec model file not exist! path', model_file)
        sys.exit(2)
    model = gensim.models.KeyedVectors.load_word2vec_format(model_file, binary=True)

    ts0 = datetime.datetime.now().timestamp() 
    print('load word2vec time passed ', ts0-ts)

    words_vector=[]
    for content in cells:
        #TextRank 关键词抽取，只获取固定词性
        v = sentence_vector(content)
        words_vector.append(v)
    vv = np.array(words_vector)

    num_clusters = 5000 #int(len(text_list)/20)
    if len(words_vector) > 10000:
        num_clusters = min(5000, int(len(words_vector)/50))
        batch_size=50
        init_size = num_clusters
        km_cluster = MiniBatchKMeans(n_clusters=num_clusters, max_iter=100, batch_size=batch_size, 
                                    init='k-means++', verbose=0, compute_labels=True, 
                                    random_state=None, tol=0.0, max_no_improvement=10, 
                                    init_size=init_size, n_init=3, reassignment_ratio=0.01)
        '''
        random_state: 随机生成簇中心的状态条件,譬如设置random_state = 9

        tol: 容忍度，即kmeans运行准则收敛的条件

        max_no_improvement：即连续多少个Mini Batch没有改善聚类效果的话，就停止算法，
        和reassignment_ratio， max_iter一样是为了控制算法运行时间的。默认是10.一般用默认值就足够了。

        batch_size：即用来跑Mini Batch
        KMeans算法的采样集的大小，默认是100.如果发现数据集的类别较多或者噪音点较多，需要增加这个值以达到较好的聚类效果。

        reassignment_ratio:
        某个类别质心被重新赋值的最大次数比例，这个和max_iter一样是为了控制算法运行时间的。这个比例是占样本总数的比例，
        乘以样本总数就得到了每个类别质心可以重新赋值的次数。如果取值较高的话算法收敛时间可能会增加，尤其是那些暂时拥有样本数较少的质心。
        默认是0.01。如果数据量不是超大的话，比如1w以下，建议使用默认值。 如果数据量超过1w，类别又比较多，可能需要适当减少这个比例值。
        具体要根据训练集来决定。

        '''
    else:
        num_clusters = min(50, int(len(words_vector)/50))
        km_cluster = KMeans(n_clusters=num_clusters, max_iter=300, n_init=40, 
                            init='k-means++',n_jobs=-1)
        '''
        n_clusters: 指定K的值
        max_iter: 对于单次初始值计算的最大迭代次数
        n_init: 重新选择初始值的次数
        init: 制定初始值选择的算法
        n_jobs: 进程个数，为-1的时候是指默认跑满CPU
        注意，这个对于单个初始值的计算始终只会使用单进程计算，
        并行计算只是针对与不同初始值的计算。比如n_init=10，n_jobs=40, 
        服务器上面有20个CPU可以开40个进程，最终只会开10个进程
        '''

    ts1 = datetime.datetime.now().timestamp() 
    print('KMeans clustering time passed ', ts1-ts)

    #返回各自文本的所被分配到的类索引
    result = km_cluster.fit_predict(vv)

    print("Predicting result:", result)
    '''
    每一次fit都是对数据进行拟合操作，
    所以我们可以直接选择将拟合结果持久化，
    然后预测的时候直接加载，进而节省时间。
    '''
    ts2 = datetime.datetime.now().timestamp() 
    print('prdicting time passed ', ts2-ts1)
    # now the result[] array has the cluster index

    # now the result[] array has the cluster index
    groups = {}
    groups_ids = {}
    k = 0
    for cell_item in cells:
        bucket = result[k]
        if bucket not in groups_ids:
            groups_ids[bucket] = cell_item
            groups[cell_item] = set()
        groups[groups_ids[bucket]].add(cell_item)
        k = k+1
    print(len(groups))
    return groups

def cells_kmeans_to_groups(cells, type_of_func = 0 , threshold = 0.55, model_file_path = ''):
    return cells_kmeans_to_groups_000(cells, 0, model_file_path)

def save_groups_to_xls(dest_file_name, groups):
    #纵向优先
    #写入xls文件
    # 打开文件
    style0 = xlwt.easyxf('font: name Times New Roman, color-index black, bold off',
        num_format_str='#,##0.00')
    stylered = xlwt.easyxf('font: name Times New Roman, color-index red, bold off',
        num_format_str='#,##0.00')

    style1 = xlwt.easyxf(num_format_str='D-MMM-YY')
    wb = xlwt.Workbook()
    ws = wb.add_sheet('Sheet0')
    max_j_start = 0
    max_j_height = 0
    sorted_word_groups = sorted(groups.items(), key=lambda x: len(x[1]), reverse = True)
    total_counts = 0
    for key, value in sorted_word_groups:
        total_counts = total_counts + len(value) + 1
    print('total counts', total_counts)
    max_height = (total_counts + len(sorted_word_groups) + 254)/255 # max height we need
    print('max_height', max_height)

    style_index = 0
    i = 0 #column
    j = 0 #row
    for key, value in sorted_word_groups: #sort by the len of set() 
        #print('## j,i row,column',j,i)
        style_index = style_index + 1
        style_item = style0
        if style_index%2 == 0:
            style_item = stylered
        ws.write(j, i, key , style_item)
        j = j + 1
        if j > max_height:
            j = 0
            i = i + 1
        for value2 in sorted(value):
            #print('j,i',j,i)
            ws.write(j, i, value2 , style_item)
            j = j + 1
            if j > max_height:
                j = 0
                i = i + 1
        j = j + 1 # add a space
        if j > max_height:
            j = 0
            i = i + 1
    wb.save(dest_file_name)

#default KMeans word2vec 7
def gs_grouping_sentences_to_xls(inputfile, outputfile, max_items=10000, encoding='gb18030', type_of_func = 7, threshold = 0.55, model_file_path=''):
    cells = load_cells_from_file(inputfile, encoding , max_items)
    ts = datetime.datetime.now().timestamp() 
    if type_of_func == 7: #7 Kmeans wordvector
        groups = cells_kmeans_to_groups(cells, type_of_func, threshold, model_file_path)
    else:
        groups = cells_to_groups(cells, type_of_func, threshold)
    print('groups items count', len(groups))
    ts2 = datetime.datetime.now().timestamp() 
    save_groups_to_xls(outputfile, groups)
    ts3 = datetime.datetime.now().timestamp() 
    print('type of compare function', type_of_func)
    print('total cells count', len(cells))
    print('compare sentences time passed (seconds):', ts2-ts)
    print('save to xls time passed (seconds):', ts3-ts2) 

def main(argv):
    inputfile = ''
    outputfile = ''
    type_of_func = 7
    threshold = 0.55
    encoding = 'gb18030'
    max_items = 1000
    model_file_path = './groupingsentences/dataset/news_12g_baidubaike_20g_novel_90g_embedding_64.bin'
    

    try:
        opts, args = getopt.getopt(argv,"hi:o:c:e:f:t:m:",["ifile=","ofile=","encoding=","maxcount="])
    except getopt.GetoptError:
        print('first.py -i <inputfile> -o <outputfile> -c <maxcount 1000 default> -e <encoding gb18030 default> -f <typeofcomparefunction 0 default> -t <threshold 0.55 default> -m <word2vec model file path>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('first.py -i <inputfile> -o <outputfile> -c <maxcount 1000 default> -e <encoding gb18030 default> -f <typeofcomparefunction 0 default> -t <threshold 0.55 default> -m <word2vec model file path>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
        elif opt in ("-m"):
            model_file_path = arg
        elif opt in ("-f"):
            type_of_func = int(arg)
        elif opt in ("-t"):
            threshold = float(arg)
        elif opt in ("-e", "--encoding"):
            encoding = (arg)
        elif opt in ("-c", "--maxcount"):
            max_items = int(arg)
    if len(inputfile)==0 or len(outputfile)==0:
        print('first.py -i <inputfile> -o <outputfile> -c <maxcount 1000 default> -e <encoding gb18030 default> -f <typeofcomparefunction 0 default> -t <threshold 0.55 default> -m <word2vec model file path>')
        sys.exit(2)

    print('Input file is "', inputfile)
    print('Output file is "', outputfile)
    gs_grouping_sentences_to_xls(inputfile, outputfile, max_items, encoding, type_of_func , threshold, model_file_path)
   

if __name__ == "__main__":
    main(sys.argv[1:])
