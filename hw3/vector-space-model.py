import numpy as np
import os

data_dir = "dataset\\"
titles = []

##############################读入文档，预处理##############################
# terms列表
title_tokens = []
author_tokens = []
content_tokens = []
# terms列表（每个文档的单独放在一个列表里），此数据结构是为了防止多次遍历文档，在第一次遍历时就将读到的结果存起来
title_tokens_doc = []
author_tokens_doc = []
content_tokens_doc = []

# 填充terms列表
for title in os.listdir(data_dir):
    titles.append(title)
    # 填充title_tokens
    temp_title = title[:-4].lower()  # -4表示列表中倒数第四个索引（不取它），目的是删去.txt后缀
    # print(type(temp_title.split())) # list
    add_tokens = []
    for i in temp_title.split():
        add_tokens.append(i)
    title_tokens += add_tokens
    title_tokens_doc.append(add_tokens)
    title_tokens = sorted(set(title_tokens))

    # 填充author_tokens
    file = open(data_dir + title, 'r')
    lines = file.readlines()
    author = lines[0][8:].lower()
    add_tokens = []
    for i in author.split():
        add_tokens.append(i)
    author_tokens += add_tokens
    author_tokens_doc.append(add_tokens)
    author_tokens = sorted(set(author_tokens))

    # 填充content_tokens
    add_tokens = []
    for i in range(1, len(lines)):
        line = lines[i]
        for j in line.split():
            if j[-1] == "," or j[-1] == "." or j[-1] == ";":  # 去掉标点
                j = j[0:-1]
            add_tokens.append(j)
    content_tokens += add_tokens
    content_tokens_doc.append(add_tokens)
    content_tokens = sorted(set(content_tokens))


##############################计算文档的TF-IDF##############################
# 列表，每个表项为一个文档的字典，里面存储此文档中（词项，TF/TF-IDF）的映射
title_docDic_list = []  # term->frequency
author_docDic_list = []
content_docDic_list = []


def cal_TF(tokens, tokens_doc, docDicList):
    for i in range(len(tokens_doc)):
        docDict = dict.fromkeys(tokens, 0)
        for j in tokens_doc[i]:
            docDict[j] += 1
        for j in docDict.keys():
            docDict[j] = np.log10(docDict[j] + 1)
        docDicList.append(docDict)


cal_TF(title_tokens, title_tokens_doc, title_docDic_list)
cal_TF(author_tokens, author_tokens_doc, author_docDic_list)
cal_TF(content_tokens, content_tokens_doc, content_docDic_list)

title_term2IDF = dict.fromkeys(title_tokens, 0)
author_term2IDF = dict.fromkeys(author_tokens, 0)
content_term2IDF = dict.fromkeys(content_tokens, 0)


def cal_IDF(tokens_doc, term2IDF):
    for i in tokens_doc:
        for j in term2IDF.keys():
            if j in i:
                term2IDF[j] += 1
    for j in term2IDF.keys():
        term2IDF[j] = np.log10(len(tokens_doc) / term2IDF[j])


cal_IDF(title_tokens_doc, title_term2IDF)
cal_IDF(author_tokens_doc, author_term2IDF)
cal_IDF(content_tokens_doc, content_term2IDF)


def cal_TFIDF(docDic_list, term2IDF):
    for docDic in docDic_list:
        assert (type(docDic) == dict)
        for term in term2IDF:
            docDic[term] = docDic[term] * term2IDF[term]


cal_TFIDF(title_docDic_list, title_term2IDF)
cal_TFIDF(author_docDic_list, author_term2IDF)
cal_TFIDF(content_docDic_list, content_term2IDF)


##############################处理用户查询F##############################
print("Hello, welcome to the poetry retrieval system.")
title_query_tokens = input("pls type in the title\n").lower().split()
author_query_tokens = input("pls type in the author\n").lower().split()
content_query_tokens = input("pls type in the content\n").lower().split()
title_query_dic = [dict.fromkeys(title_tokens, 0)]  # 词典，存储查询的term->TFIDF对，外面用列表套起来是为了共用对文档处理的TFIDF函数
author_query_dic = [dict.fromkeys(author_tokens, 0)]
content_query_dic = [dict.fromkeys(content_tokens, 0)]


def cal_query_TF(query_tokens, query_dic):
    for token in query_tokens:
        ret = query_dic.get(token, -1)  # 若不存在在字典里（文档中没有出现过这个单词，返回-1）
        if ret != -1:
            query_dic[token] += 1


cal_query_TF(title_query_tokens, title_query_dic[0])
cal_query_TF(author_query_tokens, author_query_dic[0])
cal_query_TF(content_query_tokens, content_query_dic[0])
cal_TFIDF(title_query_dic, title_term2IDF)
cal_TFIDF(author_query_dic, author_term2IDF)
cal_TFIDF(content_query_dic, content_term2IDF)
title_similarities = []  # 列表，存储query与每个文档相似度的余弦值，按文档顺序排序
author_similarities = []
content_similarities = []


def cal_similarity(query_dic, docDic_list, similarities):
    for docDic in docDic_list:
        similarity = 0
        for key in query_dic.keys():
            if query_dic[key] == 0:  # 等于零的直接跳过
                continue
            similarity += query_dic.get(key) * docDic.get(key)
        similarities.append(similarity)


cal_similarity(title_query_dic[0], title_docDic_list, title_similarities)
cal_similarity(author_query_dic[0], author_docDic_list, author_similarities)
cal_similarity(content_query_dic[0], content_docDic_list, content_similarities)

# 自定义权值
weight_title = 0.5
weight_author = 0.3
weight_content = 0.2
result = dict.fromkeys(titles, float(0))
for i in range(len(titles)):
    result[titles[i]] += (
            weight_title * title_similarities[i] + weight_author * author_similarities[i] + weight_content *
            content_similarities[i])
result = dict(sorted(result.items(), key=lambda x: x[1], reverse=True))  # 按键大小进行排序
for key in result.keys():
    if result[key] != 0:
        print(key, result[key])
