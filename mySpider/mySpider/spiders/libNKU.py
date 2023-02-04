import scrapy
from mySpider.items import MyspiderItem


class LibnkuSpider(scrapy.Spider):
    name = 'libNKU'
    allowed_domains = ['nankai.edu.cn']
    # 更改此处cls=的值来对不同目录进行爬取，注意要同时修改pipeline.py中的json文件名
    start_urls = ['https://opac.nankai.edu.cn/browse/cls_browsing_book.php?s_doctype=all&cls=TP31&page=1']
    pageCnt = 0

    def parse(self, response):
        # 获取当页所有节点
        node_list=response.xpath('//div[@class="list_books"]')
        # 遍历节点列表
        print(len(node_list))
        for node in node_list:
            detail_url = response.urljoin(node.xpath('./h3/strong/a/@href').extract_first())
            #print(item)
            # 进入详情页面
            yield scrapy.Request(
                url=detail_url,
                callback=self.detailParse
            )

        # 模拟翻页
        self.pageCnt+=1
        print("现在是第 %d 页" % self.pageCnt)
        preNext = response.xpath('//a[@class="blue"]')
        for node in preNext:
            if(node.xpath('./text()').extract_first() == "下一页"):
                yield scrapy.Request(
                    url=response.urljoin(node.xpath('./@href').extract_first()),
                    callback=self.parse
                )


            


    def detailParse(self,response):
        item = MyspiderItem()
        item['link'] = response.url
        node_list=response.xpath('//*[@id="item_detail"]/dl')
        # 遍历节点列表
        #print(len(node_list))
        for node in node_list:
            if(node.xpath('./dt/text()').extract_first()=="题名/责任者:"):
                if(len(node.xpath('./dd/a/text()'))!=0):
                    item['nameAndAuthor'] = str(node.xpath('./dd/a/text()').extract_first()) + str(node.xpath('./dd/text()').extract_first())
                else:
                    item['nameAndAuthor'] = node.xpath('./dd/text()').extract_first()

            if(node.xpath('./dt/text()').extract_first()=="出版发行项:"):
                if(len(node.xpath('./dd/a/text()'))!=0):
                    item['press'] = str(node.xpath('./dd/a/text()').extract_first()) + str(node.xpath('./dd/text()').extract_first())
                else:
                    item['press'] = node.xpath('./dd/text()').extract_first()
            
            if(node.xpath('./dt/text()').extract_first()=="ISBN及定价:"):
                if(len(node.xpath('./dd/a/text()'))!=0):
                    item['ISBNAndPrice'] = str(node.xpath('./dd/a/text()').extract_first()) + str(node.xpath('./dd/text()').extract_first())
                else:
                    item['ISBNAndPrice'] = node.xpath('./dd/text()').extract_first()
                
            if(node.xpath('./dt/text()').extract_first()=="学科主题:"):
                item['subject'] =""
                if(len(node.xpath('./dd/a/text()'))!=0):
                    item['subject'] += str(node.xpath('./dd/a/text()').extract_first()) 
                if(len(node.xpath('./dd/text()'))!=0):
                    item['subject'] += node.xpath('./dd/text()').extract_first()
        yield item
        


