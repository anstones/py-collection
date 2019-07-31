import requests
import gzip
from io import BytesIO
url = 'http://172.23.184.12:8481/FileService/DownloadFile?filesessionid=C4MS5GIGCK8UJ000PITVSC6UIG'


# name = 'asfsaf.jpg'
# r = requests.get(url=url)
# path = r'C:\Users\Administrator\Desktop\huawei\static\uploads\{}'.format(name)

# with gzip.open(BytesIO(r.content),"rb") as f_in:
#     with open(path, "wb")as f_out:
#         f_out.write(f_in.read())


# zimg_upload_url = 'http://172.21.132.201/image/upload'
# haha = open(r'C:\Users\Administrator\Desktop\huawei\haha.jpg', 'rb')
# bb = haha.read()
# files = {'file':('haha.jpg', open(r'C:\Users\Administrator\Desktop\huawei\haha.jpg', 'rb'), 'image/jpeg')}
# head= {'Content-Type': 'multipart/form-data'}
# r = requests.post(url=url, data=bb, headers=head)
# print(r.content)

# import json
# a = '{"ret":true,"info":{"md5":"2fc75d73f7cb34eabbb9667e1868def2_1553678526","filename":"","filetype":"JPEG","contenttype":"image/JPEG","filesize":0,"width":1920,"height":1080}}'

# b = json.loads(a)
# print(b.get('ret'))

# c= '/Snapshot/07462661284131280101/0746266128413128010120190327012932722849.jpg'

# d = c.split('/')[-1]
# print(d)


def rotate(nums,k):
    length = len(nums)
    k = k % length
    reverse(nums, 0, length-1)
    reverse(nums, 0, k-1)
    reverse(nums, k, length-1)
    print(nums)



def reverse(list, left, right):
    while left < right:
        list[left], list[right] = list[right], list[left]
        left += 1
        right -= 1

    return list

nums = [0,1,2,3,4,5,6,7]
k = 3
rotate(nums,k)

