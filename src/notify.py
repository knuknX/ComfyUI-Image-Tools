import requests

def post_notify(url, headers=None, json_data=None):
    # 构造请求头
    headers = headers or {}

    # 发送 POST 请求
    response = requests.post(url, headers=headers, json=json_data)
    return response.text
