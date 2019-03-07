SELECT 
count(*) as count,
p.type
from 
tb_personnel_guard as p
LEFT JOIN
tb_personnel_guard_area as a
on
p.id=a.guard_id
LEFT JOIN
db_unitpropertybase.t_pb_unit as u
on
a.estate_code = u.id
WHERE
a.town_code=440306
GROUP BY
p.type