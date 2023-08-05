from sync.base import BaseSync
from spider.album import AlbumSpider
from classcard_dataclient.models.album import Album, Image, TypeSet


class AlbumSync(BaseSync):
    def __init__(self):
        super(AlbumSync, self).__init__()
        self.page_list = [("http://www.student.sdnu.edu.cn/", "list.jsp?urltype=tree.TreeTempUrl&wbtreeid=1016")]
        self.img = []

    def crawl(self):
        for page in self.page_list:
            print(">>> start crawl {}".format(page))
            asp = AlbumSpider(page[0], page[1])
            asp.start()
            for target in asp.targets.values():
                if not target.get("content", None):
                    continue
                if isinstance(target["content"], str):
                    img = Image(name=target["topic"], path=target["content"])
                else:
                    img = Image(name=target["topic"], path=target["content"][0])
                self.img.append(img)

    def sync(self):
        self.crawl()
        album = Album(name="校园风采集锦", category=TypeSet.CLASSROOM_TYPE, all_classroom=True)
        for img in self.img:
            album.add_image(img)
        self.client.create_album(self.school_id, album)
