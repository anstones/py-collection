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
    FROM 
        t_plateusers AS p
    LEFT JOIN house_user AS h on p.user_name=h.`name` and p.id_card_number=h.id_code,
				t_parkinfo AS i,
				t_pb_unit AS u
    WHERE i.area_code = u.id AND p.park_no = i.park_no
		AND (''='' OR p.plate like '' OR p.id_card_number like '' OR p.telephone like '') 
    AND (''='' OR u.province_code='') 
    AND ('370500'='' OR u.city_code='370500') 
    AND (''='' OR u.town_code='') 
    AND (''='' OR u.id='')