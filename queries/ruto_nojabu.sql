SELECT spheres.loc, COUNT(spheres.loc) * 100.0 / 100000
FROM spheres LEFT JOIN (SELECT spheres.seed, spheres.sphere
  FROM [woth] LEFT JOIN spheres ON (spheres.seed = woth.seed AND spheres.item = woth.item)
  LEFT JOIN locations on spheres.loc = locations.loc
  WHERE woth.[item] = 'Bottle with Letter' AND locations.always = 0 AND locations.sometimes = 0) AS lseed ON (lseed.seed = spheres.seed AND lseed.sphere < spheres.sphere)
  LEFT JOIN (SELECT loc, area
FROM locations
WHERE (area = 'Ice Cavern' OR area = 'Zora''s Fountain' OR area = 'Jabu Jabu''s Belly' OR loc = 'Barinade')
AND mq = 0 AND shop = 0 AND scrub = 0 AND cow = 0) AS rlocs ON (rlocs.loc = spheres.loc)
LEFT JOIN (SELECT seed FROM spheres WHERE loc = 'Barinade' AND (item LIKE '%Medallion')) AS medjabu ON medjabu.seed = spheres.seed
LEFT JOIN (SELECT seed FROM spheres WHERE loc = 'Barinade' AND (NOT item LIKE '%Medallion')) AS stnjabu ON stnjabu.seed = spheres.seed
  WHERE (NOT (lseed.seed IS NULL)) AND (NOT (rlocs.loc IS NULL) AND (medjabu.seed IS NULL) AND stnjabu.seed IS NULL)
  GROUP BY spheres.loc