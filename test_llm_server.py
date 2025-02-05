import unittest
import json
from llm_server import app

class TestLLMServer(unittest.TestCase):
    def setUp(self):
        # テスト用のクライアントを作成
        self.app = app.test_client()
        self.app.testing = True

    def test_soften_text_endpoint(self):
        # テストデータの準備
        test_data = {
            "text": "「プロは素人より上だから素人がプロにガタガタ言うな」論を心底ゴミだと思ってる"
        }
        
        print("\n元のテキスト:")
        print(test_data["text"])
        
        # POSTリクエストを送信
        response = self.app.post('/soften',
                               data=json.dumps(test_data),
                               content_type='application/json')
        
        # レスポンスの検証
        self.assertEqual(response.status_code, 200)
        
        # レスポンスのJSONデータを取得
        data = json.loads(response.data)
        
        print("\n言い換え後のテキスト:")
        print(data['softer_text'])
        
        # レスポンスの構造を確認
        self.assertIn('softer_text', data)
        self.assertIsInstance(data['softer_text'], str)
        self.assertTrue(len(data['softer_text']) > 0)

    def test_invalid_request(self):
        # 無効なデータでテスト
        test_data = {}
        
        response = self.app.post('/soften',
                               data=json.dumps(test_data),
                               content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('softer_text', data)

if __name__ == '__main__':
    unittest.main(verbosity=2) 