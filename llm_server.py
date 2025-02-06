# app.py
from flask import Flask, request, jsonify
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

app = Flask(__name__)

MODEL_NAME = "elyza/ELYZA-japanese-Llama-2-7b-instruct"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, use_fast=False)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    torch_dtype=torch.float32,
    device_map=None
)

# デバイスの設定
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = model.to(device)

@app.route('/soften', methods=['POST'])
def soften_text():
    try:
        data = request.get_json()
        original_text = data.get("text", "")
        
        # より具体的なプロンプトを設定
        prompt = f"""
次の文章を、感情的な表現を抑えて、より丁寧な表現に書き換えてください。
元の意図は保持しつつ、穏やかな表現にしてください。
また、元の文章と同程度の分量で書き換えてください。

元の文章：{original_text}
書き換えた文章："""

        # トークン化とモデル入力の準備
        inputs = tokenizer(prompt, return_tensors="pt").to(device)
        
        # 生成パラメータの調整
        with torch.no_grad():
            outputs = model.generate(
                inputs['input_ids'],
                max_length=256,
                do_sample=True,
                temperature=0.6,  # より控えめな温度
                top_p=0.9,
                repetition_penalty=1.2,  # 繰り返しを防ぐ
                pad_token_id=tokenizer.pad_token_id,
                eos_token_id=tokenizer.eos_token_id
            )
        
        softened_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # プロンプトの部分を除去して結果のみを取得
        result = softened_text.split("書き換えた文章：")[-1].strip()
        
        return jsonify({"softer_text": result})
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({
            "error": str(e),
            "softer_text": original_text
        }), 500

if __name__ == '__main__':
    app.run(port=5000)
