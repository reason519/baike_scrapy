import json
import jieba

<<<<<<< HEAD
with open('E:\\scrapy/baike.json',encoding='utf8') as f:
=======
with open('D:\\data\\scrapy/baike.json',encoding='utf8') as f:
>>>>>>> 2015cbfd377bcbf9c61963fd8307fd9182ebf78c
    count=0;
    for line in f:
        # json_str=json.dumps(line,ensure_ascii=False)
        data=json.loads(line)
        print(data.get('title',None),data.get('url',None))
        #count+=1
        #print(count)
        #print(type(data))
        #print(len(data.get('summarylinks','')[0]),len(data.get('summarylinks','')[1]))
        # print(data.get('summary',None))
        # #res=jieba.cut(data.get('summary',None))
        #print(data.get('content',None))
        # print(data.get('basicinfo',None))
        #print(len(data.get('basicinfo', None)[0]), len(data.get('basicinfo',None)[1]))
        # print(data.get('contentlinks',None))
<<<<<<< HEAD
       # print(len(data.get('contentlinks', None)[0]), len(data.get('contentlinks',None)[1]))
=======
        print(len(data.get('contentlinks', None)[0]), len(data.get('contentlinks',None)[1]))
>>>>>>> 2015cbfd377bcbf9c61963fd8307fd9182ebf78c
        # print(data.get('summarylinks',None))
    # data=json.loads(f,encoding='utf-8')
