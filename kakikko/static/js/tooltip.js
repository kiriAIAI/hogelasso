document.addEventListener("DOMContentLoaded", function () {
    const tooltips = {
        "bell-icon": "通知",
        "charge_img":"チャージ",
        "shopping-cart": "ショッピングカート",
        "account": "ログイン",
        "backButton": "戻る",
        "sidenavbar-search": "検索",
        "home": "ホーム",
        "sakusei": "投稿",
        "chat": "チャット",
        "rireki": "購入履歴",
        "profile": "プロフィール",
        "logout": "ログアウト",
        "button": "チャットボット",
        "dropZone": "画像をドロップ",
        "message-send-btn": "送信",
        "profile-edit-btn": "プロフィールを編集",
        "delete-btn": "投稿を削除",
        "fa-heart": "お気に入り",
        "Comment_Submission": "送信",
        "removeFromCart": "削除",
        "image": "画像を添付",
        "edit-btn": "編集",
    };

    const tooltipElement = document.createElement("div");
    tooltipElement.classList.add("tooltip");
    document.body.appendChild(tooltipElement);

    let currentTooltipElement = null;
    let isTooltipVisible = false;
    let tooltipTimeout = null;
    let isMouseOverElement = false;

    function showTooltip(element, tooltipText, position = 'right') {
        if (tooltipTimeout) {
            clearTimeout(tooltipTimeout);
            tooltipTimeout = null;
        }

        currentTooltipElement = element;
        tooltipElement.textContent = tooltipText;
        tooltipElement.style.display = "block";
        tooltipElement.style.opacity = "0";

        const rect = element.getBoundingClientRect();
        const viewportHeight = window.innerHeight;

        // 检查元素是否在视口内
        if (rect.top < 0 || rect.bottom > viewportHeight) {
            if (!isMouseOverElement) {
                hideTooltip();
            }
            return;
        }
        
        if (position === 'right') {
            tooltipElement.style.left = (rect.right + 15) + "px";
            tooltipElement.style.top = (rect.top + rect.height/2 - tooltipElement.offsetHeight/2) + "px";
            tooltipElement.classList.remove('chatbot-tooltip', 'top-tooltip');
        } else if (position === 'left') {
            tooltipElement.style.left = (rect.left - tooltipElement.offsetWidth - 15) + "px";
            tooltipElement.style.top = (rect.top + rect.height/2 - tooltipElement.offsetHeight/2) + "px";
            tooltipElement.classList.add('chatbot-tooltip');
            tooltipElement.classList.remove('top-tooltip');
        } else if (position === 'top') {
            tooltipElement.style.left = (rect.left + rect.width/2 - tooltipElement.offsetWidth/2) + "px";
            tooltipElement.style.top = (rect.top - tooltipElement.offsetHeight - 10) + "px";
            tooltipElement.classList.add('top-tooltip');
            tooltipElement.classList.remove('chatbot-tooltip');
        }

        requestAnimationFrame(() => {
            tooltipElement.style.opacity = "1";
            isTooltipVisible = true;
        });
    }

    function hideTooltip() {
        if (!isTooltipVisible || isMouseOverElement) return;
        
        tooltipElement.style.opacity = "0";
        isTooltipVisible = false;

        tooltipTimeout = setTimeout(() => {
            if (!isMouseOverElement) {
                tooltipElement.style.display = "none";
                currentTooltipElement = null;
            }
            tooltipTimeout = null;
        }, 200);
    }

    function getElement(identifier) {
        let element = document.getElementById(identifier);
        if (!element) {
            const elements = document.getElementsByClassName(identifier);
            if (elements.length > 0) {
                element = elements[0];
            }
        }
        return element;
    }

    // スクロールイベントの処理（デバウンス処理付き）
    let scrollTimeout;
    let lastScrollTop = window.pageYOffset || document.documentElement.scrollTop;
    
    document.addEventListener('scroll', () => {
        const currentScrollTop = window.pageYOffset || document.documentElement.scrollTop;
        const isScrollingDown = currentScrollTop > lastScrollTop;
        lastScrollTop = currentScrollTop;

        if (scrollTimeout) {
            clearTimeout(scrollTimeout);
        }

        if (isTooltipVisible && !isMouseOverElement) {
            hideTooltip();
        }

        scrollTimeout = setTimeout(() => {
            if (currentTooltipElement && isMouseOverElement) {
                const rect = currentTooltipElement.getBoundingClientRect();
                if (rect.top >= 0 && rect.bottom <= window.innerHeight) {
                    showTooltip(
                        currentTooltipElement, 
                        tooltips[currentTooltipElement.id || currentTooltipElement.className],
                        currentTooltipElement.id === 'button' ? 'left' : 
                        (currentTooltipElement.id === 'sidenavbar-search' || currentTooltipElement.className === 'image') ? 'top' : 'right'
                    );
                }
            }
        }, 100);
    });

    Object.keys(tooltips).forEach(identifier => {
        const element = getElement(identifier);
        if (element) {
            element.addEventListener("mouseenter", function () {
                isMouseOverElement = true;
                currentTooltipElement = element;
                showTooltip(element, tooltips[identifier], 
                    identifier === 'button' ? 'left' : 
                    identifier === 'image' ? 'right' : 'right'
                );
            });

            element.addEventListener("mouseleave", function () {
                isMouseOverElement = false;
                setTimeout(() => {
                    if (!isMouseOverElement) {
                        hideTooltip();
                    }
                }, 100);
            });
        }
    });
});

