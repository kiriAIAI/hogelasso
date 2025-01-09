from flask import Flask, render_template, send_from_directory, jsonify, request, redirect, url_for ,session ,flash
import mysql.connector
import os

from werkzeug.utils import secure_filename

# import datetime
from datetime import timedelta
import random


app = Flask(__name__, template_folder='kakikko')
app.permanent_session_lifetime = timedelta(days=7)

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

def saveToDatabase(sql,data):
    try:
        conn = conn_db()
        cursor = conn.cursor()
        cursor.executemany(sql, data)
        conn.commit()
    except:
        print("データベースへの保存中にエラーが発生しました。")
    finally:
        cursor.close()
        
def checkForDuplicateEntry(sql,data):
    conn = conn_db()
    cursor = conn.cursor()
    cursor.execute(sql, data)
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result

def update_database(where,Updated_value,sql):
    conn = conn_db()
    cursor = conn.cursor()
    cursor.execute(sql, (Updated_value, where))
    conn.commit()
    cursor.close()
    conn.close()


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



# -------------------- category.html --------------------
@app.route('/category/<category>')
def category(category):
    if 'login_id' not in session:
        return redirect(url_for('login'))
        
    try:
        # カテゴリー名の対応表
        category_names = {
            'literature': '文学・評論',
            'social': '社会・政治',
            'history': '歴史・地理',
            'business': 'ビジネス・経済',
            'science': '科学・テクノロジー',
            'medical': '医学・薬学',
            'it': 'コンピュータ・IT',
            'design': '建築・デザイン',
            'hobby': '趣味・実用',
            'sports': 'スポーツ',
            'certification': '資格・検定',
            'lifestyle': '暮らし・健康'
        }
        
        conn = conn_db()
        cursor = conn.cursor(dictionary=True)
        
        # カテゴリーに属する書籍を取得
        cursor.execute("""
            SELECT b.*, u.username as owner_name
            FROM books b
            JOIN users u ON b.owner_id = u.id
            WHERE b.book_category = %s
            ORDER BY b.book_id DESC
        """, (category,))
        books = cursor.fetchall()
        
        return render_template('category.html', 
                             books=books,
                             category_name=category_names.get(category, 'Unknown Category'))
        
    except Exception as e:
        print(f"Error: {e}")
        return render_template('category.html', books=[], category_name='Error')
        
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()



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
            error = "無効なユーザー名、メ���ルアドレス、パスワード"
            return render_template('login.html', error=error)
    
    return render_template('login.html')



# -------------------- logout.html --------------------
@app.route('/logout.html')
def logout():
    session.pop('login_id', None)  # 清除用户的会话信息
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
    conn = conn_db()
    cursor = conn.cursor()
        
    cursor.execute('SELECT book_id FROM books ORDER BY book_id DESC LIMIT 1')
    latest_book_id = cursor.fetchone() # 取得した結果を表示 
    
    app.config['UPLOAD_FOLDER'] = 'kakikko/static/images/users_images'
    file = request.files['image_data']
    file_name = f"{latest_book_id[0]}_{file.filename}" # type: ignore
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file_name) # type: ignore
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
        if not cover_image:
            return jsonify({'message': '表紙画像をアップロードしてください'}), 400
        
        
        # # base64データの場合は、有効なフォーマットであることを確認する
        # if cover_image.startswith('data:image'):
        #     pass
        # else:
        #     return jsonify({'message': '無効な画像形式です'}), 400

        # データ挿入
        conn = conn_db()
        cursor = conn.cursor()
        
        cursor.execute('SELECT book_id FROM books ORDER BY book_id DESC LIMIT 1')
        latest_book_id = cursor.fetchone() # 取得した結果を表示 
        cover_image = f"{latest_book_id[0] + 1}_{cover_image}" # type: ignore
            
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

