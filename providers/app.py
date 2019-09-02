from flask import Flask, request, jsonify, Response
import json
import mysql.connector
from flask_cors import CORS, cross_origin
import logging
import csv
app = Flask(__name__)

def getMysqlConnection():
    return mysql.connector.connect(user='root', host='mysql', port='3306', password='123', database='billdb')

@app.route("/")
def hello():
    return "Flask inside Docker!!"


@cross_origin() # allow all origins all methods.


@app.route('/health', methods=['GET'])
def get_health():
    db = getMysqlConnection()
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


@app.route('/rates', methods=['GET'])
def get_rates():
    db = getMysqlConnection()
    try:
        sqlstr = "SELECT * FROM Rates"
        cur = db.cursor()
        cur.execute(sqlstr)
        output_jason = cur.fetchall()
    except Exception as e:
        logging.error("ERROR , whilr trying: ", sqlstr)
        return jsonify("500 Internal server error")
    finally:
        logging.info("200 OK SQL completed query: ", sqlstr)
        db.close()
    return jsonify(output_jason)


if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0')

