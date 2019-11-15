SELECT DISTINCT 
                         hints.seed, hints.loc, (CASE WHEN awoth.ztype = 'Song' AND bothcheck.hinttype IS NULL THEN 'Song' WHEN awoth.ztype != 'Song' AND bothcheck.hinttype IS NULL THEN 'Item' WHEN awoth.ztype IS NULL 
                         AND bothcheck.hinttype IS NULL THEN 'None' ELSE 'Both' END) AS hint_type
FROM            hints LEFT OUTER JOIN
                             (SELECT        woth.seed, woth.loc, locations.area, woth.item, locations.ztype
                               FROM            woth LEFT OUTER JOIN
                                                         locations ON woth.loc = locations.loc) AS awoth ON awoth.seed = hints.seed AND awoth.area = hints.loc LEFT OUTER JOIN
                             (SELECT DISTINCT hints_1.seed, hints_1.loc, (CASE WHEN awoth1.ztype = 'Song' THEN 'Song' ELSE 'Item' END) AS hinttype
                               FROM            hints AS hints_1 LEFT OUTER JOIN
                                                             (SELECT        woth_1.seed, woth_1.loc, locations_1.area, woth_1.item, locations_1.ztype
                                                               FROM            woth AS woth_1 LEFT OUTER JOIN
                                                                                         locations AS locations_1 ON woth_1.loc = locations_1.loc) AS awoth1 ON awoth1.seed = hints_1.seed AND awoth1.area = hints_1.loc
                               WHERE        (hints_1.htype = 'woth')) AS bothcheck ON bothcheck.seed = hints.seed AND bothcheck.loc = hints.loc AND bothcheck.hinttype <> (CASE WHEN awoth.ztype = 'Song' THEN 'Song' ELSE 'Item' END)
WHERE        (hints.htype = 'woth') AND (hints.loc = 'Hyrule Field') AND (CASE WHEN awoth.ztype = 'Song' AND bothcheck.hinttype IS NULL THEN 'Song' WHEN awoth.ztype != 'Song' AND bothcheck.hinttype IS NULL THEN 'Item' WHEN awoth.ztype IS NULL 
                         AND bothcheck.hinttype IS NULL THEN 'None' ELSE 'Both' END) = 'Both'
ORDER BY hints.seed