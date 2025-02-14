# app.py
from flask import Flask, request, jsonify
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import time
app = Flask(__name__)

print("Starting server...")
print("Loading model...")
#MODEL_NAME = "elyza/ELYZA-japanese-Llama-2-7b-instruct"
#MODEL_NAME = "deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B"
MODEL_NAME = "google/gemma-2-2b-it"

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, use_fast=False)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    torch_dtype=torch.float16,
    use_cache=True,
    #device_map="auto",  # 自動デバイス割り当て
    #offload_folder="./offload"  # オフロードフォルダを指定
)

print(f"Model loaded. Using device: {model.device}")

# デバイスの設定
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = model.to(device)

@app.route('/soften', methods=['POST'])
def soften_text():
    try:
        # 開始時間を記録
        start_time = time.time()
        
        data = request.get_json()
        original_text = data.get("text", "")
        
        # より具体的なプロンプトを設定
        prompt = f"""
次の文章を、感情的な表現を抑えて、より丁寧な表現に書き換えてください。
元の意図は保持しつつ、穏やかな表現にしてください。
また、元の文章と同程度の分量で書き換えてください。

元の文章：{original_text}
書き換えた文章："""

        # トークナイズ開始時間
        tokenize_start = time.time()
        inputs = tokenizer(prompt, return_tensors="pt", padding=True, truncation=True)
        tokenize_time = time.time() - tokenize_start
        
        # 推論開始時間
        inference_start = time.time()
        with torch.no_grad():
            outputs = model.generate(
                inputs['input_ids'],
                attention_mask=inputs['attention_mask'],
                max_length=256,
                do_sample=True,
                temperature=0.6,
                top_p=0.9,
                repetition_penalty=1.2,
                pad_token_id=tokenizer.pad_token_id,
                eos_token_id=tokenizer.eos_token_id
            )
        inference_time = time.time() - inference_start
        
        # デコード開始時間
        decode_start = time.time()
        softened_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
        decode_time = time.time() - decode_start
        
        # 合計時間
        total_time = time.time() - start_time
        
        return jsonify({
            "softer_text": softened_text,
            "processing_times": {
                "tokenize": tokenize_time,
                "inference": inference_time,
                "decode": decode_time,
                "total": total_time
            }
        })
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000, threaded=True)
