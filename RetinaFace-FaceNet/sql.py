"""

NAME : sql

USER : admin

DATE : 10/10/2023

PROJECT_NAME : RetinaFace-FaceNet

CSDN : friklogff
"""
 Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql


# 能避开全局变量就避开全局变量.

# 写入文件
class CaipiaoPipeline:
    # 引擎
    def open_spider(self, spider):  # 引擎中对"管道(pipeline)"的一个设计
        print("我爱黎明")
        # 打开文件
        self.f = open('data2.csv', mode="a", encoding="utf-8")

    def close_spider(self, spider):
        print("你爱个毛线")
        # 关闭文件
        self.f.close()

    # 每次spider返回一条数据. 这里就要运行一次.
    def process_item(self, item, spider):
        # print("===>", item)
        # # 期号,红球1_红球2_红球3..,篮球
        # with open("data.csv", mode="a", encoding="utf-8") as f:
        #     f.write(item['qi'])
        #     f.write(",")
        #     f.write("_".join(item['hong']))
        #     f.write(",")
        #     f.write(item['lan'])
        #     f.write("\n")
        self.f.write(item['qi'])
        self.f.write(",")
        self.f.write("_".join(item['hong']))
        self.f.write(",")
        self.f.write(item['lan'])
        self.f.write("\n")
        return item

# 写入数据库
class CaipiaoPipeline_MySQL:

    def open_spider(self, spider):
        self.conn = pymysql.connect(host="127.0.0.1",
                                    port=3306,
                                    user="root",
                                    password="1300982918",
                                    database="test")

    def close_spider(self, spider):
        self.conn.close()

    # 每次spider返回一条数据. 这里就要运行一次.
    def process_item(self, item, spider):
        try:
            # 2.弄个游标
            cursor = self.conn.cursor()
            # 3.写入数据
            sql = "insert into shuangseqiu(qi, hong, lan) values(%s, %s, %s)"
            cursor.execute(sql, (item['qi'], "_".join(item['hong']), item['lan']))
            # 4.提交事务
            self.conn.commit()
        except Exception as e:
            # 5.如果报错. 回滚
            print(e)
            self.conn.rollback()
        print("存储完毕")
        return item  # 如果不return. 后续的管道将接受不到数据

