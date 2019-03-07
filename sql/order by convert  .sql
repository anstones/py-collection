-- SELECT * from listed_company WHERE province LIKE '%陕西%' ORDER BY main_bussiness_income(code as signed integer) DESC

SELECT * from listed_company WHERE province LIKE '%陕西%' ORDER BY CONVERT(main_bussiness_income,SIGNED) DESC