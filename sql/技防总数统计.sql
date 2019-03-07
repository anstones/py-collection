SELECT 
sum(t.amount) as count,
t.type_name
from 
tb_technical_guard as t
LEFT JOIN
db_unitpropertybase.t_pb_unit as u
on
t.estate_code = u.id
WHERE
t.province_code=440000
GROUP BY
t.type_name