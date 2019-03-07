SELECT
room.room_code as house_code,
room.room_name as house_name,
room.use_status as useage,
room.name as ower_name,
count(u.room_code) as reside_amount
FROM 
t_upb_room as room,
house_user as u
WHERE
room.room_code=u.room_code
and
room.unit_id=971104
GROUP BY
room.room_code
