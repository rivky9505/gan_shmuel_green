from flask import Flask , render_template , redirect , request , jsonify , json , Response
app = Flask(__name__, template_folder='.')
import os
from flaskext.mysql import MySQL


app.config['MYSQL_HOST'] = '0.0.0.0'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '123'
app.config['MYSQL_DB'] = 'billdb'


mysql = MySQL(app)



@app.route('/')
@app.route('/index')
def index():
    return '0'
   

@app.route('/health')
def health():
	return 'OK'	
  
app.run(host='0.0.0.0')

