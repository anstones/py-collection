#encoding=utf-8
import pymysql
import requests,sys,os,time,json
 
class Mysql(object):
    def __init__(self):
        self.__db_host = "192.168.1.8"
        self.__db_port = 3306
        self.__db_user = "ys"
        self.__db_psw  = ""
        self.__db_database = "my"
 
    def db_connection(self):
        self.__connection = pymysql.connect(
                                            host=self.__db_host,
                                            port=self.__db_port,
                                            user=self.__db_user,
                                            passwd=self.__db_psw,
                                            db=self.__db_database,
                                            charset='utf8'
                                            )
        # self.
        self.__connection.autocommit(True)
    def execute_no_query(self,command_text,parameters=None):
        effectRow = 0
        try:
            self.db_connection()
            cursor = self.__connection.cursor()
            effectRow = cursor.execute(command_text,parameters)
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            return effectRow
 
    def db_close(self):
        if hasattr(self, 'conn') and self.__conn:


file_path =os.path.join(sys.path[0],"test.txt")
file=open(file_path,'r',encoding='utf-8')
for line in file.readlines():
    uid="null"
    pic_md5="null"
    province_code="null"
    town_code="null"
    city_code="null"
    if line:
        li=[]
        li=line.encode('utf-8').decode('utf-8-sig').strip('\n').split("________")
        uid = li[0] if len(li[0])>0 else "null"
        pic_md5 = li[1] if len(li[1])>0 else "null"
        province_code = li[2] if len(li[3])>0 else "null"
        town_code = li[3] if len(li[3])>0 else "null"
        city_code = li[4] if len(li[4])>0 else "null"
        sql = """
            insert into user (uid,pic_md5,province_code,town_code,city_code) VALUES ('%s','%s','%s','%s','%s')"""
 
        try:
            mysql = Mysql()
            mysql.execute_no_query(sql % (uid,pic_md5,province_code,town_code,city_code))
        except Exception as e:
            print(e)
        finally:
            mysql.db_close()
    else:
