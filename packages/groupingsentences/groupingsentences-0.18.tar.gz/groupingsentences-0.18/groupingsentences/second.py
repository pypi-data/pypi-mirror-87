# encoding=utf-8
import jieba
import xlrd
import math
import re
import xmind
import json
import datetime
from groupingsentences.ssdistance import get_similarity_val_by_sentences
from groupingsentences.ssdistance import get_funcname_by_func_type_id
from groupingsentences.fileload import load_cells_from_file
import sys, getopt
import os.path

#关键词根提取法，这套程序的核心思路是：

#a: 统计top词根N个
#b: 提取包含词根的对应关键词子集
#c: 利用xmind模块，在循环中插入对应节点
#21：top词根不一定是合适的 同时 已经被作为节点的词根不应该重复计算
#因此需要一个库，记录已经被作为节点的词根
#同时，类似”可是“这样的词不具有研究意义，不应该被作为节点，所以需要一个库，事先导入非法词根表
#22：几百万的关键词，当需要打印的层级较多时，提取各级词频对应词库的交集很耗时，而且分词操作在遍历的过程中可以预计是会重复执行的，因此还是一样要做分词预处理，只不过这个预处理会更复杂一点，需要建立几个词典库：
#库1：{id:[长尾词，对应词根集合]}
#如：记录id”1“，对应值是一个列表，里面有长尾词”QQ邮箱格式怎么写“，和这个长尾词对应的所有词根集合（set(["QQ","邮箱","格式","怎么","写"])）
#库2：{长尾词:id}
#如：记录”QQ邮箱格式怎么写“，它对应在库1的记录id是”1“
#库3：{词根:对应词频}
#如：记录”QQ“，它的词频是5，说明它出现在5个关键词里
#库4：{词根:对应ID集合}
#如：记录”QQ“，它的对应ID集合是set([1,2,3,4,5])，表示有包含它的关键词的对应ID是哪几个

def create_stores(cells, words_already, stop_words):
    value_id = 1
    store1 = {}
    store2 = {}
    store3 = {}
    store4 = {}

    for sentence1 in cells:
        seg_list = jieba.cut_for_search(sentence1)
        for seg in list(seg_list):
            if seg not in words_already and seg not in stop_words:
                seg_count = store3.get(seg, 0)
                store3[seg] = seg_count+1
                if seg in store4:
                    store4[seg].add(value_id) 
                else:
                    store4[seg] = set([value_id])
        seg_list = jieba.cut_for_search(sentence1)
        #print(",".join(list(seg_list)))
        if value_id not in store1:
            store1[value_id]=[sentence1,set(list(seg_list))]
        if sentence1 not in store2:
            store2[sentence1]=value_id
        value_id = value_id+1
    return store1,store2,store3,store4

#TOP 获取lw句子列表里对应的首N个词根列表
def get_top(lw, top_count, store1, store2, store3, words_already, stop_words):
    #lw is a sentence list
    store1_,store2_,store3_,store4_ = create_stores(lw, words_already, stop_words)
    top_words = []
    segs = {}
    for value in lw:
        longtail_word_id = store2_[value] #库2：{长尾词:id}
        #get seg list
        seg_list = store1_[longtail_word_id][1] #库1：{id:[长尾词，对应词根集合]} 
        for seg in list(seg_list):
            if seg not in words_already:
                segs[seg]=store3_[seg] #库3：{词根:对应词频}
    sorted_segs = sorted(segs.items(), key = lambda kv:(kv[1], kv[0]),reverse=True)
    #print(sorted_segs)

    for item in sorted_segs[:top_count]:
        sub_word = item[0]
        sub_idsets = store4_[sub_word] #库4：{词根:对应ID集合}
        # 插入子主题
        subword_count = (store3_[sub_word].__str__())
        #print(sub_words)
        #print("$$$$$$$$$$$$\n")
        longtail_words_ids = sub_idsets
        longtail_words_list = []

        lw =  get_lw_by_seg(sub_word, store1_, store2_, store3_, store4_)
        # 打印主题对应的长尾词
        for id in longtail_words_ids:
            longtail_words_list.append(store1_[id][0]) #库1：{id:[长尾词，对应词根集合]}
        top_words.append((sub_word, sub_idsets, subword_count, longtail_words_list, lw))
    return top_words

