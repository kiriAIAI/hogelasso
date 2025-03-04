// 編集要素の取得
    const titleInput = document.getElementById('titleInput');
    const contentInput = document.getElementById('contentInput');

    // 入力フィールドを編集可能な領域に変換する
    function makeEditable(element) {
        const editableDiv = document.createElement('div');
        editableDiv.contentEditable = true;
        editableDiv.className = element.className;
        editableDiv.style.minHeight = element.offsetHeight + 'px';
        editableDiv.style.width = '100%';
        editableDiv.style.border = '1px solid #ccc';
        editableDiv.style.padding = '8px';
        editableDiv.innerHTML = element.value;

        element.parentNode.insertBefore(editableDiv, element);
        element.style.display = 'none';

        // 元の入力フィールドに内容を同期させる
        editableDiv.addEventListener('input', () => {
            element.value = editableDiv.innerHTML;
        });

        return editableDiv;
    }

    // 編集可能コンテンツ
    const editableTitleDiv = makeEditable(titleInput);
    const editableContentDiv = makeEditable(contentInput);

    // formatDoc
    function formatDoc(command, value = null) {
        document.execCommand(command, false, value);
    }


    // 色選択
    function updateColorValue(color) {
      document.getElementById('hexValue').textContent = color.toUpperCase();
      document.getElementById('swatch').style.backgroundColor = color;
      applyStyleToSelection('color', color); 
    };

    document.getElementById('colorPicker').addEventListener('input', function(e) {
      updateColorValue(e.target.value);
    });

    updateColorValue('#ff0000');

    document.getElementById('wf-form-Create-Form').addEventListener('submit', function(e) {
      e.preventDefault();
      
      const titleContent = document.getElementById('titleInput').innerHTML;
      const textContent = document.getElementById('contentInput').innerHTML;
      
    });

    function updateColorValue(color) {
      document.getElementById('hexValue').textContent = color.toUpperCase();
      document.getElementById('swatch').style.backgroundColor = color;
      document.execCommand('foreColor', false, color);
    }

    document.addEventListener('DOMContentLoaded', function() {
        const editableTitleDiv = document.querySelector('[contenteditable="true"]');
        const editableContentDiv = document.querySelector('div.textarea[contenteditable="true"]');

        [editableTitleDiv, editableContentDiv].forEach(element => {
            if (element) {
                element.addEventListener('focus', function() {
                    this.setAttribute('data-focused', 'true');
                });
                
                element.addEventListener('blur', function() {
                    this.removeAttribute('data-focused');
                });
            }
        });
    });


    // フォントサイズ
    let size = 1; // 初期フォントサイズ
    const sizeInput = document.getElementById('sizeInput');
    const sizeValue = document.getElementById('sizeValue'); // 数値表示用の要素を取得

    // スライダーの初期値を設定
    sizeInput.value = size;
    sizeValue.textContent = size; // 初期値を表示

    // 入力からフォントサイズを更新
    sizeInput.addEventListener('input', function() {
        let value = parseFloat(this.value);
        if (isNaN(value)) {
            value = 1;
        }
        // 限界範囲
        if (value < 0.5) value = 0.5;
        if (value > 5) value = 5;

        size = value;
        sizeValue.textContent = size.toFixed(1); // 数値を更新
        updateDisplay();
        adjustFontSize(0); // スライダーの変更に応じてフォントサイズを調整
    });

    // フォントサイズ調整機能
    function adjustFontSize(delta) {
        const selection = document.getSelection();
        if (selection.rangeCount > 0) {
            const range = selection.getRangeAt(0);
            const selectedText = range.toString();

            if (selectedText) {
                const span = document.createElement('span');
                size = Math.max(0.5, Math.min(size + delta, 5)); // フォントサイズを更新
                span.style.fontSize = `${size}rem`; // 更新されたサイズを使用
                span.textContent = selectedText;

                range.deleteContents();
                range.insertNode(span);

                // 行の高さを調整
                const parentElement = span.parentNode;
                parentElement.style.lineHeight = `${size}rem`; // 行の高さをフォントサイズに基づいて設定

                updateDisplay();
            }
        }
    }

    // アップデート表示機能
    function updateDisplay() {
        const displayValue = size === Math.floor(size) ? Math.floor(size) : size.toFixed(1);
        sizeInput.value = displayValue;
    }
    
    

    // 挿入リスト
    function insertList(command) {
        formatDoc(command);
    }
    
    // チェックボックス
    function insertCheckbox() {
        const selection = window.getSelection();
        if (selection.rangeCount > 0) {
            const range = selection.getRangeAt(0);
            const text = range.toString();
            const div = document.createElement('div');
            div.innerHTML = `<input type="checkbox"> ${text}`;
            range.deleteContents();
            range.insertNode(div);
        }
    }

    // 画像プレビュー機能
    document.addEventListener('DOMContentLoaded', function() {
      const fileUpload = document.getElementById('fileUpload');
      const preview = document.getElementById('preview');
      const dropZone = document.getElementById('dropZone');
      const previewContainer = document.getElementById('imagePreview');

      // ファイルの選択
      fileUpload.addEventListener('change', handleFileSelect);

      // ドラッグ＆ドロップ処理
      previewContainer.addEventListener('dragover', handleDragOver);
      previewContainer.addEventListener('drop', handleDrop);

      function handleFileSelect(e) {
        const file = e.target.files[0];
        displayPreview(file);
      }

      function handleDragOver(e) {
        e.preventDefault();
        e.stopPropagation();
        previewContainer.style.borderColor = '#2196f3';
      }

      function handleDrop(e) {
        e.preventDefault();
        e.stopPropagation();
        previewContainer.style.borderColor = '#ccc';
        
        const file = e.dataTransfer.files[0];
        if (file && file.type.startsWith('image/')) {
          fileUpload.files = e.dataTransfer.files;
          displayPreview(file);
        }
      }

      function displayPreview(file) {
        if (file && file.type.startsWith('image/')) {
            const reader = new FileReader();
            
            reader.onload = function(e) {
                // 圧縮画像
                const img = new Image();
                img.onload = function() {
                    const canvas = document.createElement('canvas');
                    const ctx = canvas.getContext('2d');
                    
                    // 最大サイズの設定
                    const MAX_WIDTH = 800;
                    const MAX_HEIGHT = 800;
                    
                    let width = img.width;
                    let height = img.height;
                    
                    // スケーリング計算
                    if (width > height) {
                        if (width > MAX_WIDTH) {
                            height *= MAX_WIDTH / width;
                            width = MAX_WIDTH;
                        }
                    } else {
                        if (height > MAX_HEIGHT) {
                            width *= MAX_HEIGHT / height;
                            height = MAX_HEIGHT;
                        }
                    }
                    
                    canvas.width = width;
                    canvas.height = height;
                    
                    // 圧縮された画像を描く
                    ctx.drawImage(img, 0, 0, width, height);
                    
                    // より小さなJPEGフォーマットに変換
                    const compressedDataUrl = canvas.toDataURL('image/jpeg', 0.7);
                    
                    preview.src = compressedDataUrl;
                    preview.style.display = 'block';
                    dropZone.style.display = 'none';
                };
                img.src = e.target.result;
            };
            
            reader.readAsDataURL(file);
        } else {
            alert('画像ファイルを選択してください。');
        }
      }

      // プレビューエリアをクリックすると、ファイル選択
      dropZone.addEventListener('click', function() {
        fileUpload.click();
      });

      preview.addEventListener('click', function() {
        fileUpload.click();
      });
      
    });

    // 投稿フォームの送信
    document.getElementById('wf-form-Create-Form').onsubmit = function(e) {
      e.preventDefault();
      
      const title = editableTitleDiv.innerHTML;
      const content = editableContentDiv.innerHTML;
      const category = document.getElementById('categorySelect').value;
      const price = document.getElementById('priceInput').value;
      const Image_data = document.getElementById('fileUpload');
      const editBookId = new URLSearchParams(window.location.search).get('edit_book_id');
      
      // form検証
      if (!title.trim() || title === '<br>') {
          alert('タイトルを入力してください');
          return;
      }
  
      if (!content.trim() || content === '<br>') {
          alert('内容を入力してください');
          return;
      }
  
      if (!category) {
          alert('カテゴリを選択してください');
          return;
      }
  
      if (!price) {
          alert('価格を入力してください');
          return;
      }
      
      // 新規作成時のみ画像をチェック
      if (!editBookId && !Image_data.files[0]) {
          alert('表紙画像をアップロードしてください');
          return;
      }

      // formDataを準備する
      const formData = {
          title: title.trim(),
          content: content.trim(),
          category: category,
          price: price,
          edit_book_id: editBookId
      };

      // 新しい画像がある場合、formDataに追加
      if (Image_data.files[0]) {
          formData.cover_image_path = Image_data.files[0].name;
      }

      // 編集モードかどうかで異なるエンドポイントを選択
      const endpoint = editBookId ? '/update_post' : '/submit_create';
  
      fetch(endpoint, {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json',
          },
          body: JSON.stringify(formData),
      })
      .then(response => response.json())
      .then(data => {
          console.log('Server response:', data);
          if (data.message === '成功') {
              alert(editBookId ? '更新が完了しました！' : '投稿が完了しました！');
              // 新しい画像がある場合、アップロード
              if (Image_data.files.length > 0) {
                  const ImageData = new FormData();
                  ImageData.append('image_data', Image_data.files[0]);
                  return fetch('/image_upload', {
                      method: 'POST',
                      body: ImageData
                  });
              }
              return Promise.resolve();
          } else {
              throw new Error(data.message);
          }
      })
      .then(() => {
          window.location.href = '/';
      })
      .catch(error => {
          console.error('Error:', error);
          alert('エラー：' + error.message);
      });
    };

document.getElementById('sizeInput').addEventListener('input', function() {
    const value = this.value;
    const min = this.min;
    const max = this.max;
    const percentage = ((value - min) / (max - min)) * 100;
    this.style.background = `linear-gradient(to right, #6a6a6a ${percentage}%, #e0e0e0 ${percentage}%)`;
});