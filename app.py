from flask import Flask, render_template, send_from_directory, jsonify, request, redirect, url_for ,session ,flash
import mysql.connector
import os

from werkzeug.utils import secure_filename

from datetime import timedelta
import random


app = Flask(__name__, template_folder='kakikko')
app.permanent_session_lifetime = timedelta(days=7)

app.secret_key = 'kakikko'


def conn_db():
    conn = mysql.connector.connect(
        host="127.0.0.1", 
        port="3306",
        user="root", 
        password="root", 
        db="kakikko",
        charset='utf8'
        )
    return conn

def auto_increment_id(table_name):
    query = f""" 
    SELECT AUTO_INCREMENT
    FROM INFORMATION_SCHEMA.TABLES
    WHERE TABLE_SCHEMA = 'kakikko'
    AND TABLE_NAME = '{table_name}';
    """
    return query

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



# -------------------- index.html --------------------
@app.route('/')
@app.route('/index.html')
def index():
    conn = conn_db()
    cursor = conn.cursor(dictionary=True)
    
    Plofile = None
    if 'login_id' in session:
        cursor.execute("""
        SELECT username, email, profile_image
        FROM users
        WHERE id = %s
        """, (session["login_id"],)) 
        Plofile = cursor.fetchone()
    
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
    
    return render_template('index.html', books=books, Plofile=Plofile)



# -------------------- category.html --------------------
@app.route('/category/<category>')
def category(category):
    if 'login_id' not in session:
        session["lastpage"] = {"endpoint": "category", "args": {"book_id": category}}
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
    if 'login_id' in session:
        session["lastpage"] = {"endpoint": "profile"}
        
        return redirect(url_for('profile'))
    
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
            if "lastpage" in session:
                lastpage_data = session.pop("lastpage")  # セッションから削除してリダイレクト
                return redirect(url_for(lastpage_data["endpoint"], **lastpage_data.get("args", {})))
            else:
                return redirect(url_for('index'))
            
        else:
            error = "無効なユーザー名、メールアドレス、パスワード"
            return render_template('login.html', error=error)
    
    return render_template('login.html')



# -------------------- logout.html --------------------
@app.route('/logout.html')
def logout():
    session.pop('login_id', None)  # ユーザーのセッション情報の消去
    return render_template('logout.html')  # ログアウトページの表示

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html')



# -------------------- create.html --------------------
@app.route('/create')
def create():
    if 'login_id' not in session:
        session["lastpage"] = {"endpoint": "create"}
        return redirect(url_for('login'))
    
    edit_book_id = request.args.get('edit_book_id')
    if edit_book_id:
        connection = conn_db()
        cursor = connection.cursor()
        cursor.execute('''
            SELECT book_title, book_content, book_category, book_price, book_cover_image 
            FROM books 
            WHERE book_id = %s
        ''', (edit_book_id,))
        book = cursor.fetchone()
        cursor.close()
        connection.close()

        if book:
            book_data = {
                'book_title': book[0], # type: ignore
                'book_content': book[1], # type: ignore
                'category': book[2],  # ここで使用するキー名がテンプレートと同じであることを確認してください。 # type: ignore
                'book_price': book[3], # type: ignore
                'book_cover_image': book[4] # type: ignore
            }
            return render_template('create.html', book=book_data)
    
    return render_template('create.html')



# -------------------- 投稿を更新する --------------------
@app.route('/update_post', methods=['POST'])
def update_post():
    if 'login_id' not in session:
        return jsonify({'message': 'ログインが必要です'}), 401

    data = request.get_json()
    book_id = data.get('edit_book_id')
    
    connection = conn_db()
    cursor = connection.cursor()
    
    try:
        cursor.execute('''
            UPDATE books 
            SET book_title = %s, book_content = %s, book_category = %s, book_price = %s 
            WHERE book_id = %s AND owner_id = %s
        ''', (
            data['title'],
            data['content'],
            data['category'],
            data['price'],
            book_id,
            session['login_id']
        ))
        connection.commit()
        return jsonify({'message': '成功'})
    except Exception as e:
        return jsonify({'message': str(e)}), 500
    finally:
        cursor.close()
        connection.close()


