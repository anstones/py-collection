SELECT 
DATE_FORMAT(o.create_time,'%%Y-%%m') month,
sum(o.amount) as objective_amount 
from tb_objective_guard as o
WHERE(%(province_code)s='' OR o.province_code=%(province_code)s)
AND (%(city_code)s='' OR o.city_code=%(city_code)s) 
AND (%(town_code)s='' OR o.town_code=%(town_code)s)
AND (%(estate_code)s='' OR o.estate_code=%(estate_code)s)
AND DATE_FORMAT(o.create_time,'%%Y-%%m')>
        DATE_FORMAT(DATE_SUB(curdate(), interval 1 YEAR),'%%Y-%%m')
GROUP BY
month 