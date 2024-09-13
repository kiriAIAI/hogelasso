from flask import Flask , render_template

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

#


if __name__ ==  "__main__":
    app.run(debug=True)