SELECT 
			p.plate AS plate_no,
			p.car_brand AS brand,
			p.car_series AS series,
			p.car_color AS color,
			p.user_name AS owner_name,
			p.telephone AS owner_telephone,
			p.id_card_number AS owner_certificate_no,
			p.room_no AS room_code,
			u.province_name,
			u.city_name,
			u.name AS estate_name,
			i.park_name,
			i.park_no,
			i.area_code AS estate_code,
			h.type AS resident_type
FROM t_parkinfo AS i
LEFT JOIN t_plateusers AS p on p.park_no = i.park_no
LEFT JOIN db_unitpropertybase.t_pb_unit AS u on i.area_code = u.id
LEFT JOIN db_unitpropertybase.house_user AS h on p.room_no = h.room
where (%(province_code)s='' OR i.province_code = %(province_code)s)
AND (%(city_code)s='' OR i.city_code = %(city_code)s)
AND (%(town_code)s='' OR i.town_code = %(town_code)s)
AND (%(estate_code)s='' OR i.estate_code = %(estate_code)s)