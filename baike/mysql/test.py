from baike_12_19.baike.mysql.mysqlconn import Mysql

with Mysql() as db:
    db.drop_table('wordinfo')
    db.drop_table('urlfilter')
    db.drop_table("itemfilter")
    db.drop_table("viewfilter")
    db.drop_table("subviewfilter")
    db.create_table_wordinfo()
    db.create_table_urlfilter()
    db.create_table_itemfilter()
    db.create_table_viewfilter()
    db.create_table_subviewfilter()
  #  db.create_index()
    db.show_tables()

    #测试insert_wordinfo
    # url='https://baike.baidu.com/item/%E8%89%BE%E4%BC%A6%C2%B7%E9%BA%A6%E5%B8%AD%E6%A3%AE%C2%B7%E5%9B%BE%E'
    # db.insert_wordinfo(url,'苹果')

    #测试insert_urlfilter
    # url='https://baike.baidu.com/item/%E8%89%BE%E4%BC%A6%C2%B7%E9%BA%A6%E5%B8%AD%E6%A3%AE%C2%B7%E5%9B%BE%E'
    # try:
    #     print(db.insert_urlfilter(url))
    #     print("aa")
    # except:
    #     print("sss")
    # print(db.select_urlfilter(url))

    #https://baike.baidu.com/item/%E8%89%BE%E4%BC%A6%C2%B7%E9%BA%A6%E5%B8%AD%E6%A3%AE%C2%B7%E5%9B%BE%E7%81%B5
# from urllib.request import unquote
# s=unquote('https://baike.baidu.com/item/%E8%89%BE%E4%BC%A6%C2%B7%E9%BA%A6%E5%B8%AD%E6%A3%AE%C2%B7%E5%9B%BE%E7%81%B5')
# print(s.find('#'),len(s))
# a='https://baike.baidu.com/item/%E9%B2%81%E8%BF%85/20721795#viewPageContent'
# print(unquote(a[:a.find('#')]))


