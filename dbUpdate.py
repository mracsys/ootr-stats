import sys
import json
# OoTR source code location
sys.path.insert(0, '../OoTR-5.1')
import os
import pyodbc
from LocationList import location_table
from HintList import hintTable

conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=MAGELLAN\SQLEXPRESS;'
                      'Database=OotrStatsS3;'
                      'Trusted_Connection=yes;')
c = conn.cursor()

c.execute("DROP TABLE IF EXISTS locations")
c.execute("DROP TABLE IF EXISTS itemhints")
c.execute("DROP TABLE IF EXISTS dkeys")
c.execute("DROP TABLE IF EXISTS bosses")
c.execute("DROP TABLE IF EXISTS unique_items")
c.execute('DROP VIEW IF EXISTS ad_seeds')
c.execute('DROP VIEW IF EXISTS checks_per_area')
c.execute('DROP VIEW IF EXISTS non_hinted_loc')
c.execute('DROP VIEW IF EXISTS prog_areas')
c.execute('DROP VIEW IF EXISTS total_spheres')
c.execute('DROP VIEW IF EXISTS woth_area')
c.execute('DROP VIEW IF EXISTS woth_item_area')
c.execute('DROP VIEW IF EXISTS woth_loc')
c.execute('DROP VIEW IF EXISTS fool_area')
c.execute('DROP VIEW IF EXISTS str_reqs')
c.execute('DROP VIEW IF EXISTS hook_reqs')
c.execute('CREATE TABLE locations (loc NVARCHAR(57), ztype NVARCHAR(11), area NVARCHAR(23), hintname NVARCHAR(66), mq BIT, shop BIT, scrub BIT, cow BIT, always BIT, sometimes BIT)')
c.execute('CREATE TABLE itemhints (item NVARCHAR(36), hintname NVARCHAR(66))')
c.execute('CREATE TABLE dkeys (area NVARCHAR(23), nkeys INTEGER)')
c.execute('CREATE TABLE bosses (loc NVARCHAR(57), dungeon NVARCHAR(17))')
c.execute('CREATE TABLE unique_items (item NVARCHAR(36), itype NVARCHAR(16))')
conn.commit()
c.execute("CREATE VIEW ad_seeds AS SELECT seed AS adseed FROM spheres WHERE (loc = 'Song from Ocarina of Time')")
c.execute("CREATE VIEW checks_per_area AS SELECT locations.area, COUNT(locations.loc) - COALESCE (MAX(dkeys.nkeys), 0) AS checks FROM locations LEFT OUTER JOIN dkeys ON locations.area = dkeys.area WHERE (locations.ztype = 'Chest') OR (locations.ztype = 'Cutscene') OR (locations.ztype = 'BossHeart') OR (locations.ztype = 'Collectable') OR (locations.ztype = 'NPC') OR (locations.ztype = 'GrottoNPC') GROUP BY locations.area")
c.execute("CREATE VIEW prog_areas AS SELECT spheres.seed, bosses.dungeon FROM spheres LEFT OUTER JOIN bosses ON bosses.loc = spheres.loc LEFT OUTER JOIN ad_seeds ON ad_seeds.adseed = spheres.seed WHERE (NOT (bosses.dungeon IS NULL)) AND (spheres.item LIKE '%Medallion') OR (NOT (bosses.dungeon IS NULL)) AND (spheres.item = 'Kokiri Emerald' OR spheres.item = 'Goron Ruby' OR spheres.item = 'Zora Sapphire') AND (NOT (ad_seeds.adseed IS NULL))")
c.execute("CREATE VIEW total_spheres AS SELECT seed, MAX(sphere) AS max_sphere FROM spheres GROUP BY seed")
c.execute("CREATE VIEW non_hinted_loc AS SELECT DISTINCT spheres.seed, spheres.loc, locations.area, spheres.item, spheres.sphere, spheres.sphere * 100.0 / total_spheres.max_sphere AS norm_sphere, hints.htype FROM spheres LEFT OUTER JOIN locations ON locations.loc = spheres.loc LEFT OUTER JOIN hints ON spheres.seed = hints.seed AND (locations.loc = hints.loc OR locations.area = hints.loc) LEFT OUTER JOIN prog_areas ON prog_areas.dungeon = locations.area AND prog_areas.seed = spheres.seed LEFT OUTER JOIN total_spheres ON total_spheres.seed = spheres.seed WHERE (hints.htype IS NULL OR hints.htype <> 'woth' AND hints.htype <> 'item') AND (NOT (locations.area IS NULL)) AND (spheres.item <> 'Gold Skulltula Token') AND (spheres.item <> 'Magic Bean') AND (spheres.item <> 'Ocarina') AND (spheres.item <> 'Gold Skulltula Token') AND (spheres.item <> 'Gerudo Membership Card') AND (spheres.item <> 'Zeldas Letter') AND (spheres.item <> 'Light Arrows') AND (spheres.item <> 'Goron Tunic') AND (spheres.item <> 'Zora Tunic') AND (NOT (spheres.item LIKE '% Key %')) AND (NOT (spheres.item LIKE '%Buy %')) AND (spheres.sphere > 2) AND (prog_areas.dungeon IS NULL) AND (locations.ztype <> 'Song') AND (dbo.spheres.loc <> 'Ganon') AND (dbo.spheres.loc <> 'King Zora Moves') AND (dbo.spheres.loc <> 'Epona') AND (dbo.spheres.loc <> 'Gerudo Fortress Carpenter Rescue')")
c.execute("CREATE VIEW woth_area AS SELECT area, COUNT(area) * 100.0 / 100000 AS pct FROM (SELECT DISTINCT woth.seed, locations.area FROM woth LEFT OUTER JOIN locations ON woth.loc = locations.loc) AS derivedtbl_1 GROUP BY area")
c.execute("CREATE VIEW woth_item_area AS SELECT area, COUNT(area) * 100.0 / 100000 AS pct FROM (SELECT DISTINCT woth.seed, locations.area FROM woth LEFT OUTER JOIN locations ON woth.loc = locations.loc WHERE (NOT (locations.ztype = 'Song'))) AS derivedtbl_1 GROUP BY area")
c.execute("CREATE VIEW woth_loc AS SELECT loc, COUNT(loc) * 100.0 / 100000 AS pct FROM woth GROUP BY loc")
c.execute("CREATE VIEW fool_area AS SELECT area, COUNT(area) * 100.0 / 100000 AS pct FROM fool GROUP BY area")
c.execute("CREATE VIEW str_reqs AS SELECT [str_req], COUNT([str_req]) * 100.0 / 100000.0 AS pct FROM (SELECT [seed], COUNT([seed]) AS str_req FROM [dbo].[spheres] WHERE [item] = 'Progressive Strength Upgrade' GROUP BY [seed]) AS derivedtbl_1 GROUP BY [str_req]")
c.execute("CREATE VIEW hook_reqs AS SELECT [hook_req], COUNT([hook_req]) * 100.0 / 100000.0 AS pct FROM (SELECT [seed], COUNT([seed]) AS hook_req FROM [dbo].[spheres] WHERE [item] = 'Progressive Hookshot' GROUP BY [seed]) AS derivedtbl_1 GROUP BY [hook_req]")

