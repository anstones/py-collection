import mysql.connector
from lib.getconf import getConfig
import numpy as np
import pickle, json
import pyDes
import traceback
from binascii import a2b_hex

"""
pymsql 带重连机制
"""

DES_KEY="01123456"
k=pyDes.des(DES_KEY, pyDes.ECB, "\0\0\0\0\0\0\0\0", pad=None, padmode=pyDes.PAD_PKCS5)
class Mysql_Query:
    def __init__(self,host,user,password):
        self.host = host
        self.user = user
        self.password = password
        self.conn = mysql.connector.connect(host=host,user=user,password=password)
        print("===", self.conn)
        #self.cursor = self.conn.cursor()

    def reconnect(self):
        self.conn = mysql.connector.connect(host=self.host,user=self.user,password=self.password)
        #self.cursor = self.conn.cursor()

    def get_cursor(self):
        try:
            cursor = self.conn.cursor()
        except:
            self.reconnect()
            cursor = self.conn.cursor()
        
        return cursor

    def uid_query(self,uids):
        res = []
        uids_str = "'"+"','".join(uids)+"'"
        sql_operation = "select user_id, unit_id, building_name, room_name, `name`, id_type, id_code, telephone, user_image, face_id from db_bigdata.tp_house_user where user_id in ({}) or face_id in ({})".format(uids_str, uids_str)
        print("sql_operation:",sql_operation)
        # cursor = self.conn.cursor()
        try:
            #cursor = self.conn.cursor()
            cursor = self.get_cursor()
            cursor.execute(sql_operation)
            #except Exception,e:
            #print(traceback.format_exc())
            #print "mysql error=== {}".format(e)
            #self.reconnect()
            #self.cursor.execute(sql_operation)
            r = cursor.fetchall()
            cursor.close()
            print("============================= ", r)
            #for item in cursor.fetchall():
            for item in r:
                if item[9] in uids:
                    res.append({
                                "uid":item[9],
                                "unit_id":item[1],
                                "building_name":item[2],
                                "room_name":item[3],
                                "name":item[4],
                                "id_type":item[5],
                                "id_code":k.decrypt(a2b_hex(item[6])),
                                "telephone":k.decrypt(a2b_hex(item[7])),
                                "face_image":item[8]})
                else:
                    res.append({
                        "uid":item[0],
                        "unit_id":item[1],
                        "building_name":item[2],
                        "room_name":item[3],
                        "name":item[4],
                        "id_type":item[5],
                        "id_code":k.decrypt(a2b_hex(item[6])),
                        "telephone":k.decrypt(a2b_hex(item[7])),
                        "face_image":item[8]})
            return res
        except Exception,e:
            print(traceback.format_exc())
        #finally:
            #cursor.close()

    def unit_query(self,unit_ids):
        res = []
        unit_str = "'"+"','".join(map(lambda x: str(x),unit_ids))+"'"
        sql_operation = "select id, name, province_name, city_name, town_name from db_bigdata.t_base_unit where id in ({})".format(unit_str)
        try:
            cursor = self.get_cursor()
            cursor.execute(sql_operation)
            #except Exception,e:
            #print "mysql error {}".format(e)
            #self.reconnect()
            #self.cursor.execute(sql_operation)
            for item in cursor.fetchall():
                res.append({
                    "id":item[0],
                    "name":item[1],
                    "province_name":item[2],
                    "city_name":item[3],
                    "town_name":item[4]})
            return res
        except Exception,e:
            print(traceback.format_exc())
        finally:
            cursor.close()

    def blacklist_query(self):
        res = []
        sql_operation = "select item_id, user_id, image_id from db_securitycenter.peopleblacklist"
        try:
            cursor = self.get_cursor()
            cursor.execute(sql_operation)
            #except Exception,e:
            #print "mysql error {}".format(e)
            #self.reconnect()
            #self.cursor.execute(sql_operation)
            for item in cursor.fetchall():
                res.append({"item_id": item[0], 'user_id': item[1], 'image_id': item[2]})
            return res
        except Exception,e:
            print(traceback.format_exc())
        finally:
            cursor.close()

    # def get_face_md5_1(self):
    #     # sql_operation = 'select f.pic_md5, f.uid, d.device uid from feature f, device d where f.uid=d.uid and d.device LIKE "' + \
    #     #                 '0000004858' + '%" limit 10'
    #     sql_operation = ''
    #
    #     try:
    #         self.cursor.execute(sql_operation)
    #     except Exception, e:
    #         pass
    #     for item in self.cursor.fetchall():
    #         print(item)
    #     return ''

    def get_face_feature(self):
        white_uids = []
        white_md5s = []
        white_features = []
        white_city_code = []
        white_town_code = []
        black_uids = []
        black_md5s = []
        black_features = []
        black_city_code = []
        black_town_code = []

        sql_operation = "select u.uid, u.pic_md5, f.feature, f.city_code, f.town_code from facefeature.feature_model_0330 f, facefeature.user u where f.user_id=u.id"
        #cursor = self.conn.cursor()
        try:
            cursor = self.get_cursor()
            cursor.execute(sql_operation)
            #except Exception,e:
            #print "mysql error {}".format(e)
            #self.reconnect()
            #self.cursor.execute(sql_operation)
            for item in cursor.fetchall():
                uid = item[0]
                if item[1]==None:
                    continue
                uid_md5s = pickle.loads(item[1])
                uid_features = eval(bytearray.decode(item[2], encoding='utf-8'))
                if item[3]==None:
                    uid_city_code = [-1 for i in range(20)]
                else:
                    uid_city_code = [item[3] for i in range(20)]
                if item[4]==None:
                    uid_town_code = [-1 for i in range(20)]
                else:
                    uid_town_code = [item[4] for i in range(20)]
                #print item[4]
                if uid.startswith('black'):
                    for md5, feature, city_code, town_code in zip(uid_md5s, uid_features['emb_2'], uid_city_code, uid_town_code):
                        black_uids.append(uid)
                        black_md5s.append(md5)
                        black_features.append(np.array(feature, dtype=np.float32))
                        black_city_code.append(city_code)
                        black_town_code.append(town_code)
                else:
                    for md5, feature, city_code, town_code in zip(uid_md5s, uid_features['emb_2'], uid_city_code, uid_town_code):
                        white_uids.append(uid)
                        white_md5s.append(md5)
                        white_features.append(np.array(feature, dtype=np.float32))
                        white_city_code.append(city_code)
                        white_town_code.append(town_code)

            return np.array(white_uids), np.array(white_md5s), np.array(white_features), np.array(white_city_code), np.array(white_town_code), np.array(black_uids), np.array(black_md5s), np.array(black_features), np.array(black_city_code), np.array(black_town_code)
        except Exception,e:
            print(traceback.format_exc())
        finally:
            cursor.close()
