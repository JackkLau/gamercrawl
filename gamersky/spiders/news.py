import scrapy

from gamersky.items import ImageItem


class NewsSpider(scrapy.Spider):
    name = "news"
    allowed_domains = ["gamersky.com"]
    start_urls = ["https://www.gamersky.com/news/202312/1684515.shtml"]
    # start_urls = ["https://www.gamersky.com/news/202312/1680626.shtml"]
    # start_urls = ["https://www.gamersky.com/news/202312/1682153.shtml"]
    # start_urls = ["https://www.gamersky.com/news/202312/1679700.shtml"]
    # start_urls = ["https://www.gamersky.com/news/202312/1680626.shtml"]

    def parse(self, response):
        print("parse response", response.status)
        if response.status == 200:
            # print("parse response", response.url)
            img_urls = response.xpath('//div[@class="Mid2L_con"]/p/a/img[@src]/@src').extract()

            for img_url in img_urls:
                # yield scrapy.Request(
                #     url=img_url,
                #     callback=self.parse_details
                # )
                item = ImageItem()
                item['image_url'] = img_url
                yield item
            # print("parse response", div)

            next_url = response.xpath('//div[@class="page_css"]/a[contains(text(),"下一页")]/@href').extract_first();
            if next_url is not None:
                yield scrapy.Request(
                    url=next_url,
                    callback=self.parse
                )
            print(next_url)

    def parse_details(self, response):

        pass