# -------------------- 投稿の削除 --------------------
@app.route('/delete_post/<int:book_id>', methods=['POST'])
def delete_post(book_id):
    if 'login_id' not in session:
        return jsonify({'message': 'ログインしてください'}), 401

    conn = None
    cursor = None
    try:
        conn = conn_db()
        cursor = conn.cursor()
        
        # 現在のログインユーザーが投稿者であることを確認
        cursor.execute("SELECT owner_id FROM books WHERE book_id = %s", (book_id,))
        result = cursor.fetchone()
        if not result or result[0] != session['login_id']:
            return jsonify({'message': '権限がありません'}), 403

        # book_id に依存するコメントを削除
        delete_comments_sql = "DELETE FROM comments WHERE book_id = %s"
        cursor.execute(delete_comments_sql, (book_id,))
        
        # 書籍レコードを削除
        delete_books_sql = "DELETE FROM books WHERE book_id = %s"
        cursor.execute(delete_books_sql, (book_id,))
        conn.commit()
        
        return jsonify({'message': '投稿が削除されました'}), 200
        
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

@app.route('/send_message', methods=['POST'])
def send_message():
    sender_id = session.get('login_id')
    if not sender_id:
        return jsonify({'error': 'User not logged in'}), 401

    data = request.get_json()
    recipient_id = 1  # 默认用户ID
    message = data['message']

    connection = conn_db()
    cursor = connection.cursor()
    cursor.execute('INSERT INTO direct_messages (sender_id, recipient_id, message) VALUES (%s, %s, %s)',
                   (sender_id, recipient_id, message))
    connection.commit()
    cursor.close()
    connection.close()

    return jsonify({'success': 'Message sent'})

@app.route('/get_messages', methods=['GET'])
def get_messages():
    sender_id = session.get('login_id')
    if not sender_id:
        return jsonify({'error': 'User not logged in'}), 401

    recipient_id = 1  # 默认用户ID

    connection = conn_db()
    cursor = connection.cursor()
    cursor.execute('''
        SELECT dm.sender_id, u.username, dm.message, dm.timestamp
        FROM direct_messages dm
        JOIN users u ON dm.sender_id = u.id
        WHERE dm.recipient_id = %s
        ORDER BY dm.timestamp ASC
    ''', (recipient_id,))
    messages = cursor.fetchall()
    cursor.close()
    connection.close()

    # 将数据转换为字典列表
    messages_list = [{'sender_id': msg[0], 'username': msg[1], 'message': msg[2], 'timestamp': msg[3].strftime('%Y-%m-%d %H:%M:%S')} for msg in messages]

    return jsonify(messages_list)


# -------------------- chat.html --------------------
@app.route('/chat.html')
def chat():
    return render_template('chat.html')



# -------------------- chatbot.html --------------------
@app.route('/chatbot.html')
def chatbot():
    return render_template('chatbot.html')




#---------------------F&A.html--------------------
@app.route('/Q&A.html')
def  QandA():
    return render_template('qanda.html')


# -------------------- forget-password.html --------------------
@app.route('/forget-password.html')
def forgetpassword():
    return render_template('forget-password.html')



# -------------------- confirm-logout.html --------------------
@app.route('/confirm-logout.html')
def confirmlogout():
    return render_template('confirm-logout.html')



# -------------------- notification.html --------------------
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
        
        # 書籍情報入手
        cursor.execute("""
            SELECT b.*, u.username 
            FROM books b 
            JOIN users u ON b.owner_id = u.id 
            WHERE b.book_id = %s
        """, (book_id,))
        book = cursor.fetchone()
        if not book:
            return redirect(url_for('index'))
        
        #コメント情報入手
        cursor.execute("""
            SELECT c.*, u.username 
            FROM comments c
            JOIN users u ON c.user_id = u.id 
            WHERE c.book_id = %s
            ORDER BY c.timestamp DESC
            LIMIT 6
        """, (book_id,))
        comments = cursor.fetchall()
        comment_data = [{
            'comment': comment['comment'], # type: ignore
            'created_at': comment['timestamp'], # type: ignore
            'username': comment['username'] # type: ignore
        } for comment in comments]
        

        
        # 現在のユーザーが本の所有者かどうかをチェックする
        is_owner = book['owner_id'] == session['login_id'] # type: ignore
        
        # 現在のユーザーが本を購入したかどうかをチェックする
        cursor.execute("""
            SELECT COUNT(*) as count
            FROM transactions
            WHERE book_id = %s AND buyer_id = %s
        """, (book_id, session['login_id']))
        purchase_info = cursor.fetchone()
        is_purchased = purchase_info['count'] > 0 # type: ignore
        
        return render_template('product-details.html', 
                             book=book,
                             comments=comment_data,
                             username=book['username'], # type: ignore
                             is_owner=is_owner,
                             is_purchased=is_purchased)
                             
    except Exception as e:
        print(f"Error: {e}")
        return redirect(url_for('index'))
        
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()



