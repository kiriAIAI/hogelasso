document.addEventListener("DOMContentLoaded", function () {
    // 各IDとクラスに対応する説明文を定義
    const tooltips = {
      "bell-icon": "通知",
      "shopping-cart": "ショッピングカート",
      "navbar-link": "アカウント",
      "backButton": "戻る",
      "sidenavbar-top": "サイドバーの展開",
      "sidenavbar-search": "検索",
      "home": "ホーム",
      "sakusei":"出品",
      "chat":"メッセージ",
      "rireki":"購入履歴",
      "profile":"プロフィール",
      "logout":"ログアウト",
      "button":"チャットボット",
      "dropZone":"画像をドロップ",
      "message-send-btn":"送信",
      "profile-edit-btn":"プロフィールを編集",
      "delete-btn":"商品を削除",
      "fa-heart":"いいね！",
      "Comment_Submission":"送信",
      "removeFromCart":"削除",
      "image":"画像を添付",
    };

    const tooltipElement = document.createElement("div");
    tooltipElement.classList.add("tooltip");
    document.body.appendChild(tooltipElement);

    // ID or Classリストを指定
    const ids = [
        "bell-icon",
        "navbar-link",
        "shopping-cart",
        "backButton",
        "sidenavbar-top",
        "sidenavbar-search",
        "home",
        "sakusei",
        "chat",
        "rireki",
        "profile",
        "logout",
        "button",
        "dropZone",
        "message-send-btn",
        "profile-edit-btn",
        "delete-btn",
        "fa-heart",
        "Comment_Submission",
        "removeFromCart",
        "image",
    ];

    // 各IDに対してマウスイベントを設定
    ids.forEach(id => {
      const element = document.getElementById(id);

      if (element) {
        element.addEventListener("mouseenter", function (e) {
          const tooltipText = tooltips[id];
          tooltipElement.textContent = tooltipText;

          // ツールチップを表示
          tooltipElement.style.display = "block";
          tooltipElement.style.left = e.pageX + "px";
          tooltipElement.style.top = e.pageY + 20 + "px"; // マウスの少し下に表示
        });

        element.addEventListener("mouseleave", function () {
          // ツールチップを非表示
          tooltipElement.style.display = "none";
        });
      } else {
        console.log(`ID: ${id} の要素は存在しません。`);
      }
    });

    // クラスに対してマウスイベントを設定
    ids.forEach(className => {
      const elements = document.getElementsByClassName(className);

      if (elements.length > 0) {
        Array.from(elements).forEach(element => {
          element.addEventListener("mouseenter", function (e) {
            const tooltipText = tooltips[className];
            tooltipElement.textContent = tooltipText;

            // ツールチップを表示
            tooltipElement.style.display = "block";
            tooltipElement.style.left = e.pageX + "px";
            tooltipElement.style.top = e.pageY + 20 + "px"; // マウスの少し下に表示
          });

          element.addEventListener("mouseleave", function () {
            // ツールチップを非表示
            tooltipElement.style.display = "none";
          });
        });
      } else {
        console.log(`Class: ${className} の要素は存在しません。`);
      }
    });
  });