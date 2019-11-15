SELECT DISTINCT spheres.seed, spheres.loc AS sometimes_loc, spheres.item AS sometimes_item, hwoth.loc AS woth_area
FROM spheres LEFT JOIN
hints ON (hints.seed = spheres.seed AND hints.loc = spheres.loc) LEFT JOIN
locations ON (locations.loc = hints.loc) LEFT JOIN
hints AS hwoth ON (hwoth.seed = hints.seed AND locations.area = hwoth.loc AND hwoth.htype = 'woth')
WHERE (NOT (hints.seed IS NULL) AND NOT (hwoth.seed IS NULL)) AND hwoth.loc = 'Hyrule Field'
ORDER BY spheres.seed