# -------------------- 表紙画像アップロード --------------------
@app.route('/image_upload', methods=['POST'])
def image_upload():
    conn = conn_db()
    cursor = conn.cursor()
    
    cursor.execute(auto_increment_id('books'))
    latest_book_id = cursor.fetchone() # 取得した結果を表示 
    
    app.config['UPLOAD_FOLDER'] = 'kakikko/static/images/users_images'
    file = request.files['image_data']
    print(file)
    file_name = f"{latest_book_id[0] - 1}_{file.filename}" # type: ignore
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file_name) # type: ignore
    file.save(file_path)
    
    cursor.close()
    conn.close()
    
    return jsonify({'message': '画像をアップロードしました'}), 200



# -------------------- 投稿を作成する --------------------

@app.route('/submit_create', methods=['POST'])
def submit_create():
    if 'login_id' not in session:
        return jsonify({'message': 'ログインしてください'}), 401
        
    conn = None
    cursor = None
    try:
        
        data = request.get_json()
        cover_image = data.get('cover_image_path', '')
        if not cover_image:
            return jsonify({'message': '表紙画像をアップロードしてください'}), 400

        conn = conn_db()
        cursor = conn.cursor()
        
        cursor.execute(auto_increment_id('books'))
        latest_book_id = cursor.fetchone() # 取得した結果を表示 
        cover_image = f"{latest_book_id[0]}_{cover_image}" # type: ignore
        
        # 要約を生成
        model = genai.GenerativeModel('gemini-2.0-flash-001')
        # GOOGLE_API_KEY=userdata.get('GOOGLE_API_KEY')  👈環境変数をつかおう（めんどい）
        genai.configure(api_key="AIzaSyAWTBtp9Nx5ZI66LL0daEU57DLQgyCoI3U")
        # 生成なう
        response = model.generate_content("次の内容を基に、物語の冒頭20%を使用して要約し、読者の興味を引く書籍紹介文を生成。長さは約80文字。"+data['content'])
        re_text = response.candidates[0].content.parts[0].text
        print(re_text)


        insert_sql = """
        INSERT INTO books (
            book_title,
            book_content,
            book_summary,
            book_category,
            book_price,
            book_cover_image,
            owner_id
        ) VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        
        values = [
            data['title'],
            data['content'],
            re_text,
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



# -------------------- 投稿を削除する --------------------
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
        if not result or result[0] != session['login_id']: # type: ignore
            return jsonify({'message': '権限がありません'}), 403

        cursor.execute("SELECT book_cover_image FROM books WHERE book_id = %s", (book_id,))
        cover_image = cursor.fetchone()[0] # type: ignore
        file_path = f"kakikko/static/images/users_images/{cover_image}"
        
        # ファイルが存在するか確認
        if os.path.exists(file_path):
            os.remove(file_path)
        else:
            print(f"File not found: {file_path}")

        # book_id に依存するショッピングカートのレコードを削除
        cursor.execute("DELETE FROM shopping_cart WHERE book_id = %s", (book_id,))
        
        # book_id に依存するコメントを削除
        cursor.execute("DELETE FROM comments WHERE book_id = %s", (book_id,))
        
        # book_id に依存する取引のレコードを削除
        cursor.execute("DELETE FROM transactions WHERE book_id = %s", (book_id,))
        
        # 書籍レコードを削除
        cursor.execute("DELETE FROM books WHERE book_id = %s", (book_id,))
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
@app.route('/chatroom')
def chatroom():
    if 'login_id' not in session:
        session["lastpage"] = {"endpoint": "chatroom"}
        return redirect(url_for('login'))  
    return render_template('chatroom.html')  

@app.route('/get_user_id/<username>', methods=['GET'])
def get_user_id(username):
    connection = conn_db()
    cursor = connection.cursor()
    cursor.execute('SELECT id FROM users WHERE username = %s', (username,))
    user = cursor.fetchone()
    cursor.close()
    connection.close()

    if user:
        print(f"User found: {username} with ID {user[0]}")  # type: ignore # 添加日志
        return jsonify({'user_id': user[0]}) # type: ignore
    else:
        print(f"User not found: {username}")  # 添加日志
        return jsonify({'error': 'User not found'}), 404

@app.route('/send_message', methods=['POST'])
def send_message():
    sender_id = session.get('login_id')
    if not sender_id:
        return jsonify({'error': 'User not logged in'}), 401

    data = request.get_json()
    recipient_id = data['recipient_id']
    message = data['message']

    connection = conn_db()
    cursor = connection.cursor()
    cursor.execute('INSERT INTO direct_messages (sender_id, recipient_id, message) VALUES (%s, %s, %s)',
                   (sender_id, recipient_id, message))
    connection.commit()
    cursor.close()
    connection.close()

    return jsonify({'success': 'Message sent'})

@app.route('/get_messages/<int:recipient_id>', methods=['GET'])
def get_messages(recipient_id):
    sender_id = session.get('login_id')
    if not sender_id:
        return jsonify({'error': 'User not logged in'}), 401

    connection = conn_db()
    cursor = connection.cursor()
    cursor.execute('''
        SELECT dm.sender_id, u.username, dm.message, dm.timestamp
        FROM direct_messages dm
        JOIN users u ON dm.sender_id = u.id
        WHERE (dm.sender_id = %s AND dm.recipient_id = %s) OR (dm.sender_id = %s AND dm.recipient_id = %s)
        ORDER BY dm.timestamp ASC
    ''', (sender_id, recipient_id, recipient_id, sender_id))
    messages = cursor.fetchall()
    cursor.close()
    connection.close()

    messages_list = [{'sender_id': msg[0], 'username': msg[1], 'message': msg[2], 'timestamp': msg[3].strftime('%Y-%m-%d %H:%M:%S')} for msg in messages] # type: ignore

    return jsonify(messages_list)


    




# -------------------- メッセージを送信する --------------------









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
        session["lastpage"] = {"endpoint": "filter"}
        return redirect(url_for('login'))
       
    try:
        conn = conn_db()
        cursor = conn.cursor(dictionary=True)
       
        # クエリパラメータの取得
        selected_categories = request.args.getlist('category')
        selected_prices = request.args.getlist('price')
        sort_option = request.args.get('sort', 'newest')  # デフォルトでは、書籍は書籍IDの降順でソートされます。
       
        # クエリーの構築
        query = """
            SELECT b.*, u.username as owner_name
            FROM books b
            JOIN users u ON b.owner_id = u.id
            WHERE 1=1
        """
        params = []
       
        if selected_categories:
            query += " AND b.book_category IN (%s)" % ','.join(['%s'] * len(selected_categories))
            params.extend(selected_categories)
       
        if selected_prices:
            max_price = max(map(int, selected_prices))
            query += " AND b.book_price <= %s"
            params.append(max_price)
       
        # 並べ替えオプションの追加
        if sort_option == 'popularity':
            query += " ORDER BY b.popularity DESC"
        elif sort_option == 'newest':
            query += " ORDER BY b.created_at DESC"  # 降順にソートするには created_at フィールドを使用する。
        elif sort_option == 'price-asc':
            query += " ORDER BY b.book_price ASC"
        elif sort_option == 'price-desc':
            query += " ORDER BY b.book_price DESC"
        else:
            query += " ORDER BY b.book_id DESC"
       
        cursor.execute(query, params)
        books = cursor.fetchall()
       
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
       
        filters = {
            'category': selected_categories,
            'price': selected_prices
        }
       
        return render_template('filter.html', books=books, filters=filters, category_names=category_names)
       
    except Exception as e:
        print(f"Error: {e}")
        return render_template('filter.html', books=[], filters={'category': [], 'price': []}, category_names={})
       
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()



# -------------------- 検索 --------------------
@app.route('/api/search-suggestions')
def search_suggestions():
    query = request.args.get('query', '').strip()
    if not query:
        return jsonify({'suggestions': []})
    
    try:
        conn = conn_db()
        cursor = conn.cursor(dictionary=True)
        
        # LIKEを使ったあいまい検索
        cursor.execute("""
            SELECT DISTINCT book_title as title
            FROM books 
            WHERE book_title LIKE %s
            LIMIT 5
        """, (f'%{query}%',))
        
        suggestions = cursor.fetchall()
        return jsonify({'suggestions': suggestions})
        
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'suggestions': []})
    
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()



# -------------------- 検索結果ページ --------------------
@app.route('/search')
def search():
    query = request.args.get('query', '').strip()
    if not query:
        return redirect(url_for('filter'))
        
    try:
        conn = conn_db()
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("""
            SELECT b.*, u.username as owner_name
            FROM books b
            JOIN users u ON b.owner_id = u.id
            WHERE b.book_title LIKE %s
            ORDER BY b.book_id DESC
        """, (f'%{query}%',))
        
        books = cursor.fetchall()

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
        
        return render_template('filter.html', 
                             books=books,
                             filters={'category': [], 'price': []},
                             category_names=category_names,
                             search_query=query)
                             
    except Exception as e:
        print(f"Error: {e}")
        return render_template('filter.html', 
                             books=[],
                             filters={'category': [], 'price': []},
                             category_names=category_names,
                             search_query=query)
    
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()



# -------------------- product-details.html --------------------
@app.route('/product-details/<int:book_id>')
def product_details(book_id):
    if 'login_id' not in session:
        session["lastpage"] = {"endpoint": "product_details", "args": {"book_id": book_id}}
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
        
        # 現在のユーザーがその本をブックマークしているかチェックする。
        cursor.execute("""
            SELECT 1 FROM favorites 
            WHERE user_id = %s AND book_id = %s
        """, (session['login_id'], book_id))
        is_favorited = cursor.fetchone() is not None
        
        # お気に入りの数を取得する
        cursor.execute("""
            SELECT COUNT(*) as favorite_count
            FROM favorites
            WHERE book_id = %s
        """, (book_id,))
        favorite_count = cursor.fetchone()['favorite_count'] # type: ignore

        return render_template('product-details.html', 
                            book=book,
                            comments=comment_data,
                            username=book['username'], # type: ignore
                            is_owner=is_owner,
                            is_purchased=is_purchased,
                            is_favorited=is_favorited,
                            favorite_count=favorite_count)
                             
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

    return redirect(url_for('shoppingcart'))



# -------------------- 今すぐ購入の処理 --------------------
@app.route('/submit_product-details', methods=['POST'])
def submit_data():
    accountID = session['login_id']
    data = request.get_json()
    sellerID = int(data.get('sellerID'))
    productID = int(data.get('productID'))

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

    return redirect(url_for('payment',account=accountID,product=productID))



#----------------------------- 商品につけるコメントの処理 --------------------------
@app.route('/submit_product-comment', methods=['POST'])
def submit_comment():
    accountID = session['login_id']
    data = request.get_json()
    maintxt = data.get('maintxt')
    productID = int(data.get('productID'))

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



#--------------------------charge.html-----------------------------------
@app.route('/charge.html')
def charge():
    if 'login_id' not in session:
        session["lastpage"] = {"endpoint": "charge"}
        return redirect(url_for('login'))
    conn = conn_db()
    cursor = conn.cursor(dictionary=True)
    
    accountID = session['login_id']
    
    cursor.execute("""
    SELECT currency
    FROM users
    WHERE id = %s
    """, (accountID,))
    json_data = cursor.fetchone()
    current_Balance = json_data["currency"] # type: ignore
    return render_template('charge.html',current_Balance=current_Balance)




#仮想通貨のチャージ
@app.route('/chargeCoins', methods=['POST'])
def chargeCoins():
    if 'login_id' not in session:
        session["lastpage"] = {"endpoint": "chargeCoins"}
        return redirect(url_for('login'))
    try:
        conn = conn_db()
        cursor = conn.cursor(dictionary=True)
        
        accountID = session['login_id']
        data = request.get_json()
        print(type(data.get('addedFunds')))
        addedFunds = int(data.get('addedFunds'))
        
        cursor.execute("""
        SELECT currency
        FROM users
        WHERE id = %s
        """, (accountID,))
        json_data = cursor.fetchone()
        current_Balance = json_data["currency"] # type: ignore
        new_Balance = current_Balance + addedFunds # type: ignore
        print(f"現在の金額 : {current_Balance}  追加する金額 : {addedFunds}  新しい金額 : {new_Balance}")
        
        update_query3 = """
        UPDATE users
        SET currency = %s
        WHERE id = %s
        """
        cursor.execute(update_query3, (new_Balance, accountID))
        conn.commit()
        
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        conn.rollback()  # エラーが発生した場合はロールバック
        
    finally:
        cursor.close()
        conn.close()
    return ""


# -------------------- shopping-cart.html --------------------
@app.route('/shopping-cart.html')
def shoppingcart():
    if 'login_id' not in session:
        session["lastpage"] = {"endpoint": "shoppingcart"}
        return redirect(url_for('login'))
        
    try:
        accountID = session['login_id']
        conn = conn_db()
        cursor = conn.cursor(dictionary=True)
        
        # Get user points
        cursor.execute("""
            SELECT points 
            FROM users 
            WHERE id = %s
        """, (session['login_id'],))
        user_points = cursor.fetchone()['points'] # type: ignore
        
        #所持金の取得
        cursor.execute("""
            SELECT currency
            FROM users
            WHERE id = %s
        """, (accountID,))

        currency = cursor.fetchone()['currency'] # type: ignore

        
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
        session['total_price'] = total_price
        return render_template(
            'shopping-cart.html',
            cart_items=cart_items,
            total_items=total_items,
            total_price=total_price,
            user_points=user_points,
            currency=currency,
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
@app.route('/proceedToCheckout',methods=['POST']) # type: ignore
def proceedToCheckout():
    try:
        conn = conn_db()
        cursor = conn.cursor()
        
        accountID = session['login_id']
        total_price = session['total_price']
        data = request.get_json()
        usepoint = data.get('usepoints')
        if usepoint == None:
            usepoint = 0
        
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
            
        #購入された書籍の金額を所持金から引く
        cursor.execute("""
        SELECT currency,points
        FROM users
        WHERE id = %s
        """, (accountID,))
        price = cursor.fetchone()
        new_currency = price[0] - int(total_price) + usepoint # type: ignore
        new_points = float(price[1]) - usepoint # type: ignore
        
        update_query3 = """
        UPDATE users
        SET currency = %s,points = %s
        WHERE id = %s
        """
        cursor.execute(update_query3, (new_currency,new_points, accountID))


        conn.commit()
        print(f'支払い総額 : {total_price}  使用ポイント : {usepoint}  残高 : {new_currency}')
        return redirect(url_for('purchase_history'))

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        conn.rollback()  # エラーが発生した場合はロールバック

    finally:
        cursor.close()
        conn.close()



# -------------------- お気に入り機能 --------------------
@app.route('/toggle-favorite', methods=['POST'])
def toggle_favorite():
    if 'login_id' not in session:
        return jsonify({'error': 'ログインが必要です'}), 401
        
    data = request.get_json()
    book_id = data.get('book_id')
    user_id = session['login_id']
    
    conn = conn_db()
    cursor = conn.cursor()
    
    # すでにお気に入りに登録されているかチェック
    cursor.execute('''
        SELECT favorite_id FROM favorites 
        WHERE user_id = %s AND book_id = %s
    ''', (user_id, book_id))
    existing_favorite = cursor.fetchone()
    
    if existing_favorite:
        # すでにお気に入りに登録されている場合、お気に入りを削除
        cursor.execute('''
            DELETE FROM favorites 
            WHERE user_id = %s AND book_id = %s
        ''', (user_id, book_id))
        status = 'removed'
    else:
        # お気に入りに登録されていない場合、お気に入りを追加
        cursor.execute('''
            INSERT INTO favorites (user_id, book_id)
            VALUES (%s, %s)
        ''', (user_id, book_id))
        status = 'added'
        
    cursor.execute('''
        SELECT COUNT(*) FROM favorites 
        WHERE book_id = %s
    ''', (book_id,))
    favorite_count = cursor.fetchone()[0] # type: ignore
    
    conn.commit()
    cursor.close()
    conn.close()
    
    return jsonify({'status': status, 'favorite_count': favorite_count})



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
        session["lastpage"] = {"endpoint": "profile"}
        return redirect(url_for('login', _external=True))

    try:
        conn = conn_db()
        cursor = conn.cursor(dictionary=True)

        if request.method == 'POST':
            # プロフィール画像アップロード処理
            # if 'profile_image' in request.files:
            file = request.files.get('profile_image')
            username = request.form.get('username')
            password = request.form.get('password')
            bio = request.form.get('Bio')
            print(file, username, password, bio)
            
            if file:
                upload_folder = 'kakikko/static/images/profiles_images'

                # アップロードフォルダ内のファイルを調べる
                for existing_file in os.listdir(upload_folder):
                    # ファイル名の最初の"/"以前の文字列を取得
                    existing_filename = existing_file.split('_')[:2]
                    existing_filename = "_".join(existing_filename)  # user_100000の形式に変換
                    # 一致する場合はファイルを削除
                    if existing_filename == secure_filename(f"user_{session['login_id']}"):
                        file_to_delete = f"{upload_folder}/{existing_file}"
                        os.remove(file_to_delete)
                            
                filename = f"user_{session['login_id']}_{secure_filename(file.filename)}" # type: ignore
                file_path = f"{upload_folder}/{filename}"
                try:
                    file.save(file_path)  # file_pathに、fileを保存
                except Exception as e:
                    return f"File upload failed: {str(e)}", 500

                try:
                    
                    cursor.execute("""
                        UPDATE users
                        SET profile_image = %s, username = %s, password = %s, bio = %s
                        WHERE id = %s
                    """, (filename, username, password, bio, session['login_id']))
                    conn.commit()

                    session['login_name'] = username
                        
                except Exception as e:
                    conn.rollback()
                    return "Database error", 500
            else:
                cursor.execute("""
                    UPDATE users
                    SET username = %s, password = %s, bio = %s
                    WHERE id = %s
                """, (username, password, bio, session['login_id']))
                conn.commit()
                session['login_name'] = username

        cursor.execute("""
            SELECT * FROM users WHERE id = %s
        """, (session['login_id'],))
        user_info = cursor.fetchone()
        
        # ユーザーがお気に入りした本を取得
        cursor.execute("""
            SELECT books.book_id, books.book_title, books.book_cover_image, books.book_price
            FROM favorites
            JOIN books ON favorites.book_id = books.book_id
            WHERE favorites.user_id = %s
        """, (session['login_id'],))
        favorite_books = cursor.fetchall()


        return render_template('profile.html', user_info=user_info, favorite_books=favorite_books)
    
    finally:
        cursor.close()
        conn.close()



# -------------------- profile-info.html --------------------
@app.route('/profile-info.html')
def profileinfo():
    if 'login_id' not in session:
        session["lastpage"] = {"endpoint": "profileinfo"}
        return redirect(url_for('login'))
        
    try:
        conn = conn_db()
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("""
            SELECT * FROM users WHERE id = %s
        """, (session['login_id'],))
        user_info = cursor.fetchone()
        
        return render_template('profile-info.html', user_info=user_info)
        
    finally:
        cursor.close()
        conn.close()



# -------------------- purchase-history.html --------------------
@app.route('/purchase-history.html')
def purchase_history():
    if 'login_id' not in session:
        session["lastpage"] = {"endpoint": "purchase_history"}
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
        session["lastpage"] = {"endpoint": "read", "args": {"book_id": book_id}}
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
        session["lastpage"] = {"endpoint": "quiz", "args": {"book_id": book_id}}
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
        session["lastpage"] = {"endpoint": "submit_quiz"}
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
            
            # 現在のポイントを取得
            cursor.execute("SELECT points FROM users WHERE id = %s", (session['login_id'],))
            current_points = cursor.fetchone()[0] or 0 # type: ignore
            
            # 2ポイントを追加
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


# 设置 Flask 配置
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SESSION_TYPE'] = 'filesystem'

if __name__ == '__main__':
    app.run(debug=False, host="0.0.0.0", port=80)
