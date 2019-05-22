import requests
import json
from collections import defaultdict
import os
from intermine.webservice import Service
from intermine.webservice import Model

def find_template_classes(intermine, template):
    classes_in_template=[]
    x = "http://registry.intermine.org/service/instances/" + intermine
    r = requests.get(x)
    dict = json.loads(r.text)
    intermine_url = dict["instance"]["url"]
    model = Model(dict["instance"]["url"]+ "/service/model")
    link = dict["instance"]["url"]+ "/service/templates?format=json"
    r = requests.get(link)
    dict = json.loads(r.text)
    for i in dict['templates'].keys():
        if (i==template):
            for j in dict['templates'][i]['select']:
                j = j.split('.')
                j = '.'.join(j[:-1])
                y = model.get_class(j)
                classes_in_template.append(y.name)

    classes_in_template = list(set(classes_in_template))
    return classes_in_template




def check_classes(intermine,template):
    classes_in_template = find_template_classes(intermine,template)
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
    f = open("one_intm_one_temp_json", "a")
    os.remove("one_intm_one_temp_json")
    f = open("one_intm_one_temp_json", "a")
    f.write('{"elements": [{ "group": "nodes",')
    count =0

    for i in class_dict.keys():
        if(count!=0):
            f.write(', {')
        f.write('"data": {"id": "')
        f.write(i)
        f.write('"')
        f.write(', "weight":')
        if i in classes_in_template:
            val = 1
        else:
            val = 0
        f.write(str(val))
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
>>>import one_intm_one_temp as o
>>>o.check_classes('flymine','Gene_RegionLocation')
'''
