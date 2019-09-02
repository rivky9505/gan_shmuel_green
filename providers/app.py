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

@app.route('/selectAll', methods=['GET'])
def selectAll():
    db = getMysqlConnection()
    try:
        data_query = "SELECT * from Provider"
        logging.info("This is an select all request massege")
        cur = db.cursor()
        cur.execute(data_query)
        output_json = cur.fetchall()
    except Exception as e:
        print("Error in SQL:\n", e)
    finally:
        
        db.close()
        return jsonify(results=output_json)

@cross_origin() # allow all origins all methods.

@app.route('/provider/<provider_name>', methods=['GET','POST'])
def insert_provider(provider_name):
    db = getMysqlConnection()
    try:
        data_query = "INSERT INTO Provider (`name`) VALUES  (%s)"
        data=(provider_name,)
        logging.info("This is an select all request massege")
        cur = db.cursor()
        cur.execute(data_query,data)
        output_json = cur.lastrowid
        # output_json = cur.fetchone()
    except Exception as e:
        print("Error in SQL:\n", e)
    finally:
        db.close()
        return jsonify( "id:",(output_json))
    
if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0')

