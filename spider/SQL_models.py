from peewee import *

"""链接数据库、创建模型父类（功能：链接数据库）、创建表"""
db = MySQLDatabase("pro_1", host="127.0.0.1", port=3308, user="root", password="root", charset='utf8')


class BaseModel(Model):
    class Meta:
        database = db


class Theme(BaseModel):
    Theme_ID = CharField(primary_key=True)
    Name = CharField()
    Theme_num = IntegerField()
    Theme_rate = IntegerField()
    Theme_content = TextField(null=True)
    Theme_url = CharField()
    print("Theme_connect")


class Topic(BaseModel):
    Title_ID = IntegerField(primary_key=True)
    Title = CharField()
    Theme_name = CharField()
    Author = CharField()
    Content = TextField()
    Create_time = DateTimeField()
    Last_answer_time = DateTimeField()
    Reply_num = IntegerField()
    Check_num = IntegerField()


class Author(BaseModel):
    UID = IntegerField(primary_key=True)
    User_name = CharField()
    User_team = CharField()
    Reply_num = IntegerField(default=0)
    Topic_num = IntegerField(default=0)
    User_Integral = IntegerField(default=0)
    User_prestige = IntegerField(default=0)
    User_contribution = IntegerField(default=0)
    Register_time = DateTimeField(null=True)
    Last_access_time = DateTimeField(null=True)


if __name__ == "__main__":
    db.create_tables([Theme, Topic, Author])
