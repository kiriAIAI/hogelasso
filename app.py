from flask import Flask, render_template, send_from_directory, jsonify, request, redirect, url_for ,session
import mysql.connector

import datetime

app = Flask(__name__, template_folder='kakikko')

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
    account_id = "123456"  # 例として固定のIDを使用
    return jsonify({"account_id": account_id}), 200

@app.route('/')
@app.route('/index.html')
def index():
    conn = conn_db()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("""
        SELECT b.book_id, b.book_title, b.book_price, b.book_cover_image,
               u.username as owner_name
        FROM books b
        JOIN users u ON b.owner_id = u.id
        ORDER BY b.book_id DESC 
        LIMIT 6
    """)
    books = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return render_template('index.html', books=books)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if not username or not email or not password or not confirm_password:
            error = "すべての項目は必須です"
            return render_template('register.html', error=error)
        
        if password != confirm_password:
            error = "パスワード不一致"
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
            error = "ユーザー名はすでに存在します"
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
        error = "登録に失敗しました、もう一度お試しください"
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
            error = "すべての項目は必須です"
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
            error = "無効なユーザー名、メールアドレス、パスワード"
            return render_template('login.html', error=error)
    
    return render_template('login.html')

@app.route('/logout.html')
def logout():
    return render_template('logout.html')

@app.route('/create.html')
def create():
    return render_template('create.html')

@app.route('/submit_create', methods=['POST'])
def submit_create():
    if 'login_id' not in session:
        return jsonify({'message': 'ログインしてください'}), 401
        
    conn = None
    cursor = None
    try:
        data = request.get_json()
        
        # 验证图片数据
        cover_image = data.get('cover_image_path', '')
        if not cover_image:
            return jsonify({'message': '表紙画像をアップロードしてください'}), 400
            
        # 如果是 base64 数据，确保它是有效的格式
        if cover_image.startswith('data:image'):
            # 可以选择在这里进行额外的图片验证
            pass
        else:
            return jsonify({'message': '無効な画像形式です'}), 400

        # 插入数据
        conn = conn_db()
        cursor = conn.cursor()
        
        insert_sql = """
        INSERT INTO books (
            book_title,
            book_content,
            book_category,
            book_price,
            book_cover_image,
            owner_id
        ) VALUES (%s, %s, %s, %s, %s, %s)
        """
        
        values = [
            data['title'],
            data['content'],
            data['category'],
            float(data['price']),
            cover_image,
            session['login_id']
        ]
        
        cursor.execute(insert_sql, values)
        book_id = cursor.lastrowid
        conn.commit()
        
        return jsonify({
            'message': '成功',
            'book_id': book_id
        }), 200
        
    except mysql.connector.Error as e:
        print(f"Database error: {e}")
        if conn:
            conn.rollback()
        return jsonify({'message': f'データベースエラー: {str(e)}'}), 500
        
    except Exception as e:
        print(f"Error: {e}")
        if conn:
            conn.rollback()
        return jsonify({'message': f'エラー: {str(e)}'}), 500
        
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

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


@app.route('/product-details/<int:book_id>')
def product_details(book_id):
    if 'login_id' not in session:
        return redirect(url_for('login'))
        
    try:
        conn = conn_db()
        cursor = conn.cursor(dictionary=True)
        
        # 获取书籍信息
        cursor.execute("""
            SELECT b.*, u.username 
            FROM books b 
            JOIN users u ON b.owner_id = u.id 
            WHERE b.book_id = %s
        """, (book_id,))
        book = cursor.fetchone()
        
        if not book:
            return redirect(url_for('index'))
            
        return render_template('product-details.html', 
                             book=book,
                             username=book['username'])
                             
    except Exception as e:
        print(f"Error: {e}")
        return redirect(url_for('index'))
        
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


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