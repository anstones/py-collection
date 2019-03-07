SELECT 
room.room_code,
count(s.special_type) as care_person_amount
FROM 
t_upb_room as room,
tb_special_person as s 
WHERE
room.room_code=s.room_code
and
room.unit_id=971104 
and 
room.building=0101
and 
s.special_type=2
GROUP BY
room.room_code