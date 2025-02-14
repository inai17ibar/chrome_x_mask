# -*- coding: utf-8 -*-
import requests
import json
from flask import jsonify

url = "http://127.0.0.1:5000/soften"

texts = [
    "「プロは素人より上だから素人がプロにガタガタ言うな」論を心底ゴミだと思ってる",
    "男を一括りにするな。警戒しない女が悪い。こんな時だけ男を頼るな。マンコ二毛作w",
    "うわ、マズそう。そこなんて貧乏人が行く所だよ。"
]

for text in texts:
    response = requests.post(url, json={"text": text})
    if response.status_code == 200:
        data = response.json()
        print(f"元のテキスト: {text}")
        print(f"言い換え後のテキスト: {data['softer_text']}\n")
    else:
        print(f"エラー: {response.status_code}")

data = {"softer_text": "テキスト"}
json_data = json.dumps(data, ensure_ascii=False)