import requests

session = requests.Session()

headers = {
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
    "_ga_SNSZLV7115" : "GS1.1.1669460797.5.1.1669460808.0.0.0",
        "_ga": "GA1.2.335449413.1669378655",
        "_gat": "1",
        "AAANSK": "530523214%7C83C0",
        "_gcl_au": "1.1.1946419028.1669378655",
        "_gid": "GA1.2.1527524974.1669378655",
        "1P_JAR": "2022-11-25-14"
}


session.headers.update(headers)


r = session.get("https://www.akakce.com/")
print(r)