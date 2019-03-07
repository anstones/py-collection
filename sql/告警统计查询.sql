SELECT 
	u.province_name, 
	pending_status as status,
	count(*)as count 
FROM tb_alarm_event as a
INNER JOIN db_unitpropertybase.t_pb_unit as u ON u.id=a.estate_code
WHERE a.province_code= 440000 AND a.create_time BETWEEN '2019-02-21'And '2019-02-22'
GROUP BY status
