(SELECT seed,dungeon AS area FROM spheres
LEFT JOIN bosses ON bosses.loc = spheres.loc
WHERE spheres.item LIKE '%Medallion' AND spheres.loc != 'Links Pocket'
UNION
SELECT seed,loc AS area FROM hints
WHERE htype='woth')