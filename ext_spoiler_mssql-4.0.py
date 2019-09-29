import sys
# OoTR source code location
sys.path.insert(0, '../OoTR-5.1')
import os
import pyodbc
from LocationList import location_table

# Spoiler log location
spoilers = './freaky/'

conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=MAGELLAN\SQLEXPRESS;'
                      'Database=OotrStatsFreaky;'
                      'Trusted_Connection=yes;')
c = conn.cursor()

# overwrite/create files and write column headers
# woth    - Way of the Hero locations with required items
# foolish - Locations with no required items by logic
# items   - Item locations
# spheres - Logic sphere in which a location/item is obtainable
c.execute("DROP TABLE dbo.woth")
c.execute("DROP TABLE dbo.fool")
c.execute("DROP TABLE dbo.items")
c.execute("DROP TABLE dbo.spheres")
c.execute('CREATE TABLE dbo.woth (seed NVARCHAR(16), loc NVARCHAR(53), item NVARCHAR(36))')
c.execute('CREATE TABLE dbo.fool (seed NVARCHAR(16), area NVARCHAR(23))')
c.execute('CREATE TABLE dbo.items (seed NVARCHAR(16), loc NVARCHAR(53), item NVARCHAR(36))')
c.execute('CREATE TABLE dbo.spheres (seed NVARCHAR(16), loc NVARCHAR(53), item NVARCHAR(36), sphere INT)')
#c.execute('CREATE TABLE locations (loc TEXT, ztype TEXT, area TEXT)')
#c.execute('CREATE TABLE dkeys (area TEXT, nkeys INTEGER)')
conn.commit()
#c.execute('CREATE VIEW "checks-per-area" AS SELECT area, COUNT(loc) FROM locations WHERE ztype="Chest" OR ztype="Cutscene" OR ztype="BossHeart" OR ztype="Collectable" OR ztype="NPC" OR ztype="GrottoNPC" GROUP BY area')
#c.execute('CREATE VIEW "woth-area" AS SELECT area, COUNT(area) FROM (SELECT DISTINCT woth.seed, area FROM woth LEFT JOIN locations on woth.loc = locations.loc) GROUP BY area ORDER BY COUNT(area) DESC')
#c.execute('CREATE VIEW "woth-loc" AS SELECT loc, COUNT(loc)*100.0/3348 FROM woth GROUP BY loc ORDER BY COUNT(loc) DESC')

# Extract location metadata from source code
#for k,v in location_table.items():
#    if 'MQ' not in k:
#        c.execute("INSERT INTO locations VALUES(?, ?, ?)", (k, v[0], v[3]))

#c.execute('INSERT INTO dkeys VALUES("Bottom of the Well", 3)')
#c.execute('INSERT INTO dkeys VALUES("Fire Temple", 9)')
#c.execute('INSERT INTO dkeys VALUES("Forest Temple", 6)')
#c.execute('INSERT INTO dkeys VALUES("Ganons Castle", 3)')
#c.execute('INSERT INTO dkeys VALUES("Gerudo Training Grounds", 9)')
#c.execute('INSERT INTO dkeys VALUES("Gerudo Fortress", 4)')
#c.execute('INSERT INTO dkeys VALUES("Shadow Temple", 6)')
#c.execute('INSERT INTO dkeys VALUES("Spirit Temple", 6)')
#c.execute('INSERT INTO dkeys VALUES("Water Temple", 7)')

# process spoiler logs
for filename in os.listdir(spoilers):
    if filename.endswith(".txt"):
        afile = filename.split("_")
        seed = afile[2]

        with open(spoilers + filename,'r') as inf:
            copy = False
            for x in inf:
                if x.strip() == "Way of the Hero:":
                    copy = True
                elif x.strip() == "Barren of Treasure:":
                    copy = False
                elif copy:
                    if x.strip() != '':
                        line = x.split(":")
                        item = line[1].strip()
                        if '[' in item:
                            isplit = item.split('[')
                            item = isplit[0].strip()
                        if 'Bottle with' in item:
                            if 'Letter' not in item and 'Big Poe' not in item:
                                item = 'Bottle'
                        row = (seed, line[0].strip(), item)
                        c.execute('INSERT INTO woth VALUES(?, ?, ?)',row)

        with open(spoilers + filename,'r') as inf:
            copy = False
            for x in inf:
                if x.strip() == "Barren of Treasure:":
                    copy = True
                elif x.strip() == "Gossip Stone Hints:":
                    copy = False
                elif copy:
                    if x.strip() != '':
                        row = (seed, x.strip())
                        c.execute('INSERT INTO fool VALUES(?, ?)',row)

        with open(spoilers + filename,'r') as inf:
            copy = False
            for x in inf:
                if x.strip() == "Locations:":
                    copy = True
                elif x.strip() == "Playthrough:":
                    copy = False
                elif copy:
                    if x.strip() != '':
                        line = x.split(":")
                        item = line[1].strip()
                        if '[' in item:
                            isplit = item.split('[')
                            item = isplit[0].strip()
                        if 'Bottle with' in item:
                            if 'Letter' not in item and 'Big Poe' not in item:
                                item = 'Bottle'
                        row = (seed, line[0].strip(), item)
                        c.execute('INSERT INTO items VALUES(?, ?, ?)',row)

        with open(spoilers + filename,'r') as inf:
            copy = False
            for x in inf:
                if x.strip() == "Playthrough:":
                    copy = True
                elif x.strip() == "Way of the Hero:":
                    copy = False
                elif copy:
                    y = x.strip()
                    if y.endswith('{'):
                        line = y.split(":")
                        sphere = line[0].strip()
                    elif y != '' and y.endswith('}') == False:
                        line = y.split(":")
                        item = line[1].strip()
                        if '[' in item:
                            isplit = item.split('[')
                            item = isplit[0].strip()
                        if 'Bottle with' in item:
                            if 'Letter' not in item and 'Big Poe' not in item:
                                item = 'Bottle'
                        row = (seed, line[0].strip(), item, int(sphere))
                        c.execute('INSERT INTO spheres VALUES(?, ?, ?, ?)',row)

conn.commit()
conn.close()