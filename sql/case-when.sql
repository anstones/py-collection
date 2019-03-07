SELECT 
        CASE WHEN %(group_flag)s = 'province_name' THEN u.province_name
        WHEN %(group_flag)s = 'city_name' THEN u.city_name
        WHEN %(group_flag)s = 'town_name' THEN u.town_name
        WHEN %(group_flag)s = 'name' THEN u.name
        END as name,
        infrastructure_type AS type,
        COUNT(*) AS count 
    FROM 
        tb_infrastructure 
    LEFT JOIN t_pb_unit as u ON estate_code=u.id
    WHERE (%(estate_code)s='' OR estate_code=%(estate_code)s)
    GROUP BY
    CASE WHEN %(group_code)s = 'province_code' THEN i.province_code
        WHEN %(group_code)s = 'city_code' THEN i.city_code
        WHEN %(group_code)s = 'town_code' THEN i.town_code
        WHEN %(group_code)s = 'estate_code' THEN i.estate_code
        END 
    type