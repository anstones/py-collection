
SELECT 
*
from
(SELECT sum(t.amount) as count_t,u.city_name as name_t from tb_technical_guard as t LEFT JOIN db_unitpropertybase.t_pb_unit as u on t.estate_code = u.id where t.province_code=440000 GROUP BY t.city_code ) as a,
(SELECT sum(o.amount) as count_o,u.city_name as name_o from tb_objective_guard as o LEFT JOIN db_unitpropertybase.t_pb_unit as u on o.estate_code = u.id where o.province_code=440000 GROUP BY o.city_code) as b,
(SELECT count(*)      as count_p,u.city_name as name_p from tb_personnel_guard as p LEFT JOIN tb_personnel_guard_area as pa on p.id=pa.guard_id LEFT JOIN db_unitpropertybase.t_pb_unit as u on pa.estate_code = u.id WHERE pa.province_code = 440000 GROUP BY pa.city_code)as c 
WHERE
	a.name_t = b.name_o
AND
	b.name_o = c.name_p

