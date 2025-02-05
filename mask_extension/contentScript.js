// 投稿要素を取得するためのセレクタ（例：data-testid属性が利用されている場合）
function processPosts() {
    const posts = document.querySelectorAll('[data-testid="tweetText"]');
    posts.forEach(post => {
      // 既に処理済みの場合はスキップ
      if (post.dataset.processed === "true") return;
  
      const originalText = post.innerText;
      // バックエンドAPIにテキスト変換リクエストを送る
      fetch("http://localhost:5000/soften", {  // バックエンドのエンドポイント
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ text: originalText })
      })
        .then(response => response.json())
        .then(data => {
          if (data && data.softer_text) {
            post.innerText = data.softer_text;
            post.dataset.processed = "true";  // 二重処理を防ぐ
          }
        })
        .catch(err => console.error("Error processing post:", err));
    });
  }
  
  // DOM変化を監視し、新たに追加された投稿も対象にする
  const observer = new MutationObserver(() => {
    processPosts();
  });
  
  observer.observe(document.body, { childList: true, subtree: true });
  
  // 初回実行
  processPosts();
  