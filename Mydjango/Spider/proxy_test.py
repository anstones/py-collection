import requests

proxy = {
    'http': "http://123.150.8.42:8001",
}

head = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
    'Connection': 'keep-alive'}

p = requests.get('https://music.163.com/', headers=head, proxies=proxy)
print(p)
