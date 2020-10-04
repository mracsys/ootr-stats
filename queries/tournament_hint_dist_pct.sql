SELECT ispheres.seed, ispheres.item, (CASE WHEN ispheres.sphere = 0 THEN 'Yes' WHEN obvious_areas.area IS NULL THEN 'No' ELSE 'Yes' END) AS obvious
FROM ispheres
LEFT JOIN locations ON ispheres.loc = locations.loc
LEFT JOIN obvious_areas ON (obvious_areas.area = locations.area AND obvious_areas.seed = ispheres.seed)
WHERE ispheres.item != 'Gold Skulltula Token'
AND ispheres.item != 'Time Travel'
AND ispheres.item != 'Triforce'
AND ispheres.item != 'Scarecrow Song'
AND ispheres.item != 'Skull Mask'
AND ispheres.item != 'Blue Fire'
AND ispheres.item != 'Big Poe'
AND ispheres.item != 'Sell Big Poe'
AND ispheres.item != 'Water Temple Clear'