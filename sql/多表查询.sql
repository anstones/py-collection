SELECT 
      `plate` as plate_no,
      `car_brand` as brand, 
      `car_series` as series,
      `car_color` as color,
      `user_name` as owner_name,
       p.telephone as owner_telephone,
      `id_card_number` as owner_certificate_no,
      `room_no`as room_code,
      `area_code` as estate_code,
      `province_name`,
       u.city_name,
       u.name as estate_name,
      `park_name`,
       i.park_no,
      `type` as resident_type
FROM t_parkinfo AS i
LEFT JOIN t_plateusers AS p on p.park_no = i.park_no
LEFT JOIN db_unitpropertybase.t_pb_unit AS u on i.area_code = u.id
LEFT JOIN db_unitpropertybase.house_user AS h on p.room_no = h.room
where i.city_code=440300  AND i.area_code=971000