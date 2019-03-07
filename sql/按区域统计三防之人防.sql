SELECT 
count(*) as count_p,
u.city_name
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
a.province_code = 440000
GROUP BY
a.city_code