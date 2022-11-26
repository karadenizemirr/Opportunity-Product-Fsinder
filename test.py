import requests

URL = "http://85.111.4.208/"

session = requests.Session()
print(session.get(URL))