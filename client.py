import requests

response = requests.get("http://127.0.0.1:5000/ad/1",
                         json={
                             'title': 'title1',
                             "description": "desc1",
                             'owner': 'user1'
                         })
print(response.status_code)
print(response.text)
