# 此文件将爬虫获取的数据存储到的json文件，进行预处理，存入elastic search中
from elasticsearch import  Elasticsearch
es = Elasticsearch()  # 连接本地9200端口


####################### 读取json文件，预处理 #######################
import json
with open("./TP30.json", "r",encoding='utf-8') as f:
    data_list = json.load(f)

documents=[]
i=0
for data in data_list:
    document={}
    #id
    document['id']=i
    #link
    if 'link' in data.keys():
        document['link']=data['link']
    else :
        document['link']=""

    # 分割name、author
    if 'nameAndAuthor' in data.keys():
        nameAndAuthor=data['nameAndAuthor'].split('/')  
        if len(nameAndAuthor)==2:  #若出现多个/或没有/，name和author设为空
            document['name']=nameAndAuthor[0]
            document['author']=nameAndAuthor[1]
        else:
            document['name']=""
            document['author']=""
    else:
        document['name']=""
        document['author']=""

    #press
    if 'press' in data.keys():
        document['press']=data['press']
    else :
        document['press']=""

    # 分割ISBN、price
    if 'ISBNAndPrice' in data.keys():
        ISBNAndPrice=data['ISBNAndPrice'].split('/')  
        if len(ISBNAndPrice)==2:  #若出现多个/或没有/，ISBN和price设为空
            document['ISBN']=ISBNAndPrice[0]
            document['price']=ISBNAndPrice[1]
        else:
            document['ISBN']=""
            document['price']=""
    else:
        document['ISBN']=""
        document['price']=""
    

    #subject
    if 'subject' in data.keys():
        document['subject']=data['subject']
    else :
        document['subject']=""

    #处理relRef1、relRef2
    if 'relRef1' in data.keys():
        document['relRef1']=data['relRef1']
    else:
        document['relRef1']=""
    if 'relRef2' in data.keys():
         document['relRef2']=data['relRef2']
    else:
        document['relRef2']=""

    documents.append(document)
    i+=1
    # if i==20:
    #     break

####################### 计算pr值 #######################
import networkx as nx

# 建立有向图
G = nx.DiGraph()

# 添加节点
for doc in documents:
    pair=(doc['id'],doc['link'])
    G.add_node(pair)
    # print("node:",doc['link'])

# 添加边
for doc in documents:
    if doc['relRef1']!="":
        pair1=(doc['id'],doc['link'])
        pair2=(doc['id'],doc['relRef1'])
        G.add_edge(pair1, pair2 )
    if doc['relRef2']!="":
        pair1=(doc['id'],doc['link'])
        pair2=(doc['id'],doc['relRef2'])
        G.add_edge(pair1, pair2 )

# 计算PageRank值
pr = nx.pagerank(G)

id=0
for node, pagerank_value in pr.items():
    #print("Node:", node, "PageRank Value:", pagerank_value)
    documents[node[0]]['pr']=pagerank_value
    id+=1

# for doc in documents:
#     print(doc)



####################### 创建es索引 #######################
index_name = "books"
body = {
    "settings": {
        "number_of_shards": 1,
        "number_of_replicas": 0
    },
    "mappings": {
        "properties": {
            "link": {
                "type": "text"
            },
            "name": {
                "type": "text"
            },
            "author": {
                "type": "text"
            },
            "press": {
                "type": "text"
            },
            "ISBN": {
                "type": "text"
            },
            "price": {
                "type": "text"
            },
            "relRef1": {
                "type": "text"
            },
            "relRef2": {
                "type": "text"
            },
            "pr": {
                "type": "float"
            }
        }
    }
}

es.indices.create(index=index_name, body=body)

# 添加数据
for doc in documents:
    es.index(index=index_name, id=doc["id"], body=doc)