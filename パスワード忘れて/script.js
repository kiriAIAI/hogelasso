document.getElementById('forgot-password-form').addEventListener('submit', function(event) {
    event.preventDefault();
    var email = document.getElementById('email').value;
    var message = document.getElementById('message');

    // 这里可以添加实际的忘记密码逻辑，例如发送请求到服务器
    if (email) {
        message.textContent = '重置密码的链接已发送到您的邮箱。';
        message.style.color = 'green';
    } else {
        message.textContent = '请输入有效的邮箱地址。';
    }
});
