from flask import Flask, render_template, send_from_directory, jsonify, request, redirect, url_for ,session
import mysql.connector

# import datetime
from datetime import timedelta


app = Flask(__name__, template_folder='kakikko')
app.permanent_session_lifetime = timedelta(days=5)

app.secret_key = 'kakikko'


def conn_db():
    conn = mysql.connector.connect(
        host="127.0.0.1", 
        user="root", 
        password="root", 
        db="kakikko",
        charset='utf8'
        )
    return conn



# 現在の日付と時刻を取得して、秒まで表示

def gettime():
    current_datetime = datetime.now() # type: ignore
    current_datetime_str = current_datetime.strftime('%Y-%m-%d %H:%M:%S')

    return current_datetime_str


@app.route('/get_account_id', methods=['GET'])
def get_account_id():
    account_id = "20000"  # 例として固定のIDを使用
    return jsonify({"account_id": account_id}), 200

@app.route('/')
@app.route('/index.html')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if not username or not email or not password or not confirm_password:
            error = "所有字段都是必填的"
            return render_template('register.html', error=error)
        
        if password != confirm_password:
            error = "密码不匹配"
            return render_template('register.html', error=error)
        
        # 检查用户名是否已存在
        con = conn_db()
        cur = con.cursor(buffered=True)
        sql = "SELECT * FROM users WHERE username = %s"
        cur.execute(sql, [username])
        existing_user = cur.fetchone()
        
        if existing_user:
            cur.close()
            con.close()
            error = "用户名已存在，请选择另一个用户名"
            return render_template('register.html', error=error)
        
        cur.close()
        con.close()
        
        return render_template('security-question.html', username=username, email=email, password=password)
    
    return render_template('register.html')

@app.route('/complete_registration', methods=['POST'])
def complete_registration():
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    question1 = request.form.get('question1')
    answer1 = request.form.get('answer1')
    question2 = request.form.get('question2')
    answer2 = request.form.get('answer2')

    con = conn_db()
    cur = con.cursor()
    
    try:
        sql = "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)"
        cur.execute(sql, [username, email, password])
        user_id = cur.lastrowid
        
        sql = "INSERT INTO user_security_questions (user_id, question1, answer1, question2, answer2) VALUES (%s, %s, %s, %s, %s)"
        cur.execute(sql, [user_id, question1, answer1, question2, answer2])
        
        con.commit()
    except Exception as e:
        con.rollback()
        error = "注册失败，请重试"
        return render_template('register.html', error=error)
    finally:
        cur.close()
        con.close()
    
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        if not username or not email or not password:
            error = "所有字段都是必填的"
            return render_template('login_form.html', error=error)

        con = conn_db()
        cur = con.cursor(buffered=True)
        sql = "SELECT * FROM users WHERE username = %s AND email = %s AND password = %s"
        cur.execute(sql, [username, email, password])
        user = cur.fetchone()
        cur.close()
        con.close()

        if user:
            session['login_id'] = user[0] # type: ignore
            session['login_name'] = user[1] # type: ignore
            return redirect(url_for('index'))
        else:
            error = "无效的用户名、邮箱或密码"
            return render_template('login.html', error=error)
    
    return render_template('login.html')

@app.route('/logout.html')
def logout():
    return render_template('logout.html')

@app.route('/create.html')
def create():
    return render_template('create.html')

@app.route('/chatroom.html')
def chatroom():
    return render_template('chatroom.html')

@app.route('/chat.html')
def chat():
    return render_template('chat.html')

@app.route('/chatbot.html')
def chatbot():
    return render_template('chatbot.html')



@app.route('/forget-password.html')
def forgetpassword():
    return render_template('forget-password.html')


@app.route('/confirm-logout.html')
def confirmlogout():
    return render_template('confirm-logout.html')

@app.route('/notification.html')
def notification():
    return render_template('notification.html')

@app.route('/filter.html')
def filter():
    return render_template('filter.html')


# product-details.html ページのレンダリング---------------------------------------------------
@app.route('/product-details.html')
def productdetails():
    return render_template('product-details.html')

@app.route('/submit_product-details', methods=['POST'])
def submit_data():
    # JSONデータの取得
    data = request.get_json()
    accountID = data.get('accountID')
    productID = data.get('productID')
    sellerID = '20000'
    # date = gettime()

    # データの表示（必要に応じてデータベースへの保存処理を追加）
    print(f'プロダクトID:{productID} , 購入者ID:{accountID} , 出品者ID:{sellerID}')
    
    conn = conn_db()
    cursor = conn.cursor()
    sql = ('''
    INSERT INTO transactions 
        (book_id, buyer_id, seller_id)
    VALUES 
        (%s, %s, %s)
    ''')

    data = [
       (productID, accountID, sellerID)
    ]

    cursor.executemany(sql, data)
    conn.commit()
    cursor.close()

    #支払い方法選択ページにリダイレクト
    print("paymentにリダイレクト")
    return redirect(url_for('payment',account=accountID,product=productID))
# --------------------------------------------------------------------------------------


@app.route('/search.html')
def search():
    return render_template('search.html')

@app.route('/shopping-cart.html')
def shoppingcart():
    return render_template('shopping-cart.html')

#--------------------------------------------------------------------------------------
@app.route('/payment')
def payment():
    return render_template('payment.html')

@app.route('/submit_payment', methods=['POST'])
def submit_data1():
    # JSONデータの取得
    data = request.get_json()
    description = data.get('description')
    print(description)
    
    accountID = request.args.get('account')
    print(accountID)
    return redirect(url_for('paymentinfo'))
    
#-------------------------------------------------------------------------------------
@app.route('/payment-info.html')
def paymentinfo():
    return render_template('payment-info.html')

@app.route('/payment-success.html')
def paymentsuccess():
    return render_template('payment-success.html')

@app.route('/profile.html')
def profile():
    return render_template('profile.html')

@app.route('/profile-info.html')
def profileinfo():
    return render_template('profile-info.html')

@app.route('/purchase-history.html')
def purchase_history():
    return render_template('purchase-history.html')

@app.route('/read.html')
def read():
    return render_template('read.html')




@app.route('/quiz.html')
def quiz():
    conn = conn_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT question_text, option1, option2, option3, option4 FROM questions ORDER BY RAND() LIMIT 1")
    question = cursor.fetchone()
    cursor.close()
    conn.close()
    
    if question is None:
        question = {
            'question_text': 'No question available',
            'option1': 'Option 1',
            'option2': 'Option 2',
            'option3': 'Option 3',
            'option4': 'Option 4'
        }
    
    return render_template('quiz.html', question=question)





@app.route('/static/css/<path:filename>')
def css(filename):
    return send_from_directory('kakikko/static/css', filename)

@app.route('/static/js/<path:filename>')
def js(filename):
    return send_from_directory('kakikko/static/js', filename)

@app.route('/static/fonts/<path:filename>')
def fonts(filename):
    return send_from_directory('kakikko/static/fonts', filename)

@app.route('/static/images/<path:filename>')
def images(filename):
    return send_from_directory('kakikko/static/images', filename)




if __name__ == '__main__':
    app.run(debug=True)