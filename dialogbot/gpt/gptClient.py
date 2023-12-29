import json

import requests


class GptClient:
    def __init__(self,
                 model="gpt-4",
                 temperature=0,
                 stream=False,
                 cache=False,
                 max_tokens=2000):
        self.model = model
        self.temperature = temperature
        self.stream = stream
        self.cache = cache
        self.max_tokens = max_tokens
        self.api_key = "rzHaUysN"
        self.secret = "09dd003fa86a6bf6a790db88002371901fb8efee"
        self.url = 'https://sophon-ai.bytedance.net/gateway/openapi/model/chatCompletion'
        self.headers = {"api-key": self.api_key + ":" + self.secret,
                        "Content-Type": "application/json"}

    def get_answer(self, msg):
        body = {"model": self.model,
                "temperature": self.temperature,
                "stream": self.stream,
                "cache": self.cache,
                "maxTokens": self.max_tokens,
                "messages": msg}
        post_dict = json.dumps(body)
        r1 = requests.post(self.url, data=post_dict, headers=self.headers)
        res = json.loads(r1.text)
        return res['choices'][0]['message']['content']