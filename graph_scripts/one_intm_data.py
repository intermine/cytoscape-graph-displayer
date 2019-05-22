import requests
import json
from collections import defaultdict
import os
from intermine.webservice import Service
import math

def find_max_data_items(new_list,intermine,intermine_url):

    service = Service(intermine_url + "/service")
    max =0;
    for i in new_list:
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
    new_list=[]
    x = "http://registry.intermine.org/service/instances/" + intermine
    r = requests.get(x)
    dict = json.loads(r.text)
    intermine_url = dict["instance"]["url"]
    link = dict["instance"]["url"]+ "/service/model?format=json"
    r = requests.get(link)
    dict = json.loads(r.text)
    for i in dict['model']['classes'].keys():
        new_list.append(i)


# new_list is a list of all the classes

    f = open("one_intm_data_json", "a")
    os.remove("one_intm_data_json")
    f = open("one_intm_data_json", "a")
    f.write('{"elements": [{ "group": "nodes",')
    count =0
    max = find_max_data_items(new_list, intermine,intermine_url)
    #print(max)
    for i in new_list:
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

    for i in dict['model']['classes'].keys():
        if (dict['model']['classes'][i]['references']):
            for j in dict['model']['classes'][i]['references'].keys():
                if dict['model']['classes'][i]['references'][j]['referencedType'] in new_list:
                    count = count+1
                    f.write(', {')
                    f.write('"data": {"id": "edge')
                    f.write(str(count))
                    f.write('", "source": "')
                    f.write(i)
                    f.write('", "target": "')
                    f.write(dict['model']['classes'][i]['references'][j]['referencedType'])
                    f.write('"')
                    f.write('}')
                    f.write('}')
        if (dict['model']['classes'][i]['collections']):
            for j in dict['model']['classes'][i]['collections'].keys():
                if dict['model']['classes'][i]['collections'][j]['referencedType'] in new_list:
                    count = count+1
                    f.write(', {')
                    f.write('"data": {"id": "edge')
                    f.write(str(count))
                    f.write('", "source": "')
                    f.write(i)
                    f.write('", "target": "')
                    f.write(dict['model']['classes'][i]['collections'][j]['referencedType'])
                    f.write('"')
                    f.write('}')
                    f.write('}')
        if (not dict['model']['classes'][i]['collections']) and (not dict['model']['classes'][i]['references']):
            count = count+1
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
    f.write('],"style": [{"selector":  "node","style": {"label": "data(id)"}}]}')
find_classes('flymine')
'''
>>>import one_intm_data as o
>>>o.find_classes('flymine')
'''
