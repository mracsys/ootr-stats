import sys
import json
# OoTR source code location
sys.path.insert(0, '../../OoT-Randomizer-R')
import os
import pyodbc
from LocationList import location_table
from HintList import hintTable

# Spoiler log location
spoilers = '../spoilersS42S/'

conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=MAGELLAN\SQLEXPRESS;'
                      'Database=OotrStatsS42S;'
                      'Trusted_Connection=yes;')
c = conn.cursor()

areaHints = []
itemHints = []
locHints = []

# Extract location metadata from source code
for k,v in location_table.items():
    mq = 0
    shop = 0
    scrub = 0
    cow = 0
    hintName = None
    if 'MQ' in k:
        mq = 1
    if 'Shop' in k or 'Bazaar' in k:
        shop = 1
    if 'Scrub' in k and (v[0] == 'NPC' or v[0] == 'GrottoNPC') and k != 'HF Deku Scrub Grotto' and k != 'LW Deku Scrub Near Bridge' and k != 'LW Deku Scrub Grotto Front':
        scrub = 1
    if 'Cow' in k:
        cow = 1
    if k in hintTable and mq == 0:
        if hintTable[k][1] is None:
            if type(hintTable[k][0]) is list:
                hintName = hintTable[k][0][0]
            else:
                hintName = hintTable[k][0]
        else:
            hintName = hintTable[k][1]
        if not (hintName in locHints):
            locHints.append({'loc': k, 'hintLoc': hintName})
    if not (v[4] is None):
        if not (v[4][0] in areaHints):
            areaHints.append('#'+v[4][0]+'#')

for k,v in hintTable.items():
    if type(v[2]) is str:
        if v[2] == 'item':
            if not (v[2] in itemHints):
                itemHints.append({'item': k, 'hintItem': v[1]})

# overwrite/create files and write column headers
# woth    - Way of the Hero locations with required items
# foolish - Locations with no required items by logic
# items   - Item locations
# spheres - Logic sphere in which a location/item is obtainable
c.execute("DROP TABLE IF EXISTS dbo.hints")
c.execute('CREATE TABLE dbo.hints (seed NVARCHAR(16), gloc NVARCHAR(38), htype NVARCHAR(4), loc NVARCHAR(53), item NVARCHAR(36))')
conn.commit()

# process spoiler logs
fcount = 0
for filename in os.listdir(spoilers):
    if filename.endswith(".json"):
        fcount = fcount + 1
        sys.stdout.write("\r%d" % fcount)
        afile = filename.split("_")
        seed = afile[2]

        with open(spoilers + filename,'r') as inf:
            sp = json.load(inf)
            for l, h in sp['gossip_stones'].items():
                hint = h['text']
                if 'way of the hero' in hint:
                    htype = 'woth'
                    loc = None
                    for t in areaHints:
                        if t in hint:
                            loc = t[1:len(t)-1]
                    item = None
                elif 'foolish choice' in hint:
                    htype = 'fool'
                    loc = None
                    for t in areaHints:
                        if t in hint:
                            loc = t[1:len(t)-1]
                    item = None
                else:
                    htype = 'item'
                    loc = None
                    for t in locHints:
                        if t['hintLoc'] in hint:
                            loc = t['loc']
                    item = None
                    for t in itemHints:
                        if t['hintItem'] in hint:
                            item = t['item']
                c.execute('INSERT INTO hints VALUES(?, ?, ?, ?, ?)',(seed, l, htype, loc, item))
            
conn.commit()
conn.close()