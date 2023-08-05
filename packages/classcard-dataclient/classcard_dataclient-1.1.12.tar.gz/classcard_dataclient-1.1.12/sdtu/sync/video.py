from sync.base import BaseSync
from spider.video import VideoSpider
from classcard_dataclient.models.video import Video
from classcard_dataclient.models.album import Album, Image, TypeSet


class VideoSync(BaseSync):
    def __init__(self):
        super(VideoSync, self).__init__()
        self.page_list = [("http://www.qlshx.sdnu.edu.cn/", "gyss.htm")]
        self.video = []
        self.img = []

    def crawl(self):
        for page in self.page_list:
            print(">>> start crawl {}".format(page))
            vs = VideoSpider(page[0], page[1])
            vs.start()
            for target in vs.targets.values():
                if not target.get("content", None):
                    continue
                if target['category'] == 'video':
                    if isinstance(target["content"], str):
                        video = Video(name=target["topic"], path=target["content"])
                    else:
                        video = Video(name=target["topic"], path=target["content"][0])
                    self.video.append(video)
                if target['category'] == 'img':
                    if isinstance(target["content"], str):
                        img = Image(name=target["topic"], path=target["content"])
                    else:
                        img = Image(name=target["topic"], path=target["content"][0])
                    self.img.append(img)

    def sync(self):
        self.crawl()
        for video in self.video:
            self.client.create_video(self.school_id, video)
        album = Album(name="校园风采集锦", category=TypeSet.CLASSROOM_TYPE, all_classroom=True)
        for img in self.img:
            album.add_image(img)
        self.client.create_album(self.school_id, album)
