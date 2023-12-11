import scrapy

from gamersky.items import ImageItem


class GifsSpider(scrapy.Spider):
    name = "gifs"
    allowed_domains = ["gamersky.com"]
    start_urls = ["https://www.gamersky.com/news/202312/1682431.shtml"]

    def parse(self, response):
        print("parse response", response.status)
        if response.status == 200:
            # print("parse response", response.url)
            img_urls = response.xpath('//div[@class="Mid2L_con"]/p/img[@src]/@src').extract()

            for img_url in img_urls:
                # yield scrapy.Request(
                #     url=img_url,
                #     callback=self.parse_details
                # )
                item = ImageItem()
                item['image_url'] = img_url
                yield item
            # print("parse response", div)

            next_url = response.xpath('//div[@class="page_css"]/a[contains(text(),"下一页")]/@href').extract_first()
            if next_url is not None:
                yield scrapy.Request(
                    url=next_url,
                    callback=self.parse
                )
            print(next_url)
