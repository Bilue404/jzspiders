from lxml import html
from Takungpao.base import TakungpaoBase


class ZhongGuoJingJi(TakungpaoBase):
    def __init__(self):
        super(ZhongGuoJingJi, self).__init__()
        self.type = '中国经济'
        self.first_url = 'http://www.takungpao.com/finance/236132/index.html'
        self.format_url = 'http://www.takungpao.com/finance/236132/{}.html'

    def _parse_total_page(self, link):
        '''解析出页面的总页数
        <div class="tkp_page">
            <a href="/finance/236132/index.html" class="cms_prevpage">上一页</a>
            <div class="cms_curpage">1</div>
            <a href="/finance/236132/2.html" class="cms_page">2</a>
            <a href="/finance/236132/3.html" class="cms_page">3</a>
            <a href="/finance/236132/4.html" class="cms_page">4</a>
            <a href="/finance/236132/5.html" class="cms_page">5</a>
            <a href="/finance/236132/6.html" class="cms_page">6</a>
            <a href="/finance/236132/7.html" class="cms_page">7</a>
            <a href="/finance/236132/8.html" class="cms_page">8</a>
            <a href="/finance/236132/9.html" class="cms_page">9</a>
            <a href="/finance/236132/10.html" class="cms_page">10</a>
            <a href="/finance/236132/2.html" class="cms_nextpage">下一页</a>
        </div>
        '''
        list_resp = self.get(link)
        if list_resp:
            body = list_resp.text
            doc = html.fromstring(body)
            page = int(doc.xpath("//div[@class='tkp_page']/a[@class='cms_page']")[-1].text_content())
            return page

    def _parse_detail(self, link):
        """解析详情页内容
        """
        '''
        <div class="tkp_con_author"><span>2020-05-16 04:24:25</span><span>大公报</span> </div>
        '''

        '''
        <h2 class="tkp_con_author">時間：
            <span style="color:#666; ExchangeMargin-right:35px;">2020-04-23 11:15:32</span>來源：
            <span style="color:#666;">
                <a href="http://www.takungpao.com/" target="_blank" style="color:#AAA">大公网</a>
            </span>
        </h2>
        '''
        detail_resp = self.get(link)
        if detail_resp:
            body = detail_resp.text
            doc = html.fromstring(body)
            try:
                source = doc.xpath("//div[@class='tkp_con_author']/span")[-1].text_content()
            except:
                try:
                    source = doc.xpath("//h2[@class='tkp_con_author']/span")[-1].text_content()
                except:
                    source = '大公报'

            result = self.extractor.extract(body)
            content = result.get("content")
            return {"source": source, "content": content}
        else:
            return {}

    def _parse_list(self, page, list_url):
        """解析列表页"""
        list_resp = self.get(list_url)
        if list_resp and list_resp.status_code == 200:
            list_page = list_resp.text
            doc = html.fromstring(list_page)
            news_list = doc.xpath('//div[@class="wrap_left"]/dl[@class="item clearfix"]')
            items = []
            for news in news_list:
                item = {}
                link = news.xpath('./dd[@class="intro"]/a/@href')[0]
                item['link'] = link

                title = news.xpath("./dd/a/@title")[0]
                title = self._process_content(title)
                # 去除其中的字节顺序标记符
                title = title.replace("\ufeff", '')
                item['title'] = title

                pub_date = news.xpath("./dd[@class='sort']/text()")[0]
                # print(">>> ", pub_date)
                pub_date = self._process_pub_dt(pub_date)
                item['pub_date'] = pub_date

                ret = self._parse_detail(link)
                item['article'] = ret.get("content")
                item['source'] = ret.get("source")
                items.append(item)
            self._spider_init()
            page_save_num = self._batch_save(self.spider_client, items, self.table_name, self.fields)
            print("第{}页保存的个数是{} ".format(page, page_save_num))

    def start(self):
        self._create_table()
        page = self._parse_total_page(self.first_url)
        print("总页数 {}".format(page))

        # TODO
        page = 2
        for page in range(1, page+1):
            print("PAGE {}".format(page))
            if page == 1:
                list_url = self.first_url
            else:
                list_url = self.format_url.format(page)
            self._parse_list(page, list_url)

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def parse_list(self, list_url):
        """解析列表页"""
        list_resp = self.get(list_url)
        if list_resp and list_resp.status_code == 200:
            list_page = list_resp.text
            doc = html.fromstring(list_page)
            news_list = doc.xpath('//div[@class="wrap_left"]/dl[@class="item clearfix"]')
            for news in news_list:
                item = {}
                link = news.xpath('./dd[@class="intro"]/a/@href')[0]
                item['Website'] = link
                title = news.xpath("./dd/a/@title")[0]
                title = self._process_content(title)
                title = title.replace("\ufeff", '')
                item['Title'] = title
                pub_date = news.xpath("./dd[@class='sort']/text()")[0]
                pub_date = self._process_pub_dt(pub_date)
                item['PubDatetime'] = pub_date
                ret = self._parse_detail(link)
                item['Content'] = ret.get("content")
                item['OrgMedName'] = ret.get("source")
                # 新增合并字段
                item['DupField'] = "{}_{}".format(self.table_code, item['Website'])
                item['MedName'] = self.name
                if not item.get('OrgMedName'):
                    item['OrgMedName'] = self.name
                item['OrgTableCode'] = self.table_code
                self._save(self.spider_client, item, self.merge_table, self.merge_fields)

    def run(self):
        self._spider_init()
        page = self._parse_total_page(self.first_url)
        print("总页数 {}".format(page))
        page = 2
        for page in range(1, page + 1):
            print("PAGE {}".format(page))
            if page == 1:
                list_url = self.first_url
            else:
                list_url = self.format_url.format(page)
            self.parse_list(list_url)


