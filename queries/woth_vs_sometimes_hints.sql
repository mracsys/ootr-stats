SELECT DISTINCT sometimes_loc, checkcount.checks
FROM (SELECT DISTINCT hints.seed, hints.loc AS sometimes_loc, hints.item AS sometimes_item, hwoth.loc AS woth_area
FROM hints LEFT JOIN
locations ON (locations.loc = hints.loc) LEFT JOIN
hints AS hwoth ON (hwoth.seed = hints.seed AND locations.area = hwoth.loc AND hwoth.htype = 'woth')
WHERE (NOT (hints.seed IS NULL) AND NOT (hwoth.seed IS NULL))) AS dhints
LEFT JOIN (SELECT        dbo.locations.area, COUNT(dbo.locations.loc) - COALESCE (MAX(dbo.dkeys.nkeys), 0) AS checks
FROM            dbo.locations LEFT OUTER JOIN
                         dbo.dkeys ON dbo.locations.area = dbo.dkeys.area
WHERE        ((dbo.locations.ztype = 'Chest') OR
                         (dbo.locations.ztype = 'Cutscene') OR
                         (dbo.locations.ztype = 'BossHeart') OR
                         (dbo.locations.ztype = 'Collectable') OR
                         (dbo.locations.ztype = 'NPC') OR
                         (dbo.locations.ztype = 'GrottoNPC') OR
						 ztype = 'Song') AND
						 mq = 0 AND shop = 0 AND scrub = 0 AND cow = 0
GROUP BY dbo.locations.area) AS checkcount ON checkcount.area = woth_area 
ORDER BY checkcount.checks DESC