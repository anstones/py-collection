SELECT 
      `plate` as plate_no,
      `car_brand` as brand, 
      `car_series` as series,
      `car_color` as color,
      `user_name` as owner_name,
      `telephone` as owner_telephone,
      `id_card_number` as owner_certificate_no,
      `room_no`as room_code,
			`area_code` as estate_code,
FROM t_parkinfo AS i
LEFT JOIN t_plateusers AS p on p.park_no = i.park_no
where (%(province_code)s='' OR i.province_code = %(province_code)s)
AND (%(city_code)s='' OR i.city_code = %(city_code)s)
AND (%(town_code)s='' OR i.town_code = %(town_code)s)
AND (%(estate_code)s='' OR i.area_code = %(estate_code)s)