# -------------------- カートに入れる処理 --------------------
@app.route('/addToCart', methods=['POST'])
def addToCart():
    accountID = session['login_id'] #セッションデータの取得
    data = request.get_json() # JSONデータの取得
    productID = int(data.get('productID'))

    print("カートに入れる処理")
    print(f'購入者ID:{accountID} , プロダクトID:{productID}') # 取得できたデータを表示
    
    #カート内に同じ商品がないかチェック
    check_sql = '''
    SELECT COUNT(*) FROM shopping_cart 
    WHERE user_id = %s AND book_id = %s AND quantity = 0
    '''
    check_data = (accountID, productID)
    result = checkForDuplicateEntry(check_sql,check_data)
    if result[0] > 0: # type: ignore
        print("エラー:すでに同じ商品が入っています")
        return redirect(url_for("shoppingcart"))

    check_sql1 = '''
    SELECT COUNT(*) FROM shopping_cart 
    WHERE user_id = %s AND book_id = %s AND quantity = 3
    '''
    check_data = (accountID, productID)
    result = checkForDuplicateEntry(check_sql1,check_data)
    if result[0] > 0: # type: ignore
        print("エラー:すでにアイテムが購入されています")
        return redirect(url_for("shoppingcart"))
    
    
    # 取得できたデータを保存
    sql = ('''
    INSERT INTO shopping_cart
        (user_id,book_id,quantity)
    VALUES 
        (%s, %s,%s)
    ''')
    data = [
       (accountID,productID,0)
    ]
    saveToDatabase(sql,data)

    print("ショッピングカートページにリダイレクト")
    return redirect(url_for('shoppingcart'))


# -------------------- 今すぐ購入の処理 --------------------
@app.route('/submit_product-details', methods=['POST'])
def submit_data():
    accountID = session['login_id']
    data = request.get_json()
    sellerID = int(data.get('sellerID'))
    productID = int(data.get('productID'))

    print("今すぐ購入の処理")
    print(f'プロダクトID:{productID} , 購入者ID:{accountID} , 出品者ID:{sellerID}')
    
    sql = ('''
    INSERT INTO transactions 
        (book_id, buyer_id, seller_id)
    VALUES 
        (%s, %s, %s)
    ''')
    data = [
       (productID, accountID, sellerID)
    ]
    saveToDatabase(sql,data)

    print("paymentにリダイレクト")
    return redirect(url_for('payment',account=accountID,product=productID))


