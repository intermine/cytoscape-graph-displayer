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


    #nodes
    f = open("one_intm_one_temp_json", "a")
    os.remove("one_intm_one_temp_json")
    f = open("one_intm_one_temp_json", "a")
    f.write('{"elements": [{ "group": "nodes",')
    count =0

    for i in new_list:
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

#check_classes('flymine','Gene_RegionLocation')
'''
>>>import one_intm_one_temp as o
>>>o.check_classes('flymine','Gene_RegionLocation')
'''
