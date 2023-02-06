# 此文件用于删除索引
from elasticsearch import Elasticsearch
es = Elasticsearch()

index_name = "books"

es.indices.delete(index=index_name)