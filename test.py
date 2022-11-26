import httpx
client = httpx.Client(http2=True)
response = client.get("https://www.akakce.com/")
print(response)