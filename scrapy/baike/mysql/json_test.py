import json
import jieba

with open('../spiders/baike.json',encoding='utf8') as f:
    count=0;
    for line in f:
        # json_str=json.dumps(line,ensure_ascii=False)
        data=json.loads(line)
        count+=1
        # print(count)
        #print(type(data))
        #print(len(data.get('summarylinks','')[0]),len(data.get('summarylinks','')[1]))
        # print(data.get('summary',None))
        # #res=jieba.cut(data.get('summary',None))
        # print(data.get('content',None))
        # print(data.get('basicinfo',None))
        print(len(data.get('basicinfo', None)[0]), len(data.get('basicinfo',None)[1]))
        # print(data.get('contentlinks',None))
        # print(len(data.get('contentlinks', None)[0]), len(data.get('contentlinks',None)[1]))
        # print(data.get('summarylinks',None))
    # data=json.loads(f,encoding='utf-8')
