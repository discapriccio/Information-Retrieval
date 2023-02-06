from django.db import models
from elasticsearch_dsl import Text, Date, Keyword, Integer, Document, Completion, Double, Float
from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import analyzer

# Create your models here.

connections.create_connection(hosts="http://localhost:9200")

my_analyzer = analyzer('ik_smart')

class BooksIndex(Document):
    link = Text()
    name = Text()
    author = Text()
    press = Text()
    ISBN = Text()
    price = Text()
    relRef1 = Text()
    relRef2 = Text()
    PR = Float()

    suggest = Completion(analyzer=my_analyzer)