def get_lw_by_seg(word1, store1, store2, store3, store4):
    # 获取词根所有id
    idsets = store4[word1] #库4：{词根:对应句子ID集合}
    # 提取词根所有长尾词
    lw = [store1[ids][0] for ids in idsets]  #{id:[长尾词，对应词根集合]}  lw = 长尾词 list
    return lw

def get_first_topwords(top_words_count, words_already, store1, store2, store3, store4, topword = '', stop_words=[]):
    top_words_list=[]
    try:
        word1 = topword
        word1_count = (store3[word1].__str__())
        # 获取词根所有id
        idsets = store4[word1] #库4：{词根:对应句子ID集合}
    except:
        print('except in get_first_topwords')
        idsets = set()
    print(idsets)

    if len(idsets) == 0:
        #print(sorted(store3.items(), key = lambda kv:(kv[1], kv[0]),reverse=True)) 
        sorted_ku3 = sorted(store3.items(), key = lambda kv:(kv[1], kv[0]),reverse=True)
        # TOP 8
        k = 0
        for item in sorted_ku3[:top_words_count*3]:
            sub_word = item[0]
            if sub_word not in words_already:
                sub_idsets = store4[sub_word] #库4：{词根:对应ID集合}
                # 插入子主题
                subword_count = (store3[sub_word].__str__())

                longtail_words_ids = sub_idsets
                longtail_words_list = []
                # 打印主题对应的长尾词
                for id in longtail_words_ids:
                    longtail_words_list.append(store1[id][0]) #库1：{id:[长尾词，对应词根集合]}
                lw =  get_lw_by_seg(sub_word, store1, store2, store3, store4)

                top_words_list.append((sub_word, sub_idsets, subword_count, longtail_words_list, lw))
                words_already.add(sub_word)
            k = k+1
            if k>top_words_count:
                break;
        print('top_words_list items count', len(top_words_list))
        return top_words_list
    else:
        word1 = topword
        word1_count = (store3[word1].__str__())
        words_already.add(word1)

        lw = get_lw_by_seg(word1, store1, store2, store3, store4)
        print(lw)

        sub_top_words_list = get_top(lw, top_words_count, store1, store2, store3, words_already, stop_words)#,set_top=set_top)
        #print(sub_top_words_list)
        return sub_top_words_list

def write_list_to_xmind(top_words_list, root_topic, max_level, level , store1, store2, store3, store4, words_already, stop_words, top_words_count):
    print('processing level :', level)
    for (word1,idsets,word1_count,longtail_root_words_list, lw) in top_words_list:
        sub_root_topic = root_topic.addSubTopic()
        sub_root_topic.setTitle(word1 + ' ('+ word1_count +')') #.decode('utf-8')
        # 统计子top词根列表
        if level != max_level:
            # 统计子top词根列表
            sub_top_words_list = get_top(lw, top_words_count, store1, store2, store3, words_already, stop_words)#,set_top=set_top)
            write_list_to_xmind(sub_top_words_list, sub_root_topic, max_level, level + 1,  store1, store2, store3, store4, words_already, stop_words, top_words_count)
        else:
            # 插入子主题
            sub_topic_s_kw = sub_root_topic.addSubTopic()
            sub_topic_s_kw.setTitle(','.join(longtail_root_words_list[:50]))#.decode('utf-8'))

def gen_my_xmind_file(top_words_list, dest_file_name, store1, store2, store3, store4, words_already, top_words_count=8, topword='', stop_words = [], max_level=1):  
    # 1、如果指定的XMind文件存在，则加载，否则创建一个新的
    workbook = xmind.load("./my.xmind")
    # 新建一个画布
    #sheet = workbook.createSheet()
    primary_sheet = workbook.getPrimarySheet()
    root_topic = primary_sheet.getRootTopic()
    # 给中心主题添加一个星星图标
    #root_topic.addMarker(MarkerId.starRed)
    #design_sheet1(primary_sheet)
    primary_sheet.setTitle("ROOT") #.decode('utf-8')
    # 新建一个主题
    root_topic = primary_sheet.getRootTopic()
    topword_title = 'ROOT'
    if len(topword)>0:
        topword_title = topword
    root_topic.setTitle(topword_title) #.decode('utf-8')

    write_list_to_xmind(top_words_list,root_topic, max_level, 0, store1, store2, store3, store4, words_already, stop_words, top_words_count)

    #print(workbook.to_prettify_json())
    #xmind.save(workbook)
    # 第2种：只保存思维导图内容content.xml核心文件，适用于没有添加评论、自定义样式和附件的情况
    xmind.save(workbook=workbook, path=dest_file_name)