class NewFinanceTrend(ZhongGuoJingJi):
    """废弃"""
    def __init__(self):
        super(NewFinanceTrend, self).__init__()
        self.type = '新经济浪潮'
        self.first_url = 'http://www.takungpao.com/finance/236160/index.html'
        self.format_url = 'http://www.takungpao.com/finance/236160/{}.html'


class HKCaiJing(ZhongGuoJingJi):
    def __init__(self):
        super(HKCaiJing, self).__init__()
        self.type = '香港财经'
        self.first_url = 'http://www.takungpao.com/finance/236131/index.html'
        self.format_url = 'http://www.takungpao.com/finance/236131/{}.html'


class HKStock(ZhongGuoJingJi):
    def __init__(self):
        super(HKStock, self).__init__()
        self.type = "港股"
        self.first_url = 'http://www.takungpao.com/finance/236135/index.html'
        self.format_url = 'http://www.takungpao.com/finance/236135/{}.html'


class GuoJiJingJi(ZhongGuoJingJi):
    def __init__(self):
        super(GuoJiJingJi, self).__init__()
        self.type = "国际经济"
        self.first_url = 'http://www.takungpao.com/finance/236133/index.html'
        self.format_url = 'http://www.takungpao.com/finance/236133/{}.html'


class DiChan(ZhongGuoJingJi):
    def __init__(self):
        super(DiChan, self).__init__()
        self.type = '地产'
        self.first_url = 'http://www.takungpao.com/finance/236136/index.html'
        self.format_url = 'http://www.takungpao.com/finance/236136/{}.html'


class Business(ZhongGuoJingJi):
    def __init__(self):
        super(Business, self).__init__()
        self.type = '商业'
        self.first_url = 'http://www.takungpao.com/finance/236137/index.html'
        self.format_url = 'http://www.takungpao.com/finance/236137/{}.html'


if __name__ == '__main__':
    ZhongGuoJingJi().run()

    HKCaiJing().run()

    HKStock().run()

    GuoJiJingJi().run()

    DiChan().run()

    Business().run()

    pass