#----------------------------- 商品につけるコメントの処理 --------------------------
@app.route('/submit_product-comment', methods=['POST'])
def submit_comment():
    accountID = session['login_id']
    data = request.get_json()
    maintxt = data.get('maintxt')
    productID = int(data.get('productID'))

    print("コメントの投稿")
    print(f'プロダクトID:{productID} , コメント投稿者ID:{accountID} , 本文:{maintxt}')
    
    sql = ('''
        INSERT INTO comments (user_id, book_id, comment)
        VALUES (%s, %s, %s)
        ''')
    data = [
       (accountID,productID,maintxt)
    ]
    saveToDatabase(sql,data)
    
    return redirect(url_for('product_details',book_id=productID))
    


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
        
        # Get user points
        cursor.execute("""
            SELECT points 
            FROM users 
            WHERE id = %s
        """, (session['login_id'],))
        user_points = cursor.fetchone()['points'] # type: ignore
        
        query = """
        SELECT 
            sc.cart_id, 
            sc.user_id, 
            sc.book_id, 
            b.book_title,
            b.book_price,
            b.book_cover_image 
        FROM 
            shopping_cart sc
        JOIN 
            books b
        ON 
            sc.book_id = b.book_id
        WHERE 
            sc.user_id = %s AND sc.quantity = 0
        ORDER BY 
            sc.cart_id DESC;
        """
        cursor.execute(query,  (session['login_id'],))
        cart_items = cursor.fetchall()
        
        total_items = len(cart_items)
        total_price = sum(item['book_price'] for item in cart_items) # type: ignore
        
        return render_template(
            'shopping-cart.html', 
            cart_items=cart_items,
            total_items=total_items,
            total_price=total_price,
            user_points=user_points
        )
        
    except Exception as e:
        print(f"Error: {e}")
        return render_template('shopping-cart.html', cart_items=[])
        
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


# -------------------- カート内のアイテムの削除 --------------------
@app.route('/remove-shopping-cart', methods=['POST'])
def remove_from_cart():
    cart_id = request.form.get('cart_id')
    sql = "UPDATE shopping_cart SET quantity = %s WHERE cart_id = %s"
    update_database(cart_id,1,sql)
    
    return redirect(url_for('shoppingcart'))


# -------------------- カート内のアイテムを購入 --------------------
@app.route('/proceedToCheckout',methods=['GET']) # type: ignore
def proceedToCheckout():
    try:
        accountID = session['login_id']
        conn = conn_db()
        cursor = conn.cursor()

        # カートに入っている商品のIDを取得
        query1 = """
        SELECT book_id 
        FROM shopping_cart 
        WHERE user_id = %s AND quantity = '0'
        """
        cursor.execute(query1, (str(accountID),))
        books = cursor.fetchall()

        # 商品がカートにない場合、ショッピングカートページに���ダイレクト
        if not books:
            print("商品がありません")
            flash('カート内に商品がありません')
            return redirect(url_for('shoppingcart'))

        # book_idsリストを作成
        book_ids = [str(book[0]) for book in books] # type: ignore

        # 商品IDからオーナーIDを取得
        query2 = """
        SELECT book_id, owner_id 
        FROM books 
        WHERE book_id IN (%s)
        """ % (", ".join(["%s"] * len(book_ids)))

        cursor.execute(query2, book_ids)
        owners = cursor.fetchall()

        print("カート内のアイテム(book_id, owner_id)", owners)

        # トランザクションテーブルにデータを挿入
        sql = '''
        INSERT INTO transactions (book_id, buyer_id, seller_id)
        VALUES (%s, %s, %s)
        '''
        
        # 各オーナーに対してデータを挿入
        for owner in owners:
            book_id = owner[0] # type: ignore
            seller_id = owner[1] # type: ignore

            cursor.execute(sql, (book_id, accountID, seller_id)) # type: ignore
            
            #アイテムを購入済みに更新
            update_query = """
            UPDATE shopping_cart
            SET quantity = 3
            WHERE book_id = %s AND user_id = %s
            """
            cursor.execute(update_query, (book_id, accountID)) # type: ignore

        conn.commit()
        return redirect(url_for('payment'))

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        conn.rollback()  # エラーが発生した場合はロールバック

    finally:
        cursor.close()
        conn.close()

