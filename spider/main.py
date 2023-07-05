"""
抓取
解析
存储
"""
import re
import ast
from urllib import parse
from datetime import datetime

import requests
from scrapy import Selector

from SQL_models import *

domain_url = "http://www.cskaoyan.com"
T_url = []
compare = ''


def get_theme(url):
    themes_text = requests.get(url).text
    themes_sel = Selector(text=themes_text)
    # theme = themes_sel.xpath('//div[@id="category_302"]/table/tr/td/dl/dt/a/text()').extract()
    theme_plates = themes_sel.xpath('//div[@class="bm bmw  flg cl"]')
    for theme_plate in theme_plates:
        theme_items = theme_plate.xpath('./div[contains(@id, "category_")]//tr//dl/dt/a')
        for theme_item in theme_items:
            Theme_url_part = theme_item.xpath('./@href').extract()[0]
            Theme_ID = Theme_url_part.split('.')[0].split('forum-')[-1]
            Theme_name = theme_item.xpath('./text()').extract()
            if not Theme_name:
                Theme_name = theme_item.xpath('.//b/text()').extract()
            Theme_url = parse.urljoin(domain_url, Theme_url_part)
            # 再爬取所有topic时,会需要访问theme的url，因此设置全局变量保存
            T_url.append(Theme_url)
            theme_text = requests.get(Theme_url).text
            theme_sel = Selector(text=theme_text)
            theme_data = theme_sel.xpath('//div[@class="bm bml pbn"]/div[@class="bm_h cl"]/h1/span')
            Theme_num = theme_data.xpath('./strong[2]/text()').extract()[0]
            Theme_rate = theme_data.xpath('./strong[3]/text()').extract()[0]
            theme_details = theme_sel.xpath('//div[@class="bm bml pbn"]/div[@class="bm_c cl pbn"]'
                                            '/div[contains(@id, "forum_rules_")]//div[@class="ptn xg2"]'
                                            '//*/text()').extract()
            theme_content = "".join(theme_details)
            # 保存数据至数据库
            theme = Theme()
            theme.Theme_ID = Theme_ID
            theme.Name = Theme_name[0]
            theme.Theme_num = Theme_num
            theme.Theme_rate = Theme_rate
            theme.Theme_content = theme_content
            theme.Theme_url = Theme_url
            existed_themes = Theme.select().where(Theme.Theme_ID == theme.Theme_ID)
            if existed_themes:
                theme.save()
            else:
                theme.save(force_insert=True)


def get_topic_mess(theme_url):
    topics_text = requests.get(theme_url).text
    topics_sel = Selector(text=topics_text)
    topics_message = topics_sel.xpath('//div[@id="threadlist"]'
                                      '/div[@class="bm_c"]'
                                      '//table[contains(@summary, "forum_")]'
                                      '/tbody[contains(@id, "thread_")]')
    for topic_message in topics_message:
        Title_ID = int(topic_message.xpath('./@id').extract()[0].split("_")[-1])
        Title = topic_message.xpath('./tr/th[1]/a[contains(@href, "thread-")]/text()').extract()[0]
        Title_content = topic_message.xpath('./tr/th[1]/a[contains(@href, "thread-")]/@href').extract()[0]
        Theme_name = topics_sel.xpath('//body[@id="nv_forum"]//div[@id="pt"]/div[@class="z"]'
                                      '/a[contains(@href, ".html")]/text()').extract()[0]
        Author = topic_message.xpath('./tr/td[2]/cite/a/text()').extract()[0]
        Create_time = topic_message.xpath('./tr/td[2]/em/span/text()').extract()[0]
        Create_time = datetime.strptime(Create_time, "%Y-%m-%d %H:%M")
        Last_answer_time = topic_message.xpath('./tr/td[4]/em/a/text()').extract()[0]
        Last_answer_time = datetime.strptime(Last_answer_time, "%Y-%m-%d %H:%M")
        Reply_num = topic_message.xpath('./tr/td[3]/a/text()').extract()[0]
        Check_num = topic_message.xpath('./tr/td[3]/em/text()').extract()[0]
        # print(Title_ID, type(Title_ID))
        # print(Author)
        # print(Title_content)
        # print(Create_time, type(Create_time))
        # print(Last_answer_time, type(Last_answer_time))
        # print(Theme_name)
        # print(Reply_num, Check_num)
        topic = Topic()
        topic.Title_ID = Title_ID
        topic.Title = Title
        topic.Theme_name = Theme_name
        topic.Author = Author
        topic.Content = Title_content
        topic.Create_time = Create_time
        topic.Last_answer_time = Last_answer_time
        topic.Reply_num = Reply_num
        topic.Check_num = Check_num
        existed_themes = Topic.select().where(Topic.Title_ID == topic.Title_ID)
        if existed_themes:
            topic.save()
        else:
            topic.save(force_insert=True)

    next_page_url = topics_sel.xpath('//div[@id="pgt"]/span/div[@class="pg"]'
                                     '/a[@class="nxt"]/@href').extract()
    if next_page_url:
        next_page_url = parse.urljoin(domain_url, next_page_url[0])
        get_topic_mess(next_page_url)


