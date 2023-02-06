from django.shortcuts import render
from datetime import datetime
from elasticsearch import Elasticsearch
from django.utils.datastructures import OrderedSet

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

# Create your views here.
from search_books.models import BooksIndex

client = Elasticsearch(hosts=["http://localhost:9200"])


class SearchView(APIView):
    '''
    返回搜索结果的接口
    '''

    permission_classes = [AllowAny]

    q = openapi.Parameter('q',
                          openapi.IN_QUERY,
                          description="查询语句",
                          type=openapi.TYPE_STRING)
    p = openapi.Parameter('p',
                          openapi.IN_QUERY,
                          description="页码",
                          type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[q, p], responses={200: {}})
    def get(self, request):
        # 获取参数
        key_words = request.query_params.get("q", "")
        page = request.query_params.get("p", "1")
        try:
            page = int(page)
        except:
            page = 1
        try:
            start_time = datetime.now()  # 计时
            response = client.search(index="books",
                                     body={
                                         "query": {
                                             "multi_match": {
                                                 "query": key_words,
                                                 "fields":
                                                 ["name", "author"]
                                             }
                                         },
                                         "from": (page - 1) * 10,
                                         "size": 10,
                                         "highlight": {
                                             "pre_tags":
                                             ["<span class='highlight'>"],
                                             "post_tags": ["</span>"],
                                             "fields": {
                                                 "name": {},
                                                 "author": {},
                                             },
                                             "fragment_size":
                                             40
                                         }
                                     })
            end_time = datetime.now()
            search_cost_time = (end_time - start_time).total_seconds()

            total_nums = response["hits"]["total"]["value"]

            if (total_nums % 10) > 0:
                page_nums = int(total_nums / 10) + 1
            else:
                page_nums = int(total_nums / 10)

            hit_list = []
            # 这里封装的时候也可以重新排序-->不过elastic里面应该有，后面可以看看
            for hit in response["hits"]["hits"]:
                hit_dict = {}
                # name
                if "name" in hit["highlight"]:
                    hit_dict["name"] = "".join(hit["highlight"].get(
                        "name", ""))
                else:
                    hit_dict["name"] = hit["_source"].get("name", "")

                # author
                if "author" in hit["highlight"]:
                    hit_dict["author"] = "".join(hit["highlight"].get(
                        "author", ""))  # 取前五百个词
                else:
                    hit_dict["author"] = hit["_source"].get("author", "")

                hit_dict["link"] = hit["_source"].get("link", "")
                hit_dict["score"] = hit["_score"]

                hit_list.append(hit_dict)

            hit_list = [item for index, item in enumerate(hit_list) if index == hit_list.index(item)]
            result = {
                "page": page,
                "searchCostTime": search_cost_time,
                "totalNums": total_nums,
                "pageNums": page_nums,
                "hitList": hit_list,
            }
            return Response(result, status=status.HTTP_200_OK)


        except Exception as e:
            return Response(e, status=status.HTTP_500_INTERNAL_SERVER_ERROR)