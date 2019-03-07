-- SELECT COUNT(1) AS allcount
--    FROM tp_house_user where sex="男" or sex="女"
-- 3084
-- select count(*) as'total_amount' from tp_house_user WHERE province_code=520000 and city_code=520600 and unit_id=3522



-- 统计总人口和男女
--    SELECT a.total_amount,
--           b.male_amount,
--           c.female_amount
--    FROM
--      (SELECT COUNT(*) AS total_amount
--       FROM tp_house_user where province_code=520000 and city_code=520600 and unit_id=3522)AS a
--    LEFT JOIN
--      (SELECT COUNT(*)AS male_amount
--       FROM tp_house_user 
--       WHERE sex = "男" and province_code=520000 and city_code=520600 and unit_id=3522)b ON 1=1
--    LEFT JOIN
--      (SELECT COUNT(*)AS female_amount
--       FROM tp_house_user
--       WHERE sex = "女" and province_code=520000 and city_code=520600 and unit_id=3522)c ON 1=1





-- SELECT birth FROM tp_house_user WHERE birth != '' ORDER BY birth DESC

-- SELECT DATEDIFF(CURRENT_DATE,birth) as "age",sex FROM tp_house_user WHERE birth != ''

-- select '25-30岁' as 年龄段 count(*) as 人数 from tp_house_user where year(getdate())-year(birth)>=25 and year(getdate())-year(birth)<30 WHERE birth != ''

-- SELECT (SELECT birth,sex from tp_house_user WHERE birth != "") as a 

-- SELECT birth,sex from tp_house_user WHERE birth != ""

-- select '10-18岁' as 年龄段 count(*) as 人数 from (select DATEDIFF(CURRENT_DATE, birth)/365 as 'age',sex from tp_house_user)a where a.age>=10 and a.age<18




--  统计人口组成结构:  总数- 查询出来的数量和    余下的表示：  未统计年龄或者性别
--   SELECT nnd as age_range,sex,count(*) as amount from(
--     SELECT
--      CASE
--       WHEN ROUND(DATEDIFF(CURDATE(), birth)/365.2422) > 0 and ROUND(DATEDIFF(CURDATE(), birth)/365.2422) < 10 THEN '0-10岁'
--       WHEN ROUND(DATEDIFF(CURDATE(), birth)/365.2422) >= 10 and ROUND(DATEDIFF(CURDATE(), birth)/365.2422) < 18 THEN '10-18岁'
--       WHEN ROUND(DATEDIFF(CURDATE(), birth)/365.2422) >= 18 and ROUND(DATEDIFF(CURDATE(), birth)/365.2422) < 30 THEN '18-30岁'
--       WHEN ROUND(DATEDIFF(CURDATE(), birth)/365.2422) >= 30 and ROUND(DATEDIFF(CURDATE(), birth)/365.2422) < 50 THEN '30-50岁'
--       WHEN ROUND(DATEDIFF(CURDATE(), birth)/365.2422) >= 50 and ROUND(DATEDIFF(CURDATE(), birth)/365.2422) < 70 THEN '50-70岁'
--       WHEN ROUND(DATEDIFF(CURDATE(), birth)/365.2422) >= 70 THEN '70岁以上'
--      END 
--      as nnd,sex as sex
--      from tp_house_user where province_code=520000 and city_code=520600 and unit_id=3522
--   ) a GROUP BY nnd,sex;
 



-- 统计关爱人和关键人 总数- 查询出来的数量和    余下的表示：  未统计信息
--  province_code =520000
--  city_code = 520600
--  estate_code = 3522
  select special_person as categroy,count(*) as amount FROM tp_house_user where province_code=520000 and city_code=520600 and unit_id=3522 GROUP BY special_person
  UNION 
  SELECT  personnel_category as categroy,count(*) as amount from t_speical_personnel where city_code=520600 and unit_id=3522 GROUP BY personnel_category 








