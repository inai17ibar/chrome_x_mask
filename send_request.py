import requests
import json
import time

# サーバーのURL
url = "http://127.0.0.1:5000/soften"

# 送信するデータ
data = {
    "text": "「プロは素人より上だから素人がプロにガタガタ言うな」論を心底ゴミだと思ってる"
}

try:
    print("リクエスト送信中...")
    start_time = time.time()
    
    response = requests.post(
        url, 
        json=data, 
        timeout=600,
        headers={'Connection': 'keep-alive'}
    )
    
    total_time = time.time() - start_time
    print(f"リクエスト完了: {total_time:.2f}秒")
    
    if response.status_code == 200:
        response_data = response.json()
        print("\n変換後のテキスト:", response_data.get("softer_text"))
        
        if "processing_times" in response_data:
            times = response_data["processing_times"]
            print("\n処理時間の内訳:")
            print(f"トークナイズ: {times['tokenize']:.2f}秒")
            print(f"推論: {times['inference']:.2f}秒")
            print(f"デコード: {times['decode']:.2f}秒")
            print(f"サーバー側合計: {times['total']:.2f}秒")
            print(f"クライアント側合計: {total_time:.2f}秒")
    else:
        print("エラー:", response.status_code, response.text)
except requests.exceptions.RequestException as e:
    print(f"リクエストエラー: {e}")