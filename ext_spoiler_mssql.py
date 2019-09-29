import sys
import json
import os
import pyodbc

# Spoiler log location
spoilers = './spoilers/'

conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=MAGELLAN\SQLEXPRESS;'
                      'Database=OotrStatsDF;'
                      'Trusted_Connection=yes;')
c = conn.cursor()

# overwrite/create files and write column headers
# woth    - Way of the Hero locations with required items
# foolish - Locations with no required items by logic
# items   - Item locations
# spheres - Logic sphere in which a location/item is obtainable
c.execute("DROP TABLE IF EXISTS dbo.woth")
c.execute("DROP TABLE IF EXISTS dbo.fool")
c.execute("DROP TABLE IF EXISTS dbo.items")
c.execute("DROP TABLE IF EXISTS dbo.spheres")
c.execute('CREATE TABLE dbo.woth (seed NVARCHAR(16), loc NVARCHAR(53), item NVARCHAR(36))')
c.execute('CREATE TABLE dbo.fool (seed NVARCHAR(16), area NVARCHAR(23))')
c.execute('CREATE TABLE dbo.items (seed NVARCHAR(16), loc NVARCHAR(53), item NVARCHAR(36))')
c.execute('CREATE TABLE dbo.spheres (seed NVARCHAR(16), loc NVARCHAR(53), item NVARCHAR(36), sphere INT)')
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
            for l, i in sp[':woth_locations'].items():
                if type(i) is dict:
                    item = i['item']
                else:
                    item = i
                if 'Bottle with' in item:
                    if 'Letter' not in item and 'Big Poe' not in item:
                        item = 'Bottle'
                row = (seed, l, item)
                c.execute('INSERT INTO woth VALUES(?, ?, ?)',row)
            
            for l in sp[':barren_regions']:
                row = (seed, l)
                c.execute('INSERT INTO fool VALUES(?, ?)',row)

            for l, i in sp['locations'].items():
                if type(i) is dict:
                    item = i['item']
                else:
                    item = i
                if 'Bottle with' in item:
                    if 'Letter' not in item and 'Big Poe' not in item:
                        item = 'Bottle'
                row = (seed, l, item)
                c.execute('INSERT INTO items VALUES(?, ?, ?)',row)
                
            for sphere in sp[':playthrough']:
                for l, i in sp[':playthrough'][sphere].items():
                    if type(i) is dict:
                        item = i['item']
                    else:
                        item = i
                    if 'Bottle with' in item:
                        if 'Letter' not in item and 'Big Poe' not in item:
                            item = 'Bottle'
                    row = (seed, l, item, int(sphere))
                    c.execute('INSERT INTO spheres VALUES(?, ?, ?, ?)',row)

conn.commit()
conn.close()