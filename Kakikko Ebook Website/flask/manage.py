from flask import Flask , render_template

import mysql.connector

app = Flask(__name__)

def conn_db():
    conn = mysql.connector.connect()