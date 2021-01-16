SELECT * FROM [fool]
LEFT JOIN (SELECT CAST(RIGHT([seed],LEN([seed])-CHARINDEX('-',[seed])) AS int) AS seed_num, [seed], COUNT([seed]) AS foolish_dungeon
FROM [fool]
WHERE
NOT ([area] = 'Deku Tree' OR
[area] = 'Dodongo''s Cavern' OR
[area] = 'Jabu Jabu''s Belly' OR
[area] = 'Forest Temple' OR
[area] = 'Fire Temple' OR
[area] = 'Water Temple' OR
[area] = 'Shadow Temple' OR
[area] = 'Spirit Temple' OR
[area] = 'Bottom of the Well' OR
[area] = 'Ice Cavern' OR
[area] = 'Gerudo Training Grounds' OR
[area] = 'Ganon''s Castle')
GROUP BY [seed]) as owfool ON owfool.seed = fool.seed
WHERE owfool.seed IS NULL