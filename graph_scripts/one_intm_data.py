import requests
import json
from collections import defaultdict
import os
from intermine.webservice import Service
import math

def find_max_data_items(class_dict,intermine,intermine_url):

    service = Service(intermine_url + "/service")
    max =0;
    for i in class_dict.keys():
        query = service.new_query(i)
        query.add_view(i + ".*")
        if(query.count()>=max):
            max=query.count()
    return max



def find_data_items(class1,intermine_url):
    service = Service(intermine_url + "/service")
    query = service.new_query(class1)
    query.add_view(class1 + ".*")
    return query.count()


def find_classes(intermine):
    class_dict = defaultdict(list)
    x = "http://registry.intermine.org/service/instances/" + intermine
    r = requests.get(x)
    dict = json.loads(r.text)
    intermine_url = dict["instance"]["url"]
    link = dict["instance"]["url"]+ "/service/model?format=json"
    r = requests.get(link)
    dict = json.loads(r.text)
    for i in dict['model']['classes'].keys():
        if dict['model']['classes'][i]['extends']:
            for j in dict['model']['classes'][i]['extends']:
                class_dict[i].append(j)
        else:
            class_dict[i]=[]

# class_dict is a dictionary that is like this {class1 : [class2], class2: [class5]...}

    #print(class_dict)
    f = open("one_intm_data_json", "a")
    os.remove("one_intm_data_json")
    f = open("one_intm_data_json", "a")
    f.write('{"elements": [{ "group": "nodes",')
    count =0
    max = find_max_data_items(class_dict, intermine,intermine_url)
    #print(max)
    for i in class_dict.keys():
        if(count!=0):
            f.write(', {')
        f.write('"data": {"id": "')
        f.write(i)
        f.write('"')
        f.write(', "weight":')
        weight = round(math.log(find_data_items(i,intermine_url)+1,max),2)
        f.write(str(weight))
        f.write('}')
        f.write('}')
        count = count+1


# developing edges in the json file
    count=0

    for i in class_dict.keys():
        count = count+1
        for j in class_dict[i]:
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



'''
>>>import one_intm_data as o
>>>o.find_classes('flymine')
'''