@app.route('/toggle-favorite', methods=['POST'])
def toggle_favorite():
    if 'user_id' not in session:
        return jsonify({'error': 'ログインが必要です'}), 401
        
    data = request.get_json()
    book_id = data.get('book_id')
    user_id = session['user_id']
    
    conn = conn_db()
    cursor = conn.cursor()
    
    # 检查是否已经收藏
    cursor.execute('''
        SELECT favorite_id FROM favorites 
        WHERE user_id = %s AND book_id = %s
    ''', (user_id, book_id))
    existing_favorite = cursor.fetchone()
    
    if existing_favorite:
        # 如果已收藏，则取消收藏
        cursor.execute('''
            DELETE FROM favorites 
            WHERE user_id = %s AND book_id = %s
        ''', (user_id, book_id))
        status = 'removed'
    else:
        # 如果未收藏，则添加收藏
        cursor.execute('''
            INSERT INTO favorites (user_id, book_id)
            VALUES (%s, %s)
        ''', (user_id, book_id))
        status = 'added'
    
    conn.commit()
    cursor.close()
    conn.close()
    
    return jsonify({'status': status})

    

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
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    print(session)
    if not session or not session.get('login_id'):
        return redirect(url_for('login', _external=True))

    try:
        conn = conn_db()
        cursor = conn.cursor(dictionary=True)

        # user_profilesテーブルにuser_idが存在するかチェック
        cursor.execute("""
            SELECT * FROM user_profiles 
            WHERE user_id = %s
        """, (session['login_id'],))
        existing_profile = cursor.fetchone()
        print(f"existingprofile {existing_profile}")
        
        # プロファイルが存在しない場合、新しい行を追加
        if existing_profile is None:
            try:
                cursor.execute("""
                    INSERT INTO user_profiles (user_id, profile_image, first_name, last_name, bio)
                    VALUES (%s, %s, %s, %s, %s)
                """, (session['login_id'], 'default-profile.jpg', None, None, None))
                conn.commit()
                print(f"新しいプロファイルを作成しました: {session['login_id']}")
            except Exception as e:
                conn.rollback()
                print(f"プロファイル作成エラー: {e}")

        if request.method == 'POST':
            print("POST request received.")
            # プロフィール画像アップロード処理
            if 'profile_image' in request.files:
                file = request.files.get('profile_image')
                first_name = request.form.get('Name')
                last_name = request.form.get('name-2')
                bio = request.form.get('Bio')
                
                if file:
                    upload_folder = 'kakikko/static/images/profiles_images'

                    # アップロードフォルダ内のファイルを調べる
                    for existing_file in os.listdir(upload_folder):
                        # ファイル名の最初の"/"以前の文字列を取得
                        print(f"existion_file{existing_file}")
                        existing_filename = existing_file.split('_')[:2]
                        existing_filename = "_".join(existing_filename)  # user_100000の形式に変換
                        print(f"split{existing_filename}")
                        # 一致する場合はファイルを削除
                        if existing_filename == secure_filename(f"user_{session['login_id']}"):
                            file_to_delete = f"{upload_folder}/{existing_file}"
                            try:
                                os.remove(file_to_delete)
                                print(f"Deleted file: {file_to_delete}")
                            except Exception as e:
                                print(f"Failed to delete file: {e}")
                                
                    filename = f"user_{session['login_id']}_{secure_filename(file.filename)}" # type: ignore
                    file_path = f"{upload_folder}/{filename}"
                    try:
                        file.save(file_path)  # file_pathに、fileを保存
                        print(f"File saved successfully: {file_path}")
                    except Exception as e:
                        print(f"Failed to save file: {e}")
                        return f"File upload failed: {str(e)}", 500

                    try:
                        # データベースに画像パスを保存
                        cursor.execute("""
                            INSERT INTO user_profiles (user_id, profile_image, first_name, last_name, bio)
                            VALUES (%s, %s, %s, %s, %s)
                            ON DUPLICATE KEY UPDATE profile_image = %s, first_name = %s, last_name = %s, bio = %s
                        """, (session['login_id'], filename, first_name, last_name, bio, filename, first_name, last_name, bio))
                        conn.commit()
                    except Exception as e:
                        conn.rollback()
                        return "Database error", 500

        # プロフィール情報取得
        print(f"Fetching profile for user_id: {session['login_id']}")
        cursor.execute("""
            SELECT u.username, up.profile_image, up.first_name, up.last_name, up.bio
            FROM users u
            LEFT JOIN user_profiles up ON u.id = up.user_id
            WHERE u.id = %s
        """, (session['login_id'],))
        user_info = cursor.fetchone()

        # ユーザーがお気に入りした本を取得
        cursor.execute("""
            SELECT b.book_id, b.book_title, b.book_price, b.book_cover_image
            FROM favorites f
            JOIN books b ON f.book_id = b.book_id
            WHERE f.user_id = %s
        """, (session['login_id'],))
        favorite_books = cursor.fetchall()


        return render_template('profile.html', user_info=user_info, favorite_books=favorite_books)
    
    finally:
        cursor.close()
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
        ORDER BY book_id DESC
        """
        cursor.execute(listed_books_sql, (login_id,))
        listed_books = cursor.fetchall()
       
        # ユーザーが購入した本
        purchased_books_sql = """
        SELECT t.book_id, b.book_title, b.book_content, b.book_price, b.book_cover_image
        FROM transactions t
        JOIN books b ON t.book_id = b.book_id
        WHERE t.buyer_id = %s
        ORDER BY book_id DESC
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
@app.route('/read.html/<int:book_id>')
def read(book_id):
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
            return redirect(url_for('purchase_history'))
            
        return render_template('read.html', book=book)
        
    except Exception as e:
        print(f"Error: {e}")
        return redirect(url_for('purchase_history'))
        
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()