def cells_to_xmind(cells, outputfile, top_words_count = 8, topword = '', stop_words_file_path = './groupingsentences/dataset/stop_words.txt', max_level=1):
    ts = datetime.datetime.now().timestamp()
    # 設定詞庫
    ### 繁體字較完整詞庫
    ### https://raw.githubusercontent.com/ldkrsi/jieba-zh_TW/master/jieba/dict.txt

    #should remove later
    #jieba.set_dictionary('./groupingsentences/dataset/twdict.txt')
 
    words_already = set() #用来保存已经加入xmind列表的无需再重复加入
    stop_words = set() #用来排除一些不适合参与排序词根，下一步可以从文件读取次列表
    if os.path.isfile(stop_words_file_path):
        ws = load_cells_from_file(stop_words_file_path, 'utf-8')
        for item in ws:
            stop_words.add(item)
            print(item)

    for word in list(stop_words):
        words_already.add(word)

    store1,store2,store3,store4 = create_stores(cells, words_already, stop_words)
    print('store1 count', len(store1))
    print('store2 count', len(store2))
    print('store3 count', len(store3))
    print('store4 count', len(store4))

    #获取首N个词根
    top_words_list = get_first_topwords(top_words_count, words_already, store1, store2, store3, store4, topword, stop_words)

    ts2 = datetime.datetime.now().timestamp() 
    gen_my_xmind_file(top_words_list, outputfile, store1, store2, store3, store4, words_already, top_words_count, topword, stop_words, max_level)
    ts3 = datetime.datetime.now().timestamp() 
    print('time passed ', ts2-ts)
    print('create 4 stores time passed (seconds):', ts2-ts)
    print('save to xmind time passed (seconds):', ts3-ts2)

def gs_grouping_sentences_to_xmind(inputfile, outputfile, max_items=10000, encoding='gb18030', topwordscount = 8, topword = '', stop_file_path = '', max_level = 1):
    cells = load_cells_from_file(inputfile, encoding , max_items)
    cells_to_xmind(cells, outputfile, topwordscount, topword, stop_file_path, max_level)   



def main(argv):
    inputfile = ''
    outputfile = ''
    top_words_count = 8
    encoding = 'gb18030'
    max_items = 1000
    top_word=''
    stop_file_path = './groupingsentences/dataset/stop_words.txt'
    max_level = 1

    try:
        opts, args = getopt.getopt(argv,"hi:o:c:e:t:w:p:m:",["ifile=","ofile=","encoding=","maxcount="])
    except getopt.GetoptError:
        print('second.py -i <inputfile> -o <outputfile> -c <maxcount 1000 default> -e <encoding gb18030 default> -t <topwordscount 8 default> -w <topword> -p <stop file path> -m <max level>' )
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('second.py -i <inputfile> -o <outputfile> -c <maxcount 1000 default> -e <encoding gb18030 default> -t <topwordscount 8 default> -w <topword> -p <stop file path> -m <max level>' )
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
        elif opt in ("-t"):
            top_words_count = int(arg)
        elif opt in ("-m"):
            max_level = int(arg)
        elif opt in ("-w"):
            top_word = arg
        elif opt in ("-p"):
            stop_file_path = arg
        elif opt in ("-e", "--encoding"):
            encoding = (arg)
        elif opt in ("-c", "--maxcount"):
            max_items = int(arg)
    if len(inputfile)==0 or len(outputfile)==0:
        print('second.py -i <inputfile> -o <outputfile> -c <maxcount 1000 default> -e <encoding gb18030 default> -t <topwordscount 8 default> -w <topword> -p <stop file path> -m <max level>' )
        sys.exit(2)

    print('Input file is "', inputfile)
    print('Output file is "', outputfile)
    gs_grouping_sentences_to_xmind(inputfile, outputfile, max_items, encoding, top_words_count, top_word, stop_file_path, max_level)


if __name__ == "__main__":
    main(sys.argv[1:])
