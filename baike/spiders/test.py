import scrapy.http.request
import scrapy.link
# s='https://baike.baidu.com/item/苹果公司/304038?fromtitle=苹果&fromid=6011223'
# if s.rfind('?')!=-1:
#     s=s.split('?')
#     print(s)
#     id_s=s[1].rfind('fromid=')+7
#     id_e=s[1].rfind('#')
#     if id_e==-1:
#         id_e=len(s)
#     print(s[1][id_s:id_e])
#
#     word_s=s[1].find('fromtitle=')+10
#     word_e=s[1].find('&')
#     print(s[1][word_s:word_e])
#
# s1='https://baike.baidu.com/item/史记·2016?fr=navbar'
# s2='https://baike.baidu.com/item/山东省人民政府办公厅关于印发山东省加快推进畜禽养殖废弃物资源化利用实施方案的通知/124h33'
#s1='https://baike.baidu.com/item/云南/206207?fromtitle=云南省&fromid=18664752#10'
# s1='https://baike.baidu.com/item/云南/19158376#viewPageContent'
# # s1='https://baike.baidu.com/item/九十九龙潭'
# # s1=s1.split('?')
# s1=s1[s1.find('/item/')+6:]
# import re
# print(re.split('[#]',s1))
# s1_e=s1.find('?')
# if s1_e!=-1:
#     print(s1[:s1_e])
# elif s1.find('#')!=-1:
#     print()
# print(int(None))
# print(int(s1[0][s1[0].rfind('/')+1:]))

#同义词处理过程，如果为同义词则返回（url，同义词，同义词id），否则不是同义词
# def process_synonym_url(url):
#     if url.rfind('?')!=-1:
#         url = url.split('?')
#         id_s = url[1].rfind('fromid=') + 7
#         id_e = url[1].rfind('#')
#         if id_e == -1:
#             id_e = len(s)
#         word_s = url[1].find('fromtitle=') + 10
#         word_e = url[1].find('&')
#         return (url[0],s[1][word_s:word_e],s[1][id_s:id_e])
#     return -1

#普通的url链接处理，例如https://baike.baidu.com/item/%E5%BD%AD%E5%88%A9%E9%93%AD/3930707?fr=aladdin
# def process_word_url(url):
#     url.split('?')
#     return re.findall('\d*$',url[0])