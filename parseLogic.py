import sys
import json
import os
import io
import re
import boolean
import itertools
from logicUtils import parseFunctions, compressItems, testReplacements
from convertLogic import writeFaultTree

def parseLogicBool(file_path):
    json_string = ""
    with io.open(file_path, 'r') as file:
        for line in file.readlines():
            json_string += line.split('#')[0].replace('\n', ' ')
    json_string = re.sub(' +', ' ', json_string)
    try:
        region_json = json.loads(json_string)
    except json.JSONDecodeError as error:
        raise Exception("JSON parse error around text:\n" + \
                        json_string[error.pos-35:error.pos+35] + "\n" + \
                        "                                   ^^\n")
    #print(region_json)
    alg = boolean.BooleanAlgebra()
    t, f, n, a, o, s = alg.definition()
    region_map = []
    for region in region_json:
        print(region['region_name'])
        pregion = region
        if ('locations' in region):
            for loc,rule in region['locations'].items():
                pregion['locations'][loc] = {'logic': rule, 'items':[], 'paths':[]}
                print("\t" + loc)
                rule = parseFunctions(rule)
                print("\t\t" + rule)
                boolrule = alg.parse(rule, simplify=True)
                syms = boolrule.symbols
                args = len(syms)
                if args > 0:
                    ttable = list(itertools.product([f, t], repeat=args))
                    total = len(ttable)
                    k = 0
                    for combo in ttable:
                        k = k + 1
                        print(str(k) + ' of ' + str(total), end='\r', flush=True)
                        tup = {}
                        evalrule = boolrule
                        for i,sym in enumerate(syms):
                            tup[sym] = combo[i]
                        r = evalrule.subs(tup, simplify=True)
                        if r:
                            pregion['locations'][loc]['items'].append(compressItems(syms, tup, s))
                            #print(pregion['locations'][loc]['items'])
                            #print(json.dumps(pregion['locations'][loc]))
                            #print(str(combo) + " " + str(r))
                else:
                    r = boolrule
                    st = "N/A"
                    if r:
                        pregion['locations'][loc]['items'].append(compressItems(syms, [True], s))
                        #print(json.dumps(pregion['locations'][loc]))
                        #print(st + " " + str(r))
        region_map.append(pregion)
    print(json.dumps(region_map))

def testLogic(file_path):
    json_string = ""
    with io.open(file_path, 'r') as file:
        for line in file.readlines():
            json_string += line.split('#')[0].replace('\n', ' ')
    json_string = re.sub(' +', ' ', json_string)
    try:
        region_json = json.loads(json_string)
    except json.JSONDecodeError as error:
        raise Exception("JSON parse error around text:\n" + \
                        json_string[error.pos-35:error.pos+35] + "\n" + \
                        "                                   ^^\n")
    #print(region_json)
    alg = boolean.BooleanAlgebra()
    t, f, n, a, o, s = alg.definition()
    for region in region_json:
        #print(region['region_name'])
        pregion = region
        if ('locations' in region):
            for loc,rule in region['locations'].items():
                pregion['locations'][loc] = {'logic': rule, 'items':[], 'paths':[]}
                #print("\t" + loc)
                rule = parseFunctions(rule)
                print("\t\t" + rule)
                boolrule = alg.parse(rule, simplify=True)
                syms = boolrule.symbols
                args = len(syms)
                if args > 0:
                    testReplacements(syms, s, pregion['locations'][loc]['logic'])

def parseLogicFT(file_path):
    json_string = ""
    with io.open(file_path, 'r') as file:
        for line in file.readlines():
            json_string += line.split('#')[0].replace('\n', ' ')
    json_string = re.sub(' +', ' ', json_string)
    try:
        region_json = json.loads(json_string)
    except json.JSONDecodeError as error:
        raise Exception("JSON parse error around text:\n" + \
                        json_string[error.pos-35:error.pos+35] + "\n" + \
                        "                                   ^^\n")
    #print(region_json)
    region_map = []
    for region in region_json:
        print(region['region_name'])
        pregion = region
        if ('locations' in region):
            for loc,rule in region['locations'].items():
                ft = writeFaultTree(file_path,rule,'./')

def parseLocLogicFT(file_path,loc):
    json_string = ""
    with io.open(file_path, 'r') as file:
        for line in file.readlines():
            json_string += line.split('#')[0].replace('\n', ' ')
    json_string = re.sub(' +', ' ', json_string)
    try:
        region_json = json.loads(json_string)
    except json.JSONDecodeError as error:
        raise Exception("JSON parse error around text:\n" + \
                        json_string[error.pos-35:error.pos+35] + "\n" + \
                        "                                   ^^\n")
    #print(region_json)
    region_map = []
    for region in region_json:
        print(region['region_name'])
        pregion = region
        if ('locations' in region):
            for l,rule in region['locations'].items():
                if l == loc:
                    ft = writeFaultTree(file_path,loc,rule,'./')


logicDir = '../OoTR-5.1/data/World/'
file_path = logicDir + 'Deku Tree.json'
#parseLogicBool(file_path)
#parseLogicFT(file_path)
parseLocLogicFT(file_path,'GS Deku Tree Basement Back Room')
#testLogic(file_path)
