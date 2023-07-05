from datetime import date

from peewee import *
# from wangdao_spider.SQL_models import *

"""
使用peewee创建表
    
对表进行增删改查
    
"""
db = MySQLDatabase('pro_1', host='127.0.0.1', port=3308, user='root', password='root')


# 定义表的结构,以对象的形式进行操作

class Person(Model):
    name = CharField()
    birthday = DateField()

    class Meta:
        database = db   # This model uses the "people.db" database.
        table_name = "bir"


class Theme(Model):
    id = IntegerField(primary_key=True)
    name = CharField()
    theme_num = IntegerField()
    theme_rate = IntegerField()
    theme_content = TextField(null=True)
    print("Theme_connect")

    class Meta:
        database = db


# 数据增删改查

if __name__ == '__main__':
    # db.create_tables([Person])
    # '''保存数据'''
    # my = Person(name='Li', birthday=date(2000, 3, 18))
    # my.save()
    # her = Person(name='Zhang', birthday=date(1999, 5, 17))
    # her.save()
    '''查找数据
    单条查询:
        select * from person where name='Li'
        my_info = Person.select().where(Person.name == 'Li').get()    #该方法与传统的sql语句相似,更精简的如下
    多条查询:
        1.非指定值的全局取
        2.指定值取重复
    '''
    try:
        info = Person.get(Person.name == 'Lsi')
    except:
        print("It's not value here")
    my_info = Person.get(Person.name == 'Li')
    print(my_info.birthday)
    # 非指定值的全局取
    for person in Person.select():
        print(person.id, person.name, person.birthday)
    # 指定值取重复 ps:query可当作list来操作(内部实现了getitem这个方法),且该方法不会抛出异常
    print('===========全局取值与指定取值的分割================')
    query = Person.select().where(Person.name == 'Li')
    for q in query:
        print(q.id, q.name, q.birthday)
    '''修改数据
        是基于保存和查询数据的基础上进行的,我现在来改id为6的所有信息
        步骤:
        1.查询数据
        2.保存数据
    '''
    query_change = Person.select().where(Person.id == 6).get()
    query_change.name = 'xiao'
    query_change.birthday = date(90, 1, 3)
    query_change.save()

    the = Theme(Theme_ID='2', name="sd", theme_num=12, theme_rate=1, theme_content="saaaaadas")
    print("save")
    the.save(force_insert=True)

    my = Person(name='Lsid', birthday=date(2000, 3, 18))
    my.save()

    # theme = Theme()
    #
    # theme.Theme_ID = 112
    # theme.Name = "hh"
    # theme.Theme_num = 12
    # theme.Theme_rate = 1
    # theme.Theme_content = "sadds"
    # theme.save()