# -------------------- quiz.html --------------------
@app.route('/quiz/<int:book_id>')
def quiz(book_id):
    if 'login_id' not in session:
        return redirect(url_for('login'))
    
    # Generate random question
    question, correct_answer, options = generate_question()
    
    return render_template('quiz.html',
                         question=question,
                         options=options,
                         correct_answer=correct_answer,
                         book_id=book_id)

def generate_question():
    # Generate random numbers and operation
    num1 = random.randint(1, 50)
    num2 = random.randint(1, 100)
    operations = ['+', '-', '*', '/']
    operation = random.choice(operations)
    
    # Ensure clean division for division operations
    if operation == '/':
        num1 = num1 * num2  # Makes sure result is whole number
        
    # Create question string
    question = f"{num1} {operation} {num2}"
    
    # Calculate correct answer
    correct_answer = str(int(eval(question)))
    
    # Generate wrong options
    options = [correct_answer]
    while len(options) < 4:
        # Generate wrong answer by slightly modifying num2
        offset = random.randint(-5, 5)
        if offset != 0:  # Avoid generating the correct answer
            try:
                if operation == '/':
                    wrong_num = num1 / (num2 + offset)
                else:
                    wrong_num = eval(f"{num1} {operation} {num2 + offset}")
                wrong_answer = str(int(wrong_num))
                if wrong_answer not in options:  # Avoid duplicates
                    options.append(wrong_answer)
            except:
                continue
    
    # Shuffle options
    random.shuffle(options)
    
    return question, correct_answer, options

@app.route('/submit_quiz', methods=['POST'])
def submit_quiz():
    if 'login_id' not in session:
        return redirect(url_for('login'))
    
    selected_option = request.form.get('option')
    correct_answer = request.form.get('correct_answer')
    book_id = request.form.get('book_id')

    # Check if answer is correct
    is_correct = selected_option == correct_answer
    
    # Update points if answer is correct
    if is_correct and 'login_id' in session:
        try:
            conn = conn_db()
            cursor = conn.cursor()
            
            # 先获取当前积分
            cursor.execute("SELECT points FROM users WHERE id = %s", (session['login_id'],))
            current_points = cursor.fetchone()[0] or 0 # type: ignore
            
            # 增加2点积分
            new_points = current_points + 2 # type: ignore
            cursor.execute("UPDATE users SET points = %s WHERE id = %s", 
                         (new_points, session['login_id']))
            conn.commit()
            
        except Exception as e:
            print(f"Error updating points: {e}")
            conn.rollback()
            
        finally:
            cursor.close()
            conn.close()

    return redirect(url_for('read', book_id=book_id))



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