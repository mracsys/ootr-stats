SELECT *
  FROM ispheres as csphere
  LEFT JOIN ispheres as fsphere ON (csphere.seed = fsphere.seed AND csphere.item = 'Gerudo Membership Card' AND 
  (fsphere.loc = 'Gerudo Fortress Rooftop Chest' OR
  fsphere.loc = 'Gerudo Fortress Membership Card' OR
  fsphere.loc = 'Horseback Archery 1000 Points' OR
  fsphere.loc = 'Horseback Archery 1500 Points'))
  WHERE NOT fsphere.seed IS NULL AND fsphere.sphere < csphere.sphere
  ORDER BY csphere.seed ASC