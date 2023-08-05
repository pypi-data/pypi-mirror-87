from spider.base import BaseSpider


class NoticeSpider(BaseSpider):
    @classmethod
    def extract_date(cls, soup):
        try:
            year = soup.find_all("span", class_="year")[0].text
            date = soup.find_all("span", class_="date")[0].text
            year = year.replace(".", "-")
            return "{}-{}".format(year, date)
        except (Exception,):
            return None

    def extract_content(self):
        for tt, t_info in self.targets.items():
            t_host = self.analyse_host(t_info["url"])
            # t_soup = self.catch_html_soup(t_info["url"])
            # t_results = t_soup.find_all("div", class_="v_news_content")
            try:
                # p_content = []
                # p_content = [str(p_tag) for p_tag in t_results[0].find_all("p")]
                # for pc in t_results[0].find_all("p"):
                #     p_content.append(self.replace_src(str(pc), t_host))
                t_info["content"] = t_info["url"]
            except (Exception,):
                t_info["content"] = None
        return self.targets


class JZSpider(BaseSpider):
    @classmethod
    def extract_date(cls, soup):
        try:
            year = soup.find_all("span", class_="year")[0].text
            date = soup.find_all("span", class_="date")[0].text
            year = year.replace(".", "-")
            return "{}-{}".format(year, date)
        except (Exception,):
            return None

    def process_url(self, url):
        return self.base_url + url
