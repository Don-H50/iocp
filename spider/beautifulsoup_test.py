import re
import requests
from bs4 import BeautifulSoup
# beautifulsoup官方文档有详细使用方法

html = """"
    <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>bobby基本信息</title>
        $(document).ready(function () {
            $.ajax({

            })
        })
</head>
<bo dy>
    <div id="info">
        <p style="color: blue">讲师信息</p>
        <div class="teacher_info info">
            python全栈工程师，7年工作经验，喜欢钻研python技术，对爬虫、
            web开发以及机器学习有浓厚的兴趣，关注前沿技术以及发展趋势。
            <p class="age">年龄: 29</p>
            <p class="name namebobby" bobby-bott="hello">姓名: bobby</p>
            <p class="work_years">工作年限: 7年</p>
            <p class="position">职位: python开发工程师</p>
        </div>
        <p style="color: aquamarine">课程信息</p>
        <table class="courses">
          <tr>
            <th>课程名</th>
            <th>讲师</th>
            <th>地址</th>
          </tr>
          <tr>
            <td>django打造在线教育</td>
            <td>bobby</td>
            <td><a href="https://coding.imooc.com/class/78.html">访问</a></td>
          </tr>
          <tr>
            <td>python高级编程</td>
            <td>bobby</td>
            <td><a href="https://coding.imooc.com/class/200.html">访问</a></td>
          </tr>
          <tr>
            <td>scrapy分布式爬虫</td>
            <td>bobby</td>
            <td><a href="https://coding.imooc.com/class/92.html">访问</a></td>
          </tr>
          <tr>
            <td>django rest framework打造生鲜电商</td>
            <td>bobby</td>
            <td><a href="https://coding.imooc.com/class/131.html">访问</a></td>
          </tr>
          <tr>
            <td>tornado从入门到精通</td>
            <td>bobby</td>
            <td><a href="https://coding.imooc.com/class/290.html">访问</a></td>
          </tr>
        </table>
    </div>

</body>
</html>

"""

# 参数：纯文本值、解析引擎 后续操作都是基于bs对象来操作
bs = BeautifulSoup(html, "html.parser")
title_tag = bs.title    # 提取的是Tag類
print(title_tag.string)
print(title_tag)

div_tag = bs.div
div_tags = bs.find_all("div")
print(div_tag)
print("\n")

# find的幾種定位方式,通过id来定位是更常用的定位方式(其中id可用正则来表示
# div_tag = bs.find("div")
# id_tag = bs.find(id = "info")
# divAid_tag = bs.find("div", id = "info")
# reg_tag = bs.find("div", id = re.compile("info-\d+"))
# mes_tag = bs.find(string="scrapy分布式爬虫")
# mesAreg_tag = bs.find(string=re.compile("info-\d+"))


# childrens = reg_tag.contents    # 提取子元素
# childrens = reg_tag.descendants # 提取子元素的子元素
# for child in childrens:
#     if child.name:
#         print(child.name)
# print("\n")
#
# parents = bs.find("p", {"class":"name"}).parents
# for parent in parents:
#     if parent.name:
#         print(parent.name)
# print("\n")
#
siblings = bs.find("p", {"class" : "name"}).next_siblings # previous_siblings獲得前面的兄弟節點
for sibling in siblings:
    if sibling.name:
        print(sibling.name)
        print(sibling.string)
print("\n")
#
# # 獲取屬性 多值屬性不影響find方法 class = “name bobby-name” 對於未知屬性的話，bs會返回字符串而不是list的形式
# name_tag = bs.find("p", {"class":"name"})
# print(name_tag["class"])
# print(name_tag["bobby-bott"])
# print(name_tag.get("class"))
# print(reg_tag)
# 學習對應庫的接口API
# 換一個庫就要重新學習
# xpath和css選擇器-通用的，任何支持的庫都一樣
# 学习xpath需要使用几个库来做操作 lxml or scrapy selector

# ==================================================
# res = requests.get("http://www.baidu.com")
# print(res.text)
#
# baidu = BeautifulSoup(res.text, "html.parser")
# # baidu_tag = baidu.find()
# baidu_title = baidu.title
# print(baidu_title.string)
# print(baidu_title)

# 引入selector这样就有了xpath的解析库了
# xpath可以作为常量赋值给变量使用
# xpath根据路径直接获取到对应标签下的值
from scrapy import Selector

path = "//*[@id='info']/div/p/text()"
tea_path = "//div[@class='teacher_info info']/text()"
teac_path = "//div[contains(@class, 'teacher_i')]/p/text()"
get_teacherdiv_class = "//div[contains(@class, 'teacher_i')]/@class"
sel = Selector(text=html)
tag = sel.xpath(path)
tag_r = sel.xpath("//div[@id='info']/div[1]/p/text()")
ex_tag = tag.extract()
print(tag)
print(ex_tag)
print(sel.xpath(get_teacherdiv_class).extract()[0])

sel_j = sel.xpath(path)
if sel_j:
    ex_tag_j = sel_j.extract()[0]
    print("ex_tag_j :"+ex_tag_j)
tea_sel_j = sel.xpath(tea_path)
if tea_sel_j:
    ex_tea_tag_j = tea_sel_j.extract()[0]
    print("ex_tea_tag_j :"+ex_tea_tag_j)


# 获得teacher的年龄姓名和工作年限 打印出来 一句话处理
mul_path = "//div[contains(@class,'teacher')]/p[@class='age']|//div[contains(@class,'teacher')]/p[@class='work_years']\
           |//div[contains(@class,'teacher')]/p[contains(@class,'name')]/text()"
mul_sel = sel.xpath(mul_path)
if sel_j:
    ex_mul_sel = mul_sel.extract()[1]
    print("ex_mul_sel :"+ex_mul_sel)









