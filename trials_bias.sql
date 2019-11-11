SELECT [loc], COUNT([loc]) * 100.0 / 10000.0 AS pct
FROM [spheres]
WHERE [loc] = 'Forest Trial Clear from Ganons Castle Forest Trial' OR
[loc] = 'Fire Trial Clear from Ganons Castle Fire Trial' OR
[loc] = 'Water Trial Clear from Ganons Castle Water Trial' OR
[loc] = 'Shadow Trial Clear from Ganons Castle Shadow Trial' OR
[loc] = 'Spirit Trial Clear from Ganons Castle Spirit Trial' OR
[loc] = 'Light Trial Clear from Ganons Castle Light Trial'
GROUP BY [loc]