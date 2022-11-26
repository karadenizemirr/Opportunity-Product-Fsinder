import requests
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
'referer' :"http://akakce.com/"}

s = requests.Session()
req = s.get("http://akakce.com/")
print(req.text)