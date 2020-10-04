import sys
import json
import os
import io
import re
from logicUtils import parseFunctions

def buildGate(sLogic, n=0, gateI=0):
    g = ''
    be = ''
    c = ''
    w = ''
    gn = ''
    gi = gateI
    s = ''
    i = n
    rg = []
    bes = []
    while True:
        c = sLogic[i:i+1]
        if (c == '('):
            # recurse to new gate
            ts, ti, tg, tTop, trg, tbes = buildGate(sLogic, i+1, gi)
            rg.append(ts)
            for og in trg:
                rg.append(og)
            for ob in tbes:
                bes.append(ob)
            gi = tg
            gn = 'G' + str(tTop)
            #advance to i
            i = ti
        elif (c == ')'):
            # return to parent
            be = w
            bes.append(be)
            if (gn == ''):
                s = s + '<basic-event name="' + be + '"/>\n'
            else:
                s = s + '<gate name="' + gn + '"/>\n'
                gn = ''
            s = s + '</' + g + '>\n'
            s = s + '</define-gate>\n'
            return s, i, gi, gateI, rg, bes
        elif (c == ' '):
            # process grammar, either event or command
            if (w == 'and'):
                # and gate
                if (g == 'and'):
                    # add child to gate
                    if (gn == ''):
                        s = s + '<basic-event name="' + be + '"/>\n'
                    else:
                        s = s + '<gate name="' + gn + '"/>\n'
                        gn = ''
                elif (g == ''):
                    # new gate
                    s = s + '<define-gate name="G' + str(gi) + '">\n'
                    s = s + '<label>Gate ' + str(gi) + '</label>\n'
                    s = s + '<and>\n'
                    if (gn == ''):
                        s = s + '<basic-event name="' + be + '"/>\n'
                    else:
                        s = s + '<gate name="' + gn + '"/>\n'
                        gn = ''
                    gi = gi + 1
                else:
                    # ambiguous grouping dependent on order of operations
                    # don't handle this for now, throw an error to verify
                    # this actually exists
                    # AND has precedence in Python
                    raise Exception('logic', 'ambiguous_and')
                g = 'and'
                w = ''
            elif (w == 'or'):
                # or gate
                if (g == 'or'):
                    # add child to gate
                    if (gn == ''):
                        s = s + '<basic-event name="' + be + '"/>\n'
                    else:
                        s = s + '<gate name="' + gn + '"/>\n'
                        gn = ''
                elif (g == ''):
                    # new gate
                    s = s + '<define-gate name="G' + str(gi) + '">\n'
                    s = s + '<label>Gate ' + str(gi) + '</label>\n'
                    s = s + '<or>\n'
                    if (gn == ''):
                        s = s + '<basic-event name="' + be + '"/>\n'
                    else:
                        s = s + '<gate name="' + be + '"/>\n'
                        gn = ''
                    gi = gi + 1
                else:
                    # ambiguous grouping dependent on order of operations
                    # don't handle this for now, throw an error to verify
                    # this actually exists
                    # AND has precedence in Python
                    raise Exception('logic', 'ambiguous_or')
                g = 'or'
                w = ''
            else:
                # basic event
                be = w
                w = ''
                bes.append(be)
        elif (i == len(sLogic)):
            # last event in string, not recursed
            be = w
            bes.append(be)
            if (s == ''):
                # only one event in the logic, no gates
                s = sLogic
            else:
                if (gn == ''):
                    s = s + '<basic-event name="' + be + '"/>\n'
                else:
                    s = s + '<gate name="' + gn + '"/>\n'
                    gn = ''
                s = s + '</' + g + '>\n'
                s = s + '</define-gate>\n'
                for og in rg:
                    s = s + og
                md = buildEvents(bes)
            s = '<?xml version="1.0"?>\n\n<opsa-mef>\n<define-fault-tree name="OoTR">\n' + s + '</define-fault-tree>\n<model-data>\n' + md + '</model-data>\n</opsa-mef>'
            return s
        else:
            w = w + c
        i = i + 1

def buildEvents(bes):
    s = ''
    for be in bes:
        if (be != ''):
            s = s + '<define-basic-event name="' + be + '">\n<label>' + be + '</label>\n<float value="1.000000e-001"/>\n</define-basic-event>\n'
    return s

def writeFaultTree(location, loc, rule, outpath):
    logic_ft = outpath + loc + '.xml'
    #logic_string = region_json[1]['locations']['Ice Cavern Iron Boots Chest']
    #logic_string = logic_string.replace('can_use(Dins_Fire)','(Dins_Fire and Magic_Meter)')
    logic_string = parseFunctions(rule)
    #print(logic_string)
    ft = buildGate(logic_string)
    with io.open(logic_ft, 'w') as f:
        f.write(ft)
    #print(ft)
    return logic_ft

logicDir = '../OoTR-5.1/data/World/'
file_path = logicDir + 'Deku Tree.json'

#writeFaultTree(file_path,'./')