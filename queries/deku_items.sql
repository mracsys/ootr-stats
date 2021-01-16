SELECT DISTINCT items.seed
FROM items
LEFT JOIN locations on items.loc = locations.loc
LEFT JOIN unique_items ON unique_items.item = items.item
WHERE locations.area = 'Deku Tree' AND unique_items.itype = 'Required'
ORDER BY items.seed