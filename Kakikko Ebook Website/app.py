from flask import Flask, render_template, send_from_directory

import mysql.connector

app = Flask(__name__)

def conn_db():
    conn = mysql.connector.connect(
        host="127.0.0.1", 
        user="root", 
        password="root", 
        db="",
        charset='utf8'
        )
    return conn


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/index.html')
def index_html():
    return render_template('index.html')

@app.route('/create.html')
def create():
    return send_from_directory('static_pages', 'create.html')

@app.route('/chatroom.html')
def chatroom():
    return render_template('chatroom.html')

@app.route('/login.html')
def login_html():
    return render_template('login.html')

@app.route('/filter.html')
def filter_html():
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

@app.route('/sign-up.html')
def signup():
    return render_template('sign-up.html')





@app.route('/css/<path:filename>')
def css(filename):
    return send_from_directory('css', filename)

@app.route('/js/<path:filename>')
def js(filename):
    return send_from_directory('js', filename)

@app.route('/fonts/<path:filename>')
def fonts(filename):
    return send_from_directory('fonts', filename)

@app.route('/images/<path:filename>')
def images(filename):
    return send_from_directory('images', filename)



if __name__ == '__main__':
    app.run(debug=True)
