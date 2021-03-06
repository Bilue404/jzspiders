import json
import os
import re
import sys

import requests
from gne import GeneralNewsExtractor

cur_path = os.path.split(os.path.realpath(__file__))[0]
file_path = os.path.abspath(os.path.join(cur_path, ".."))
sys.path.insert(0, file_path)

from base_spider import SpiderBase
from scripts import utils


class CCTVFinance(SpiderBase):
    def __init__(self):
        super(CCTVFinance, self).__init__()
        self.web_url = 'https://jingji.cctv.com/index.shtml'
        self.url = 'https://news.cctv.com/2019/07/gaiban/cmsdatainterface/page/economy_1.jsonp?cb=economy'
        self.extractor = GeneralNewsExtractor()
        self.fields = ['title', 'keywords', 'pub_date', 'brief', 'link', 'article']
        self.table_name = 'cctvfinance'
        # self.name = '央视网-财经频道'
        info = utils.org_tablecode_map.get(self.table_name)
        self.name, self.table_code = info[0], info[1]

    def _create_table(self):
        create_sql = '''
        CREATE TABLE IF NOT EXISTS `{}`(
          `id` int(11) NOT NULL AUTO_INCREMENT,
          `pub_date` datetime NOT NULL COMMENT '发布时间',
          `title` varchar(64) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL COMMENT '文章标题',
          `keywords` varchar(64) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL COMMENT '文章关键词',
          `link` varchar(128) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL COMMENT '文章详情页链接',
          `brief` text CHARACTER SET utf8 COLLATE utf8_bin COMMENT '文章摘要',
          `article` text CHARACTER SET utf8 COLLATE utf8_bin COMMENT '详情页内容',
          `CREATETIMEJZ` datetime DEFAULT CURRENT_TIMESTAMP,
          `UPDATETIMEJZ` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
          PRIMARY KEY (`id`),
          UNIQUE KEY `link` (`link`),
          KEY `pub_date` (`pub_date`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='央视网-财经频道';
        '''.format(self.table_name)
        self._spider_init()
        self.spider_client.insert(create_sql)
        self.spider_client.end()

    def extract_content(self, body):
        try:
            result = self.extractor.extract(body)
        except:
            return ''
        else:
            return result

    def parse_detail(self, link):
        resp = requests.get(link, headers=self.headers)
        body = resp.text.encode("ISO-8859-1").decode("utf-8")
        ret = self.extract_content(body)
        content = ret.get("content")
        return content

    def start(self):
        """单独成表"""
        self._create_table()
        resp = requests.get(self.url, headers=self.headers)
        items = []
        if resp.status_code == 200:
            body = resp.text.encode("ISO-8859-1").decode("utf-8")
            datas_str = re.findall(r"economy\((.*)\)", body)[0]
            datas = json.loads(datas_str).get("data").get("list")

            for data in datas:
                item = dict()
                item['title'] = data.get("title")
                item['keywords'] = data.get("keywords")
                item['pub_date'] = data.get("focus_date")
                item['brief'] = data.get('brief')
                link = data.get("url")
                item['link'] = link
                try:
                    content = self.parse_detail(link)
                except:
                    content = None
                if content:
                    item['article'] = content
                    items.append(item)
                    ret = self._save(self.spider_client, item, self.table_name, self.fields)

    def run(self):
        """入汇总表"""
        self._spider_init()
        resp = requests.get(self.url, headers=self.headers)
        if resp.status_code == 200:
            body = resp.text.encode("ISO-8859-1").decode("utf-8")
            datas_str = re.findall(r"economy\((.*)\)", body)[0]
            datas = json.loads(datas_str).get("data").get("list")

            for data in datas:
                item = dict()
                item['PubDatetime'] = data.get("focus_date")
                item['Title'] = data.get("title")
                item['KeyWords'] = data.get("keywords")
                link = data.get("url")
                item['Website'] = link
                item['Abstract'] = data.get('brief')
                try:
                    content = self.parse_detail(link)
                except:
                    content = None
                if content:
                    item['Content'] = content
                    # 汇总表附加字段
                    item['DupField'] = "{}_{}".format(self.table_code, item['Website'])
                    item['MedName'] = self.name
                    item['OrgMedName'] = self.name
                    item['OrgTableCode'] = self.table_code
                    self._save(self.spider_client, item, self.merge_table, self.merge_fields)

    def trans_history(self):
        self._spider_init()
        for i in range(1000):    # TODO
            trans_sql = '''select pub_date as PubDatetime,\
title as Title,\
keywords as KeyWords,\
link as Website,\
brief as Abstract, \
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
    # CCTVFinance().start()

    # CCTVFinance().trans_history()

    CCTVFinance().run()

    pass
