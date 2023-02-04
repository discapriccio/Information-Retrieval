from elasticsearch import  Elasticsearch
es = Elasticsearch(["https://localhost:9200"])  # 连接本地9200端口
print(es.index(index='py2', doc_type='doc', id=1, body={'name': "张开", "age": 18}))
print(es.get(index='py2', doc_type='doc', id=1))