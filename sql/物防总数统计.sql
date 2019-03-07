SELECT 
sum(o.amount) as count,
o.type_name
from 
tb_objective_guard as o
LEFT JOIN
db_unitpropertybase.t_pb_unit as u
on
o.estate_code = u.id
WHERE
o.province_code=440000
GROUP BY
o.type_name