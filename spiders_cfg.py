spiders_config = {
    # 表名[容器名]: [启动文件路径, 启动方式(间隔/定点), 启动参数, 增量标的字段, 爬虫中文简称
    "juchao_kuaixun": ['Juchaodaynews/jcspider.py', "interval", (5, "minutes"), "CREATETIMEJZ", '巨潮快讯'],

    "juchao_info": ['Juchaodaynews/juchao_info.py', "interval", (10, "minutes"), "CREATETIMEJZ", '巨潮AI资讯'],

    "EEONews": ['EEOFinance/eeospider.py', 'interval', (10, 'minutes'), "CREATETIMEJZ", '经济观察网'],


}
