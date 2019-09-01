from flask import Flask , render_template , redirect , request , jsonify , json , Response
app = Flask(__name__, template_folder='.')
import os

@app.route('/')
@app.route('/index')
def index():
    return '0'
   

@app.route('/health')
def health():
	return 'OK'	
  
app.run(host='0.0.0.0')

