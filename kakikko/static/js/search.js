document.addEventListener('DOMContentLoaded', function() {
  const searchInput = document.getElementById('search');
  const suggestionsDiv = document.getElementById('search-suggestions');
  let debounceTimer;

  // 入力イベントの処理
  searchInput.addEventListener('input', function() {
    clearTimeout(debounceTimer);
    const query = this.value.trim();
    
    if (query.length < 1) {
      suggestionsDiv.style.display = 'none';
      return;
    }

    // 頻繁なリクエストを避けるため、300ミリ秒後に検索を遅らせる
    debounceTimer = setTimeout(() => {
      fetch(`/api/search-suggestions?query=${encodeURIComponent(query)}`)
        .then(response => response.json())
        .then(data => {
          suggestionsDiv.innerHTML = '';
          
          if (data.suggestions.length > 0) {
            data.suggestions.forEach(suggestion => {
              const div = document.createElement('div');
              div.className = 'suggestion-item';
              div.textContent = suggestion.title;
              div.addEventListener('click', () => {
                searchInput.value = suggestion.title;
                suggestionsDiv.style.display = 'none';
                // オプション：直接フォーム送信
                searchInput.closest('form').submit();
              });
              suggestionsDiv.appendChild(div);
            });
            suggestionsDiv.style.display = 'block';
          } else {
            suggestionsDiv.style.display = 'none';
          }
        });
    }, 300);
  });

  // ページ上の他の場所をクリックすると、サジェストを非表示にする
  document.addEventListener('click', function(e) {
    if (!searchInput.contains(e.target) && !suggestionsDiv.contains(e.target)) {
      suggestionsDiv.style.display = 'none';
    }
  });
});