import json
import os

import requests
from dotenv import load_dotenv, find_dotenv

# read local .env file
load_dotenv(find_dotenv())

API_KEY = os.environ['ERNIE_API_KEY']
SECRET_KEY = os.environ['ERNIE_SECRET_KEY']


def get_access_token():
    """
    使用 AK，SK 生成鉴权签名（Access Token）
    :return: access_token，或是None(如果错误)
    """
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}
    return str(requests.post(url, params=params).json().get("access_token"))


def main():
    url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/eb-instant?access_token=" \
          + get_access_token()

    payload = json.dumps({
        "messages": [
            {
                "role": "user",
                "content": "什么是NLP？"
            },
            {
                "role": "assistant",
                "content": "NLP是自然语言处理的缩写，它是指对自然语言进行的计算机处理。自然语言处理是人工智能领域的一个分支，\
                           旨在使计算机能够理解和生成人类语言。NLP的研究涉及多个领域，如语言学、计算机科学、数学等，包括\
                           如何处理自然语言数据、如何建立有效的文本分类系统、如何识别和纠正拼写和语法错误、如何生成人类语言等。"
            },
            {
                "role": "user",
                "content": "能详细说说这些研究领域吗？"
            }
        ]
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(json.loads(response.text)['result'])


if __name__ == '__main__':
    main()
