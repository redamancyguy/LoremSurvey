import requests

url = 'http://1506607292.top'
params = {
    'id': 2
}
request = requests.get(url=url, params=params)
print(request.url)

{"sessionid": "9719a00ed0c5709d80dfef33795dcef3", "problemSet": [{"index": 1, "options": 1},
                                                                 {"index": 2, "options": 1},
                                                                 {"index": 3, "answer": "wojudehaixingba"},
                                                                 {"index": 4, "answer": "wojudehaixingba"}]}
