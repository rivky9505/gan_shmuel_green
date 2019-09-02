from flask import Flask, request, jsonify, Response
import json
import mysql.connector
from flask_cors import CORS, cross_origin
import logging
app = Flask(__name__)

def getMysqlConnection():
    return mysql.connector.connect(user='testing', host='mysql', port='3306', password='testing', database='test')


@app.route("/")
def hello():
    return "Flask inside Docker!!"


@cross_origin() # allow all origins all methods.


@app.route('/health', methods=['GET'])
def get_health():
    db = getMysqlConnection()
    print(db)
    try:
        sqlstr = "SELECT 1"
        cur = db.cursor()
        cur.execute(sqlstr)
        output_json = cur.fetchall()
    except Exception as e:
        logging.error("ERROR , while trying :", sqlstr)
        return jsonify("500 Internal server error")
    finally:
        logging.info("200 OK Weight is healthy")
        db.close()
    return jsonify(results=output_json)



if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0')
