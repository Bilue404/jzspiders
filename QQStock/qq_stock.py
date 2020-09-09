import json
import os
import sys

from gne import GeneralNewsExtractor

cur_path = os.path.split(os.path.realpath(__file__))[0]
file_path = os.path.abspath(os.path.join(cur_path, ".."))
sys.path.insert(0, file_path)

from base_spider import SpiderBase
from scripts import utils


class qqStock(SpiderBase):
    def __init__(self):
        # TODO 重构: https://new.qq.com/ch/finance/
        super(qqStock, self).__init__()
        self.extractor = GeneralNewsExtractor()
        self.token = "8f6b50e1667f130c10f981309e1d8200"
        self.list_url = "https://pacaio.match.qq.com/irs/rcd?cid=52&token={}" \
                        "&ext=3911,3922,3923,3914,3913,3930,3915,3918,3908&callback=__jp1".format(self.token)
        self.fields = []
        self.table_name = "qq_Astock_news"
        # self.name = '腾讯财经[A股]'
        info = utils.org_tablecode_map.get(self.table_name)
        self.name, self.table_code = info[0], info[1]

    def _create_table(self):
        sql = '''
         CREATE TABLE IF NOT EXISTS `{}` (
          `id` int(11) NOT NULL AUTO_INCREMENT,
          `pub_date` datetime NOT NULL COMMENT '发布时间',
          `title` varchar(64) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL COMMENT '文章标题',
          `link` varchar(128) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL COMMENT '文章详情页链接',
          `article` text CHARACTER SET utf8 COLLATE utf8_bin COMMENT '详情页内容',
          `CREATETIMEJZ` datetime DEFAULT CURRENT_TIMESTAMP,
          `UPDATETIMEJZ` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
          PRIMARY KEY (`id`),
          UNIQUE KEY `link` (`link`),
          KEY `pub_date` (`pub_date`),
          KEY `update_time` (`UPDATETIMEJZ`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='腾讯财经[A股]'; 
        '''.format(self.table_name)
        self._spider_init()
        self.spider_client.insert(sql)
        self.spider_client.end()

    def _parse_article(self, vurl):
        detail_page = self._get(vurl)
        if detail_page:
            result = self.extractor.extract(detail_page.text)
            return result.get("content")

    def _parse_list(self):
        list_resp = self._get(self.list_url)
        if list_resp:
            print("请求主列表页成功 ")
            body = list_resp.text
            body = body.lstrip("__jp1(")
            body = body.rstrip(")")
            body = json.loads(body)
            datas = body.get("data")

            specials = []
            articles = []

            for data in datas:
                if data.get("article_type") == 120:
                    specials.append(data)
                elif data.get("article_type") == 0:
                    articles.append(data)
                else:
                    print("爬取到预期外的数据{}".format(data))
                    print("爬取到预期外的数据类型{}".format(data.get("article_type")))  # 56 视频类型 不再爬取
            return specials, articles

    def start(self):
        self._create_table()

        specials, articles = self._parse_list()
        items = []
        for article in articles:
            item = {}
            vurl = article.get("vurl")
            item['link'] = vurl
            item['pub_date'] = article.get("publish_time")
            item['title'] = article.get("title")
            article = self._parse_article(vurl)
            if article:
                item['article'] = article
                print(item)
                items.append(item)

        print(f"网站爬取个数 {len(items)}")
        self._spider_init()
        ret = self._batch_save(self.spider_client, items, self.table_name, self.fields)
        print(f"入库个数 {ret}")

        # print("开始处理专题页")
        # print(specials)
        #
        # for special in specials:
        #     special_id = special.get("app_id")
        #     special_url = "https://pacaio.match.qq.com/openapi/getQQNewsSpecialListItems?id={}&callback=getSpecialNews".format(special_id)
        #     ret = self._get(special_url).text
        #     ret = ret.lstrip("""('getSpecialNews(""")
        #     ret = ret.rstrip(""")')""")
        #     jsonobj = json.loads(ret)
        #     # print(jsonobj)
        #
        #     data = jsonobj.get("data")
        #     id_list = data.get("idlist")
        #     for one in id_list:
        #         new_list = one.get('newslist')
        #         for new in new_list:
        #             # print("标题:", new.get("longtitle"), end=",")
        #             # # print("链接:", new.get("surl"), end=",")
        #             # # "https://new.qq.com/omn/{}/{}.html".format(id[:6], id)
        #             # id = new.get("id")
        #             # print("链接:", "https://new.qq.com/omn/{}/{}.html".format(id[:8], id), end=",")
        #             # print("发布时间:", new.get("time"))
        #             item = {}
        #             id = new.get("id")
        #             link = "https://new.qq.com/omn/{}/{}.html".format(id[:8], id)
        #             title = new.get("longtitle")
        #             pub_date = new.get("time")
        #             if link and title and pub_date:
        #                 article = self._parse_article(link)
        #                 if article:
        #                     item['link'] = link
        #                     item['pub_date'] = pub_date
        #                     item['title'] = title
        #                     item['article'] = article
        #                     print(">>>>>", item)

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    def run(self):
        self._spider_init()

        specials, articles = self._parse_list()
        for article in articles:
            item = {}
            vurl = article.get("vurl")
            item['Website'] = vurl
            item['PubDatetime'] = article.get("publish_time")
            item['Title'] = article.get("title")
            article = self._parse_article(vurl)
            if article:
                item['Content'] = article
                # 增加合并表字段
                item['DupField'] = "{}_{}".format(self.table_code, item['Website'])
                item['MedName'] = self.name
                item['OrgMedName'] = self.name
                item['OrgTableCode'] = self.table_code
                print(item)
                self._save(self.spider_client, item, self.merge_table, self.merge_fields)

    def trans_history(self):
        self._spider_init()
        for i in range(1000):    # TODO
            trans_sql = '''select pub_date as PubDatetime,\
title as Title,\
link as Website,\
article as Content, \
CREATETIMEJZ as CreateTime, \
UPDATETIMEJZ as UpdateTime \
from {} limit {}, 1000; '''.format(self.table_name, i*1000)
            datas = self.spider_client.select_all(trans_sql)
            print(len(datas))
            if not datas:
                break
            for data in datas:
                data['DupField'] = "{}_{}".format(self.table_code, data['Website'])
                data['MedName'] = self.name
                data['OrgMedName'] = self.name
                data['OrgTableCode'] = self.table_code
                self._save(self.spider_client, data, 'OriginSpiderAll', self.merge_fields)


if __name__ == "__main__":
    # qqStock().start()

    # qqStock().trans_history()

    qqStock().run()

    pass