# Extract location metadata from source code
for k,v in location_table.items():
    mq = 0
    shop = 0
    scrub = 0
    cow = 0
    always = 0
    sometimes = 0
    hintName = None
    if 'MQ' in k:
        mq = 1
    if 'Shop' in k or 'Bazaar' in k:
        shop = 1
    if 'Scrub' in k and (v[0] == 'NPC' or v[0] == 'GrottoNPC') and k != 'HF Grotto Deku Scrub Piece of Heart' and k != 'LW Grotto Deku Scrub Deku Nut Upgrade' and k != 'LW Deku Scrub Deku Stick Upgrade':
        scrub = 1
    if 'Cow' in k:
        cow = 1
    if k in hintTable:
        if hintTable[k][1] is None:
            if type(hintTable[k][0]) is list:
                hintName = hintTable[k][0][0]
            else:
                hintName = hintTable[k][0]
        else:
            hintName = hintTable[k][1]
        if type(hintTable[k][2]) is list:
            if hintTable[k][2][1] == 'always':
                always = 1
            if hintTable[k][2][1] == 'sometimes':
                sometimes = 1
        else:
            if hintTable[k][2] == 'always':
                always = 1
            if hintTable[k][2] == 'sometimes':
                sometimes = 1
    if v[4] is None:
        c.execute("INSERT INTO locations VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (k, v[0], v[4], hintName, mq, shop, scrub, cow, always, sometimes))
    else:
        c.execute("INSERT INTO locations VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (k, v[0], v[4][0], hintName, mq, shop, scrub, cow, always, sometimes))

for k,v in hintTable.items():
    if type(v[2]) is str:
        if v[2] == 'item':
            c.execute("INSERT INTO itemhints VALUES(?, ?)", (k, v[1]))

# dungeon checks that are small keys or the boss key
c.execute("INSERT INTO dkeys VALUES('Bottom of the Well', 3)")
c.execute("INSERT INTO dkeys VALUES('Ganons Castle', 3)")
c.execute("INSERT INTO dkeys VALUES('Gerudo Training Grounds', 9)")
c.execute("INSERT INTO dkeys VALUES('Gerudo Fortress', 4)")
c.execute("INSERT INTO dkeys VALUES('Forest Temple', 6)")
c.execute("INSERT INTO dkeys VALUES('Fire Temple', 8)")
c.execute("INSERT INTO dkeys VALUES('Water Temple', 7)")
c.execute("INSERT INTO dkeys VALUES('Shadow Temple', 6)")
c.execute("INSERT INTO dkeys VALUES('Spirit Temple', 6)")

c.execute("INSERT INTO bosses VALUES('Queen Gohma','Deku Tree')")
c.execute("INSERT INTO bosses VALUES('King Dodongo','Dodongo''s Cavern')")
c.execute("INSERT INTO bosses VALUES('Barinade','Jabu Jabu''s Belly')")
c.execute("INSERT INTO bosses VALUES('Phantom Ganon','Forest Temple')")
c.execute("INSERT INTO bosses VALUES('Volvagia','Fire Temple')")
c.execute("INSERT INTO bosses VALUES('Morpha','Water Temple')")
c.execute("INSERT INTO bosses VALUES('Bongo Bongo','Shadow Temple')")
c.execute("INSERT INTO bosses VALUES('Twinrova','Spirit Temple')")

c.execute("INSERT INTO [unique_items] VALUES('Zora Sapphire','Dungeon')")
c.execute("INSERT INTO [unique_items] VALUES('Shadow Medallion','Dungeon')")
c.execute("INSERT INTO [unique_items] VALUES('Kokiri Emerald','Dungeon')")
c.execute("INSERT INTO [unique_items] VALUES('Spirit Medallion','Dungeon')")
c.execute("INSERT INTO [unique_items] VALUES('Water Medallion','Dungeon')")
c.execute("INSERT INTO [unique_items] VALUES('Fire Medallion','Dungeon')")
c.execute("INSERT INTO [unique_items] VALUES('Goron Ruby','Dungeon')")
c.execute("INSERT INTO [unique_items] VALUES('Light Medallion','Dungeon')")
c.execute("INSERT INTO [unique_items] VALUES('Forest Medallion','Dungeon')")
c.execute("INSERT INTO [unique_items] VALUES('Arrows (10)','Junk')")
c.execute("INSERT INTO [unique_items] VALUES('Bombs (5)','Junk')")
c.execute("INSERT INTO [unique_items] VALUES('Piece of Heart','Junk')")
c.execute("INSERT INTO [unique_items] VALUES('Rupees (50)','Junk')")
c.execute("INSERT INTO [unique_items] VALUES('Rupees (5)','Junk')")
c.execute("INSERT INTO [unique_items] VALUES('Heart Container','Junk')")
c.execute("INSERT INTO [unique_items] VALUES('Ice Trap','Junk')")
c.execute("INSERT INTO [unique_items] VALUES('Piece of Heart (Treasure Chest Game)','Junk')")
c.execute("INSERT INTO [unique_items] VALUES('Bombs (10)','Junk')")
c.execute("INSERT INTO [unique_items] VALUES('Deku Shield','Junk')")
c.execute("INSERT INTO [unique_items] VALUES('Nayrus Love','Junk')")
c.execute("INSERT INTO [unique_items] VALUES('Rupees (200)','Junk')")
c.execute("INSERT INTO [unique_items] VALUES('Recovery Heart','Junk')")
c.execute("INSERT INTO [unique_items] VALUES('Deku Seeds (30)','Junk')")
c.execute("INSERT INTO [unique_items] VALUES('Double Defense','Junk')")
c.execute("INSERT INTO [unique_items] VALUES('Deku Nuts (10)','Junk')")
c.execute("INSERT INTO [unique_items] VALUES('Bombs (20)','Junk')")
c.execute("INSERT INTO [unique_items] VALUES('Arrows (5)','Junk')")
c.execute("INSERT INTO [unique_items] VALUES('Hylian Shield','Junk')")
c.execute("INSERT INTO [unique_items] VALUES('Rupees (20)','Junk')")
c.execute("INSERT INTO [unique_items] VALUES('Deku Stick (1)','Junk')")
c.execute("INSERT INTO [unique_items] VALUES('Biggoron Sword','Junk')")
c.execute("INSERT INTO [unique_items] VALUES('Deku Stick Capacity','Junk')")
c.execute("INSERT INTO [unique_items] VALUES('Arrows (30)','Junk')")
c.execute("INSERT INTO [unique_items] VALUES('Stone of Agony','Junk')")
c.execute("INSERT INTO [unique_items] VALUES('Deku Nut Capacity','Junk')")
c.execute("INSERT INTO [unique_items] VALUES('Deku Nuts (5)','Junk')")
c.execute("INSERT INTO [unique_items] VALUES('Ice Arrows','Junk')")
c.execute("INSERT INTO [unique_items] VALUES('Kokiri Sword','Junk')")
c.execute("INSERT INTO [unique_items] VALUES('Small Key (Ganons Castle)','Key')")
c.execute("INSERT INTO [unique_items] VALUES('Small Key (Forest Temple)','Key')")
c.execute("INSERT INTO [unique_items] VALUES('Boss Key (Forest Temple)','Key')")
c.execute("INSERT INTO [unique_items] VALUES('Small Key (Bottom of the Well)','Key')")
c.execute("INSERT INTO [unique_items] VALUES('Small Key (Fire Temple)','Key')")
c.execute("INSERT INTO [unique_items] VALUES('Boss Key (Fire Temple)','Key')")
c.execute("INSERT INTO [unique_items] VALUES('Boss Key (Water Temple)','Key')")
c.execute("INSERT INTO [unique_items] VALUES('Small Key (Water Temple)','Key')")
c.execute("INSERT INTO [unique_items] VALUES('Small Key (Shadow Temple)','Key')")
c.execute("INSERT INTO [unique_items] VALUES('Boss Key (Shadow Temple)','Key')")
c.execute("INSERT INTO [unique_items] VALUES('Small Key (Gerudo Training Grounds)','Key')")
c.execute("INSERT INTO [unique_items] VALUES('Small Key (Spirit Temple)','Key')")
c.execute("INSERT INTO [unique_items] VALUES('Boss Key (Spirit Temple)','Key')")
c.execute("INSERT INTO [unique_items] VALUES('Boss Key (Ganons Castle)','Key')")
c.execute("INSERT INTO [unique_items] VALUES('Bombchus (20)','Optional')")
c.execute("INSERT INTO [unique_items] VALUES('Goron Tunic','Optional')")
c.execute("INSERT INTO [unique_items] VALUES('Farores Wind','Optional')")
c.execute("INSERT INTO [unique_items] VALUES('Bombchus (10)','Optional')")
c.execute("INSERT INTO [unique_items] VALUES('Zora Tunic','Optional')")
c.execute("INSERT INTO [unique_items] VALUES('Bombchus (5)','Optional')")
c.execute("INSERT INTO [unique_items] VALUES('Magic Meter','Required')")
c.execute("INSERT INTO [unique_items] VALUES('Bottle with Letter','Required')")
c.execute("INSERT INTO [unique_items] VALUES('Bomb Bag','Required')")
c.execute("INSERT INTO [unique_items] VALUES('Claim Check','Required')")
c.execute("INSERT INTO [unique_items] VALUES('Slingshot','Required')")
c.execute("INSERT INTO [unique_items] VALUES('Boomerang','Required')")
c.execute("INSERT INTO [unique_items] VALUES('Lens of Truth','Required')")
c.execute("INSERT INTO [unique_items] VALUES('Mirror Shield','Required')")
c.execute("INSERT INTO [unique_items] VALUES('Iron Boots','Required')")
c.execute("INSERT INTO [unique_items] VALUES('Bottle','Required')")
c.execute("INSERT INTO [unique_items] VALUES('Bow','Required')")
c.execute("INSERT INTO [unique_items] VALUES('Progressive Hookshot','Required')")
c.execute("INSERT INTO [unique_items] VALUES('Fire Arrows','Required')")
c.execute("INSERT INTO [unique_items] VALUES('Progressive Scale','Required')")
c.execute("INSERT INTO [unique_items] VALUES('Dins Fire','Required')")
c.execute("INSERT INTO [unique_items] VALUES('Progressive Strength Upgrade','Required')")
c.execute("INSERT INTO [unique_items] VALUES('Progressive Wallet','Required')")
c.execute("INSERT INTO [unique_items] VALUES('Light Arrows','Required')")
c.execute("INSERT INTO [unique_items] VALUES('Hammer','Required')")
c.execute("INSERT INTO [unique_items] VALUES('Hover Boots','Required')")
c.execute("INSERT INTO [unique_items] VALUES('Prescription','Required')")
c.execute("INSERT INTO [unique_items] VALUES('Bottle with Big Poe','Required')")
c.execute("INSERT INTO [unique_items] VALUES('Eyedrops','Required')")
c.execute("INSERT INTO [unique_items] VALUES('Eyeball Frog','Required')")
c.execute("INSERT INTO [unique_items] VALUES('Eponas Song','Song')")
c.execute("INSERT INTO [unique_items] VALUES('Suns Song','Song')")
c.execute("INSERT INTO [unique_items] VALUES('Requiem of Spirit','Song')")
c.execute("INSERT INTO [unique_items] VALUES('Song of Time','Song')")
c.execute("INSERT INTO [unique_items] VALUES('Serenade of Water','Song')")
c.execute("INSERT INTO [unique_items] VALUES('Sarias Song','Song')")
c.execute("INSERT INTO [unique_items] VALUES('Minuet of Forest','Song')")
c.execute("INSERT INTO [unique_items] VALUES('Nocturne of Shadow','Song')")
c.execute("INSERT INTO [unique_items] VALUES('Zeldas Lullaby','Song')")
c.execute("INSERT INTO [unique_items] VALUES('Prelude of Light','Song')")
c.execute("INSERT INTO [unique_items] VALUES('Bolero of Fire','Song')")
c.execute("INSERT INTO [unique_items] VALUES('Song of Storms','Song')")
c.execute("INSERT INTO [unique_items] VALUES('Rupee (1)','Valid')")

conn.commit()
conn.close()