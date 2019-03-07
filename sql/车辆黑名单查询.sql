SELECT 
	b.id as row_id,
	plate_no,
	car_brand,
	car_corlor,
	owner_name,
	telephone,
	CONCAT(p.name,c.city_name) as belong_place,
	certificate_type,
	certificate_no,
	type,
	case_code,
	image_id
from 
	tb_car_blacklist as b
left join
	db_unitpropertybase.t_pb_address_province as p
on 
	b.belong_province_code = p.code
left join
	db_unitpropertybase.t_pb_address_city as c
on 
  b.belong_city_code = c.city_code
where 
	b.id =1

