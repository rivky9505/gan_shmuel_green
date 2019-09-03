from flask import Flask , render_template , redirect , request , jsonify , json , Response
app = Flask(__name__, template_folder='.')
import os
import mysql.connector
from flaskext.mysql import MySQL

def getMysqlConnection():
    return mysql.connector.connect(user='root', host='0.0.0.0', port='3306', password='123', database='billdb')




mydb = mysql.connector.connect(
  host="0.0.0.0",
  user="root",
  passwd="123",
  port='3306'
)

print(mydb)

@app.route('/')
@app.route('/index')
def index():
    return '0'
   

@app.route('/health')
def health():
    #db = getMysqlConnection()
    cursor = mysql.cursor()
    sql = "SELECT 1"
    cursor.execute(sql)
    results = cursor.fetchall()
    return '{ "ErrorCode" : 0 , "Description" : "OK" }'	
  
app.run(host='0.0.0.0')

