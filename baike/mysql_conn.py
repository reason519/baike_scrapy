import MySQLdb


class Mysql:

    dsn = ("localhost","root","czr455163","baike")

    def __init__(self):
        self.conn = MySQLdb.connect(*self.dsn)
        self.cursor = self.conn.cursor()
        self.conn.set_character_set('utf8')
        self.cursor.execute('SET NAMES utf8;')
        self.cursor.execute('SET CHARACTER SET utf8;')
        self.cursor.execute('SET character_set_connection=utf8;')

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.close()

    #删除表格
    def drop_table(self,table_name):
        self.cursor.execute("DROP TABLE IF EXISTS "+table_name)

    #查看表
    def show_tables(self):
        res=self.cursor.execute("show tables")
        print(self.cursor.fetchall())

    #创建索引
    def create_index(self):
        self.cursor.execute("""alter table wordinfo add  UNIQUE index wordinfourl(URL);""")
        self.cursor.execute("""alter table urlfilter add  UNIQUE index urlfilterurl(URL);""")
        self.cursor.execute("""alter table itemfilter add  UNIQUE index itemfilterurl(URL);""")
        self.cursor.execute("""alter table viewfilter add  UNIQUE index viewfilterurl(URL);""")
        self.cursor.execute("""alter table subviewfilter add  UNIQUE index subviewfilterurl(URL);""")
       # self.conn.commit()
    #创建表
    def create_table_wordinfo(self):
        sql= """CREATE TABLE wordinfo (
         ID int(12) NOT NULL auto_increment,
         URL  VARCHAR(120) NOT NULL,
         WORD  VARCHAR(60) NOT NULL,
         WORDID INT,  
         POLYSEMY VARCHAR (60),
         SYNONYM VARCHAR (60),
         PRIMARY KEY (ID))character set = utf8;"""
        self.cursor.execute(sql)
       # self.conn.commit()

    def create_table_urlfilter(self):
        sql="""CREATE TABLE urlfilter(
        URL VARCHAR (120) NOT NULL,
        PRIMARY KEY (URL))character set = utf8;"""
        self.cursor.execute(sql)

#由于itemfilter表中重复的元素较多可能千万以上为提高效率所以url缩短，去除http://baike.baidu.com/item/
    def create_table_itemfilter(self):
        sql="""CREATE TABLE itemfilter(
        URL VARCHAR (40) NOT NULL,
        PRIMARY KEY (URL))character set = utf8;"""
        self.cursor.execute(sql)

    def create_table_viewfilter(self):
        sql="""CREATE TABLE viewfilter(
        URL VARCHAR (120) NOT NULL,
        PRIMARY KEY (URL))character set = utf8;"""
        self.cursor.execute(sql)

    def create_table_subviewfilter(self):
        sql="""CREATE TABLE subviewfilter(
        URL VARCHAR (120) NOT NULL,
        PRIMARY KEY (URL))character set = utf8;"""
        self.cursor.execute(sql)

    #插入操作
    def insert_wordinfo(self,id,word,wordid=0,polysemy='',synonym=''):
        sql="""INSERT INTO wordinfo(URL,WORD,WORDID,POLYSEMY,SYNONYM) VALUES ('%s','%s','%d','%s','%s')"""% \
            (id,word,wordid,polysemy,synonym)
        self.cursor.execute(sql)
        self.conn.commit()

    def insert_urlfilter(self,url):
        sql="""INSERT INTO urlfilter(URL) VALUES('%s')"""%(url)
        self.cursor.execute(sql)
        self.conn.commit()

    def insert_itemfilter(self,url):
        sql="""INSERT INTO itemfilter(URL) VALUES('%s')"""%(url)
        self.cursor.execute(sql)
        self.conn.commit()

    def insert_viewfilter(self,url):
        sql="""INSERT INTO viewfilter(URL) VALUES('%s')"""%(url)
        self.cursor.execute(sql)
        self.conn.commit()

    def insert_subviewfilter(self,url):
        sql="""INSERT INTO subviewfilter(URL) VALUES('%s')"""%(url)
        self.cursor.execute(sql)
        self.conn.commit()

    #查找
    def select_urlfilter(self,url):
        sql="""SELECT * FROM urlfilter WHERE id =('%s')"""%(url)
        self.cursor.execute(sql)
        res=self.cursor.fetchall()
        return res
