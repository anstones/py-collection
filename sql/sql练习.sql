-- SELECT * from (SELECT count(*) as count,city from (SELECT city,main_bussiness_income,net_profit,stock_code from listed_company3 where province LIKE '%陕西%')a GROUP BY city) t ORDER BY t.count DESC
-- SELECT city,main_bussiness_income,net_profit,stock_code from listed_company3 ORDER BY CONVERT(main_bussiness_income,SIGNED) DESC  


-- SELECT t.count,t.sum,t.province from (SELECT SUM(CONVERT(main_bussiness_income,SIGNED))as sum, count(*) as count, province from listed_company3 GROUP BY province)t ORDER BY t.count DESC 

-- 问题： 
-- 1、查询“001”课程比“002”课程成绩高的所有学生的学号；

-- SELECT b.sid from (SELECT score,sid from sc WHERE cid=1)a,(SELECT score,sid from sc WHERE cid=2)b WHERE a.score>b.score and a.sid=b.sid

-- 2、查询平均成绩大于60分的同学的学号和平均成绩；
-- SELECT sid,sum(score)/count(*)as pj from sc GROUP BY sid HAVING pj >60
-- SELECT sid,AVG(score) from sc  GROUP BY sid HAVING AVG(score)>60

-- 3、查询所有同学的学号、姓名、选课数、总成绩；
-- SELECT student.sid,student.sname,count(sc.cid),sum(sc.score) from student LEFT JOIN sc on student.sid=sc.sid GROUP BY student.sid,student.sname

-- 4、查询姓“李”的老师的个数； 
-- SELECT COUNT(*) from teacher WHERE tname LIKE '李%'

-- 5.查询没学过“叶平”老师课的同学的学号、姓名；
-- SELECT student.sid,student.sname from student WHERE sid not in (SELECT sc.sid from sc,course,teacher WHERE sc.cid=course.cid and teacher.tid=course.tid and tname='叶平')

-- 6、查询学过“001”并且也学过编号“002”课程的同学的学号、姓名； 
-- SELECT student.sid,student.sname from sc,student WHERE student.sid=sc.sid and sc.cid =1 and EXISTS (SELECT * from sc as sc_2 WHERE sc_2.sid=sc.sid and sc_2.cid =2)

-- 7、查询学过“叶平”老师所教的所有课的同学的学号、姓名；
-- SELECT student.sid,student.sname from student WHERE sid in (SELECT sc.sid from sc,course,teacher WHERE sc.cid=course.cid and teacher.tid=course.tid and tname='叶平')


-- 8、查询课程编号“002”的成绩比课程编号“001”课程低的所有同学的学号、姓名
-- SELECT a.sid from (SELECT sid,score from sc WHERE cid=1)a,(SELECT sid,score from sc WHERE cid=2)b WHERE a.score > b.score and a.sid= b.sid 

-- 9、查询所有课程成绩小于60分的同学的学号、姓名；
-- SELECT sname,sid from student WHERE sid in(SELECT student.sid from student,sc WHERE sc.score<60 and student.sid=sc.sid ) 

-- 10、查询没有学全所有课的同学的学号、姓名
-- SELECT student.sname,student.sid from student,sc WHERE student.sid = sc.sid  GROUP BY student.sname,student.sid HAVING count(cid)< (SELECT count(*) from course)
 
-- 11、查询至少有一门课与学号为“1001”的同学所学相同的同学的学号和姓名； 
-- SELECT DISTINCT student.sid,student.sname from student,sc WHERE student.sid = sc.sid and sc.cid in(SELECT cid from sc WHERE sid =1)

-- 12、查询至少学过学号为“001”同学所有一门课的其他同学学号和姓名；
-- SELECT DISTINCT student.sid,student.sname from student,sc WHERE student.sid=sc.sid and sc.cid in (SELECT cid from sc WHERE sid=1)

-- 13、把“SC”表中“叶平”老师教的课的成绩都更改为此课程的平均成绩；
-- UPDATE sc set score =(select avg(t.score) from (SELECT score from sc,course,teacher WHERE course.cid = sc.cid and course.tid=teacher.tid  and teacher.tname='叶平') t)

-- 14、查询和“1002”号的同学学习的课程完全相同的其他同学学号和姓名；
-- SELECT student.sname,student.sid from student,sc WHERE student.sid = sc.sid  GROUP BY student.sname,student.sid HAVING count(cid)=(SELECT count(*) from sc WHERE sid = 2 )


-- 26、查询每门课程被选修的学生数
-- SELECT cid,count(sid) from sc GROUP BY cid

-- 27、查询出只选修了一门课程的全部学生的学号和姓名 
-- SELECT student.sname,student.sid from student WHERE sid in (SELECT sid from sc GROUP BY sid HAVING count(cid)=3)

-- 28、查询男生、女生人数 
-- SELECT count(*) from student WHERE ssex='男'
-- SELECT count(*) from student WHERE ssex='女'

-- 29、查询姓“张”的学生名单
-- SELECT * from student WHERE sname like '张%'

-- 30、查询同名同性学生名单，并统计同名人数  (having  count(*)>1 可表示某个相同的属性)
-- select sname,count(*) from student group by sname having  count(*)>1

-- 31、2000年出生的学生名单(注：Student表中Sage列的类型是datetime)
-- SELECT * from student WHERE sage = 2018-2000

-- 32、查询每门课程的平均成绩，结果按平均成绩升序排列，平均成绩相同时，按课程号降序排列
-- SELECT cid,avg(score) from sc GROUP BY cid ORDER BY avg(score) desc

-- 33、查询平均成绩大于85的所有学生的学号、姓名和平均成绩 





