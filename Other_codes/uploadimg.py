import requests
import gzip
from io import BytesIO
url = 'http://172.23.184.12:8481/FileService/DownloadFile?filesessionid=C4MS5GIGCK8UJ000PITVSC6UIG'


name = 'asfsaf.jpg'
r = requests.get(url=url)
path = r'C:\Users\Administrator\Desktop\huawei\static\uploads\{}'.format(name)

with gzip.open(BytesIO(r.content),"rb") as f_in:
    with open(path, "wb")as f_out:
        f_out.write(f_in.read())


""" 上传图片到图片服务器 """
zimg_upload_url = 'http://172.21.132.201/image/upload'
haha = open(r'C:\Users\Administrator\Desktop\huawei\haha.jpg', 'rb')
bb = haha.read()
files = {'file':('haha.jpg', open(r'C:\Users\Administrator\Desktop\huawei\haha.jpg', 'rb'), 'image/jpeg')}
head= {'Content-Type': 'multipart/form-data'}
r = requests.post(url=zimg_upload_url, data=files, headers=head)
print(r.content)


def rotate(nums,k):
    """ 旋转有序队列 """
    length = len(nums)
    k = k % length
    reverse(nums, 0, length-1)
    reverse(nums, 0, k-1)
    reverse(nums, k, length-1)
    print(nums)



def reverse(list, left, right):
    """ 手动实现有序列表反转 """
    while left < right:
        list[left], list[right] = list[right], list[left]
        left += 1
        right -= 1
    print(list)
    return list

nums = [0,1,2,3,4,5,6,7]
k = 3
rotate(nums, k)
reverse(nums, 0, len(nums)-1)
