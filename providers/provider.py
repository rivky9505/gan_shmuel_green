from flask import Flask , render_template , redirect , request , jsonify , json , Response
app = Flask(__name__, template_folder='.')
import os
import mysql.connector
from flaskext.mysql import MySQL






@app.route('/')
@app.route('/index')
def index():
    return '0'
   

@app.route('/health')
def health():

    return '{ "ErrorCode" : 0 , "Description" : "OK" }'	
  
app.run(host='0.0.0.0')


# Boris START Code



# Boris End Code