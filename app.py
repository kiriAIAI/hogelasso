from flask import Flask, render_template, send_from_directory, jsonify, request, redirect, url_for ,session
import mysql.connector
import os

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



# -------------------- index.html --------------------
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
    # print("login_idを表示")
    # print(session['login_id'])
    
    return render_template('index.html', books=books)



# -------------------- register.html --------------------
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
        
        # ユーザー名が既に存在するかどうかをチェックする
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



# -------------------- complete_registration.html --------------------
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



# -------------------- login.html --------------------
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
            print("login_idを更新")
            print(session['login_id'])
            session['login_name'] = user[1] # type: ignore
            return redirect(url_for('index'))
        else:
            error = "無効なユーザー名、メールアドレス、パスワード"
            return render_template('login.html', error=error)
    
    return render_template('login.html')



# -------------------- logout.html --------------------
@app.route('/logout.html')
def logout():
    session.pop('user_id', None)  # 清除用户的会话信息
    return render_template('logout.html')  # 渲染登出页面

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html')





# -------------------- create.html --------------------
@app.route('/create.html')
def create():
    return render_template('create.html')


@app.route('/image_upload', methods=['POST'])
def image_upload():
    app.config['UPLOAD_FOLDER'] = 'kakikko/static/images/users_images'
    file = request.files['image_data']
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename) # type: ignore
    file.save(file_path)
    
    return jsonify({'message': '画像をアップロードしました'}), 200

# -------------------- submit_create.html --------------------
@app.route('/submit_create', methods=['POST'])
def submit_create():
    if 'login_id' not in session:
        return jsonify({'message': 'ログインしてください'}), 401
        
    conn = None
    cursor = None
    try:
        
        data = request.get_json()
        # print(request.files['image_data'])
        # 画像データを検証
        cover_image = data.get('cover_image_path', '')
        print(cover_image)
        if not cover_image:
            return jsonify({'message': '表紙画像をアップロードしてください'}), 400
           
        # app.config['UPLOAD_FOLDER'] = 'kakikko/static/images'
        # file = request.files['Image_data']
        # file_path = os.path.join(app.config['UPLOAD_FOLDER'], cover_image)
        # file.save(file_path)
         
        # # base64データの場合は、有効なフォーマットであることを確認する
        # if cover_image.startswith('data:image'):
        #     pass
        # else:
        #     return jsonify({'message': '無効な画像形式です'}), 400

        # データ挿入
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



# -------------------- chatroom.html --------------------
@app.route('/chatroom.html')
def chatroom():
    return render_template('chatroom.html')



# -------------------- chat.html --------------------
@app.route('/chat.html')
def chat():
    return render_template('chat.html')

@app.route('/chatbot.html')
def chatbot():
    return render_template('chatbot.html')



# -------------------- forget-password.html --------------------
@app.route('/forget-password.html')
def forgetpassword():
    return render_template('forget-password.html')



# -------------------- confirm-logout.html --------------------
@app.route('/confirm-logout.html')
def confirmlogout():
    return render_template('confirm-logout.html')

@app.route('/notification.html')
def notification():
    return render_template('notification.html')



# -------------------- filter.html --------------------
@app.route('/filter.html')
def filter():
    if 'login_id' not in session:
        return redirect(url_for('login'))
        
    try:
        conn = conn_db()
        cursor = conn.cursor(dictionary=True)
        
        # すべての書籍
        cursor.execute("""
            SELECT b.*, u.username as owner_name
            FROM books b
            JOIN users u ON b.owner_id = u.id
            ORDER BY b.book_id DESC
        """)
        books = cursor.fetchall()
        
        return render_template('filter.html', books=books)
        
    except Exception as e:
        print(f"Error: {e}")
        return render_template('filter.html', books=[])
        
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()



# -------------------- product-details.html --------------------
@app.route('/product-details/<int:book_id>')
def product_details(book_id):
    if 'login_id' not in session:
        return redirect(url_for('login'))
        
    try:
        conn = conn_db()
        cursor = conn.cursor(dictionary=True)
        
        # 書籍情報を入手
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
                             username=book['username']) # type: ignore
                             
    except Exception as e:
        print(f"Error: {e}")
        return redirect(url_for('index'))
        
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# --------------------------------------------------------------------------------------

