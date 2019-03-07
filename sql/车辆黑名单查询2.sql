SELECT 
	e.id as row_id,
	e.create_time,
	e.event_type,
	e.alarm_degree,
	event_image_id,
	u.name as location,
	e.video_url,
	e.event_describe,
	e.pending_status,
	e.pending_operator,
	e.pending_time,
	u.lng as longitude,
	u.lat as latitude
from 
	tb_alarm_event as e,
	tb_car_blacklist as b,
	db_unitpropertybase.t_pb_unit as u
where 
	e.id=b.id
and
	e.estate_code = u.id
and
	b.id =1



-- left join
-- 	db_unitpropertybase.t_pb_address_province as p
-- on 
-- 	b.belong_province_code = p.code
-- left join
-- 	db_unitpropertybase.t_pb_address_city as c
-- on 
--   b.belong_city_code = c.city_code
-- 
-- LEFT JOIN 
-- 	tb_alarm_event as e on e.id = b.id