import sys
import json
import os
import psycopg2
import pgcred

# Spoiler log location
spoilers = './spoilers/'

conn = psycopg2.connect(host=pgcred.hostname, user=pgcred.username, password=pgcred.password, database=pgcred.pgdatabase)

c = conn.cursor()

# overwrite/create files and write column headers
# woth    - Way of the Hero locations with required items
# foolish - Locations with no required items by logic
# items   - Item locations
# spheres - Logic sphere in which a location/item is obtainable
c.execute("DROP TABLE IF EXISTS woth")
c.execute("DROP TABLE IF EXISTS fool")
c.execute("DROP TABLE IF EXISTS items")
c.execute("DROP TABLE IF EXISTS spheres")
c.execute("DROP TABLE IF EXISTS ispheres")
c.execute('CREATE TABLE woth (seed VARCHAR(16), loc VARCHAR(59), item VARCHAR(36))')
c.execute('CREATE TABLE fool (seed VARCHAR(16), area VARCHAR(23))')
c.execute('CREATE TABLE items (seed VARCHAR(16), loc VARCHAR(59), item VARCHAR(36))')
c.execute('CREATE TABLE spheres (seed VARCHAR(16), loc VARCHAR(59), item VARCHAR(36), sphere INT)')
c.execute('CREATE TABLE ispheres (seed VARCHAR(16), loc VARCHAR(59), item VARCHAR(36), sphere INT)')
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
                c.execute('INSERT INTO woth VALUES(%s, %s, %s)', row)
            
            for l in sp[':barren_regions']:
                row = (seed, l)
                c.execute('INSERT INTO fool VALUES(%s, %s)', row)

            for l, i in sp['locations'].items():
                if type(i) is dict:
                    item = i['item']
                else:
                    item = i
                if 'Bottle with' in item:
                    if 'Letter' not in item and 'Big Poe' not in item:
                        item = 'Bottle'
                row = (seed, l, item)
                c.execute('INSERT INTO items VALUES(%s, %s, %s)', row)
            
            proghook = 1
            progstr = 1
            progscale = 1
            isphere = 0

            for sphere in sp[':playthrough']:
                itemInSphere = False
                for l, i in sp[':playthrough'][sphere].items():
                    if type(i) is dict:
                        item = i['item']
                    else:
                        item = i
                    if 'Bottle with' in item:
                        if 'Letter' not in item and 'Big Poe' not in item:
                            item = 'Bottle'
                    row = (seed, l, item, int(sphere))
                    c.execute('INSERT INTO spheres VALUES(%s, %s, %s, %s)', row)
                    if item == 'Progressive Hookshot':
                        if proghook == 1:
                            item = 'Hookshot'
                        else:
                            item = 'Longshot'
                        proghook = proghook + 1
                    if item == 'Progressive Strength Upgrade':
                        item = 'Strength ' + str(progstr)
                        progstr = progstr + 1
                    if item == 'Progressive Scale':
                        if progscale == 1:
                            item = 'Zora Scale'
                        else:
                            item = 'Gold Scale'
                        progscale = progscale + 1
                    if (not ('Small Key' in item or 'Boss Key' in item or 'Buy ' in item or 'Deliver ' in item or 'Emerald' in item or 'Ruby' in item or 'Sapphire' in item or 'Medallion' in item or 'Bug' in item)) and item != 'Fish' and item != '':
                        row = (seed, l, item, int(isphere))
                        c.execute('INSERT INTO ispheres VALUES(%s, %s, %s, %s)', row)
                        itemInSphere = True
                if itemInSphere:
                    isphere = isphere + 1

conn.commit()
conn.close()