@app.route('/submit_product-details', methods=['POST'])
def submit_data():
    # JSONデータの取得
    data = request.get_json()
    sellerID = int(data.get('sellerID'))
    productID = int(data.get('productID'))
    
    #sessionの情報を取得
    accountID = session['login_id']

    # 取得できたデータを表示
    print(f'プロダクトID:{productID} , 購入者ID:{accountID} , 出品者ID:{sellerID}')
    
    # 取得できたデータを保存
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


# -------------------- search.html --------------------
@app.route('/search.html')
def search():
    return render_template('search.html')



# -------------------- shopping-cart.html --------------------
@app.route('/shopping-cart.html')
def shoppingcart():
    if 'login_id' not in session:
        return redirect(url_for('login'))
        
    try:
        conn = conn_db()
        cursor = conn.cursor(dictionary=True)
        
        # ショッピングカートに商品を入れる
        cursor.execute("""
            SELECT b.*, c.quantity 
            FROM cart c
            JOIN books b ON c.book_id = b.book_id
            WHERE c.user_id = %s
        """, (session['login_id'],))
        cart_items = cursor.fetchall()
        
        return render_template('shopping-cart.html', cart_items=cart_items)
        
    except Exception as e:
        print(f"Error: {e}")
        return render_template('shopping-cart.html', cart_items=[])
        
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()



# -------------------- payment.html --------------------
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



# -------------------- payment-info.html --------------------
@app.route('/payment-info.html')
def paymentinfo():
    return render_template('payment-info.html')



# -------------------- payment-success.html --------------------
@app.route('/payment-success.html')
def paymentsuccess():
    return render_template('payment-success.html')



# -------------------- profile.html --------------------
@app.route('/profile')
def profile():
    if 'login_id' not in session:
        return redirect(url_for('login'))

    try:
        conn = conn_db()
        cursor = conn.cursor(dictionary=True)
        
        # ユーザー情報の取得
        cursor.execute("""
            SELECT username, email, profile_image, bio
            FROM users 
            WHERE id = %s
        """, (session['login_id'],))
        
        user_info = cursor.fetchone()
        
        if not user_info:
            return redirect(url_for('login'))
            
        return render_template('profile.html', 
                             username=user_info['username'],  # ユーザー名をテンプレートに渡す # type: ignore
                             user_info=user_info)
                             
    except Exception as e:
        print(f"Error: {e}")
        return redirect(url_for('login'))
        
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()



# -------------------- profile-info.html --------------------
@app.route('/profile-info.html')
def profileinfo():
    return render_template('profile-info.html')



# -------------------- purchase-history.html --------------------
@app.route('/purchase-history.html')
def purchase_history():
    if 'login_id' not in session:
        return redirect(url_for('login'))
    else :
        login_id = str(session.get('login_id'))
    print("現ユーザーID:", login_id)
        
    try:
        conn = conn_db()
        cursor = conn.cursor(dictionary=True)
        
        # ユーザーが出品した本
        listed_books_sql =  """
        SELECT book_id, book_title, book_content, book_price, book_cover_image
        FROM books
        WHERE owner_id = %s
        """
        cursor.execute(listed_books_sql, (login_id,))
        listed_books = cursor.fetchall()
        
        # ユーザーが購入した本
        purchased_books_sql = """
        SELECT t.book_id, b.book_title, b.book_content, b.book_price, b.book_cover_image
        FROM transactions t
        JOIN books b ON t.book_id = b.book_id
        WHERE t.buyer_id = %s
        """
        cursor.execute(purchased_books_sql, (login_id,))
        purchased_books = cursor.fetchall()
        
        return render_template('purchase-history.html', 
                             purchased_books=purchased_books,
                             listed_books=listed_books)
                             
    except Exception as e:
        print("Error:", e)
        import traceback
        traceback.print_exc()
        return render_template('purchase-history.html', 
                             purchased_books=[],
                             listed_books=[])
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()



# -------------------- read.html --------------------
@app.route('/read.html')
def read():
    return render_template('read.html')



# -------------------- quiz.html --------------------
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





# -------------------- static --------------------
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