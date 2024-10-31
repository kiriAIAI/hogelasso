from flask import Flask, render_template, send_from_directory

import mysql.connector

app = Flask(__name__, template_folder='kakikko', static_folder='static')

def conn_db():
    conn = mysql.connector.connect(
        host="127.0.0.1", 
        user="root", 
        password="root", 
        db="hew",
        charset='utf8'
        )
    return conn


@app.route('/')
@app.route('/index.html')
def index():
    return render_template('index.html')

@app.route('/create.html')
def create():
    return render_template('create.html')

@app.route('/chatroom.html')
def chatroom():
    return render_template('chatroom.html')

@app.route('/chat.html')
def chat():
    return render_template('chat.html')

@app.route('/login.html')
def login():
    return render_template('login.html')

@app.route('/logout.html')
def logout():
    return render_template('logout.html')

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

@app.route('/product-details.html')
def productdetails():
    return render_template('product-details.html')

@app.route('/search.html')
def search():
    return render_template('search.html')

@app.route('/shopping-cart.html')
def shoppingcart():
    return render_template('shopping-cart.html')

@app.route('/profile.html')
def profile():
    return render_template('profile.html')

@app.route('/purchase-history.html')
def purchase_history():
    return render_template('purchase-history.html')

@app.route('/read.html')
def read():
    return render_template('read.html')


@app.route('/signup.html')
def signup():
    return render_template('signup.html')

@app.route('/signup-security-question.html')
def signupsecurityquestion():
    return render_template('signup-security-question.html')

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


@app.route('/FAQ.html')
def FAQ():
    return render_template("chatbot.html")




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
