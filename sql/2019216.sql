SELECT 
      `p.plate` as plate_no,
      `p.car_brand` as brand, 
      `p.car_series` as series,
      `p.car_color` as color,
      `p.room_name` as owner_name,
      `p.telephone` as owner_telephone,
      `p.id_card_number` as owner_certificate_no,
      `p.room_no`as room_code,
			`i.area_code`as estate_code 
    FROM t_plateusers AS p
    LEFT JOIN t_parkinfo AS i on p.park_no = i.park_no
		where city_code=440300  AND estate_code=971000;
    