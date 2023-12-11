# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import os

import scrapy
# useful for handling different item types with a single interface
from scrapy.pipelines.images import ImagesPipeline
from scrapy.utils.misc import md5sum


class GamerskyPipeline:
    def process_item(self, item, spider):
        return item


class NewsImagesPipeline(ImagesPipeline):

    # def get_media_requests(self, item, info):
    #     return scrapy.Request(url=item['image_url'])
    #
    # def file_path(self, request, response=None, info=None, *, item=None):
    #     file_name = request.url.split('/')[-1]
    #     return file_name
    #
    # def item_completed(self, results, item, info):
    #     print('下载完成')
    #     pass

    def get_media_requests(self, item, info):
        print(item['image_url'])
        return scrapy.Request(url=item['image_url'])

    def file_path(self, request, response=None, info=None, *, item=None):
        file_name = request.url.split('/')[-1]
        return file_name

    def item_completed(self, results, item, info):
        print('下载完成')

    def check_gif(self, image):
        if image.format is None:
            return True

    def persist_gif(self, key, data, info):
        root, ext = os.path.splitext(key)
        absolute_path = self.store._get_filesystem_path(key)
        print(absolute_path)
        # self.store._mkdir(os.path.dirname(absolute_path), info)
        f = open(absolute_path, 'wb')  # use 'b' to write binary data.
        f.write(data)

    def image_downloaded(self, response, request=None, info=None, *, item=None):
        checksum = None
        print(request)
        print(response)
        res = self.get_images(response, request, info)
        for path, image, buf in res:
            if checksum is None:
                buf.seek(0)
                checksum = md5sum(buf)
            width, height = image.size
            if self.check_gif(image):
                self.persist_gif(path, response.body, info)
            else:
                self.store.persist_file(
                    path, buf, info,
                    meta={'width': width, 'height': height},
                    headers={'Content-Type': 'image/jpeg'})
        return checksum
