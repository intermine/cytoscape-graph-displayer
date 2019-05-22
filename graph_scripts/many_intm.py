import requests
import json
from collections import defaultdict
import os



def find_classes(*intermines):
    new_dict = defaultdict(list)
    classes = defaultdict(list)
    new_list2 = []
    for i in range(0,len(intermines)):
        x = "http://registry.intermine.org/service/instances/" + intermines[i]
        r = requests.get(x)
        dict = json.loads(r.text)
        link = dict["instance"]["url"]+ "/service/model?format=json"
        r = requests.get(link)
        dict = json.loads(r.text)
        for j in dict['model']['classes'].keys():
            new_dict[intermines[i]].append(j)
            new_list2.append(j)

    #new_list contains all the data in a dict such that {'intermine': [classes]}

    #distinct_classes contains all the data in a dict such that {'intermine': [classes]}
    distinct_classes = set(new_list2)
    distinct_classes = list(distinct_classes)

    #distinct_classes contains all the distinct classes taking all intermines
    for i in distinct_classes:
        for j in new_dict.keys():
            for k in range(0,len(new_dict[j])):
                if(i == new_dict[j][k]):
                    classes[i].append(j)


    #makes nodes in the json file for yo's script
    f = open("many_intm_json", "a")
    os.remove("many_intm_json")
    f = open("many_intm_json", "a")
    f.write('{"elements": [{ "group": "nodes",')
    count =0
    for i in classes.keys():
        if(count!=0):
            f.write(', {')
        f.write('"data": {"id": "')
        f.write(i)
        f.write('"')
        f.write(', "weight":')
        a = 1 - len(classes[i])/len(intermines)
        f.write(str(a))
        f.write('}, "classes": [')
        for j in classes[i]:
            if(j!=classes[i][0]):
                f.write(',')
            f.write('"' +j +'"')
        f.write(']')
        f.write('}')
        count = count+1


    # developing edges in the json file

    for i in range(0,len(intermines)):
        x = "http://registry.intermine.org/service/instances/" + intermines[i]
        r = requests.get(x)
        dict = json.loads(r.text)
        link = dict["instance"]["url"]+ "/service/model?format=json"
        r = requests.get(link)
        dict = json.loads(r.text)
        count =0
        for i in dict['model']['classes'].keys():
            count = count+1
            if not dict['model']['classes'][i]['extends']:
                f.write(', {')
                f.write('"data": {"id": "edge')
                f.write(str(count))
                f.write('", "source": "')
                f.write(i)
                f.write('", "target": "')
                f.write(i)
                f.write('"')

                f.write('}')
                f.write('}')
            else:
                for j in dict['model']['classes'][i]['extends']:
                        f.write(', {')
                        f.write('"data": {"id": "edge')
                        f.write(str(count))
                        f.write('", "source": "')
                        f.write(i)
                        f.write('", "target": "')
                        f.write(j)
                        f.write('"')
                        f.write('}')
                        f.write('}')
    f.write('],"style": [{"selector":  "node","style": {"label": "data(id)"}}]}')

#find_classes("flymine")
#find_classes("ratmine", "mousemine","flymine","humanmine","bmapmine","chomine","beanmine","bovinemine","chickpeamine","cowpeamine","grapemine","hymenopteramine","indigomine","legumemine","maizemine","medicmine","mitominer","modmine","oakmine","peanutmine","phytomine","planmine","repetdbmine","soymine","targetmine","thalemine","wheatmine","wormmine","xenmine","yeastmine","zebrafishmine")
find_classes("flymine", "humanmine","mousemine","ratmine")
'''
>>>import many_intm as m
>>>m.find_classes("flymine", "humanmine","mousemine","ratmine")
copy the contents of many_intm_json in web application
'''
