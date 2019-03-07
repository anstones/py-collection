SELECT
r.room_code,
m.before_data last_property_usage,
m.curr_data as property_usage
from 
t_upb_room as r
LEFT JOIN
room_meter_data as m
ON
r.room_code=m.room_code
WHERE
r.unit_id=971104 
and 
r.building=0101
AND
m.meter_type=1
GROUP BY
r.room_code