def get_topic():
    for theme in Theme.select():
        get_topic_mess(theme.Theme_url)


if __name__ == "__main__":
    # get_theme(domain_url)
    get_topic()
    a = '23142'
    print(a, type(a))
    b = int(a)
    print(b, type(b))
    l = []
    print(type(l))
    if not l:
        print("是空的")




        # theme_url = theme.Theme_url
        # topics_text = requests.get(theme_url).text
        # topics_sel = Selector(text=topics_text)
        # topics_message = topics_sel.xpath('//div[@id="threadlist"]'
        #                                   '/div[@class="bm_c"]'
        #                                   '//table[contains(@summary, "forum_")]'
        #                                   '/tbody[contains(@id, "thread_")]')
        # for topic_message in topics_message:
        #     topic = Topic()
        #     Title_ID = int(topic_message.xpath('./@id').extract()[0].split("_")[-1])
        #     Title = topic_message.xpath('./tr/th[1]/a[contains(@href, "thread-")]/text()').extract()[0]
        #     Theme_name = topics_sel.xpath('//body[@id="nv_forum"]//div[@id="pt"]/div[@class="z"]'
        #                                   '/a[contains(@href, ".html")]/text()').extract()[0]
        #     # Theme_name = theme.Name
        #     # topic_message.xpath('').extract()[0]
        #     Author = topic_message.xpath('./tr/td[2]/cite/a/text()').extract()[0]
        #     Create_time = topic_message.xpath('./tr/td[2]/em/span/text()').extract()[0]
        #     Create_time = datetime.strptime(Create_time, "%Y-%m-%d %H:%M")
        #     Last_answer_time = topic_message.xpath('./tr/td[4]/em/a/text()').extract()[0]
        #     Last_answer_time = datetime.strptime(Last_answer_time, "%Y-%m-%d %H:%M")
        #     Peply_num = topic_message.xpath('./tr/td[3]/a/text()').extract()[0]
        #     Check_num = topic_message.xpath('./tr/td[3]/em/text()').extract()[0]
        #     print(Title_ID, type(Title_ID))
        #     print(Title)
        #     print(Author)
        #     print(Create_time, type(Create_time))
        #     print(Last_answer_time, type(Last_answer_time))
        #     print(Theme_name)
        #     print(Peply_num, Check_num)
        #     next_page_url = topics_sel.xpath('//div[@id="pgt"]/span/div[@class="pg"]'
        #                                      '/a[@class="nxt"]/@href').extract()
        #     if next_page_url:
        #         next_page_url = parse.urljoin(domain_url, next_page_url[0])
        #     # print(Title_ID, type(Title_ID))
        #     # print(Author)
        #     # print(Create_time, type(Create_time))
        #     # print(Last_answer_time, type(Last_answer_time))
        #     # print(Theme_name)
        #     # print(Peply_num, Check_num)
        #     print(next_page_url)
        # for t in topics_message:
        #     if not t:
        #         print(theme_url)
