from flask import Flask, request, jsonify, Response
import json
import mysql.connector
from flask_cors import CORS, cross_origin
import logging
import csv
app = Flask(__name__)

def getMysqlConnection():
    return mysql.connector.connect(user='testing', host='mysql', port='3306', password='testing', database='test')

@app.route("/")
def hello():
    return "Flask inside Docker!!"

@app.route('/api/getMonths', methods=['GET'])
@cross_origin() # allow all origins all methods.
def get_months():
    db = getMysqlConnection()
    print(db)
    try:
        sqlstr = "SELECT * from containers_registered"
        print(sqlstr)
        cur = db.cursor()
        cur.execute(sqlstr)
        output_json = cur.fetchall()
    except Exception as e:
        print("Error in SQL:\n", e)
    finally:
        db.close()
    return jsonify(results=output_json)



@app.route('/health', methods=['GET'])
def get_health():
    db = getMysqlConnection()
    try:
        sqlstr = "SELECT 1"
        logging.info("This is an info message")
        cur = db.cursor()
        cur.execute(sqlstr)
        output_json = cur.fetchall()
    except Exception as e:
        print("Error in SQL:\n", e)
    finally:
        db.close()
    return jsonify(results=output_json)

@app.route('/unknown', methods=['GET'])
def get_unknown():
    db = getMysqlConnection()
    try:
        data_query = "SELECT * from unknown"
        logging.info("This is an unknown request massege")
        cur = db.cursor()
        cur.execute(data_query)
        output_json = cur.fetchall()
    except Exception as e:
        print("Error in SQL:\n", e)
    finally:
        db.close()
    return jsonify(results=output_json)

@app.route('/batch-weight', methods=['GET','POST'])
def post_batch_weight():
    db = getMysqlConnection()
    try:
        with open ('containers1.csv', 'r') as f:
            reader = csv.reader(f)
            return reader
            columns = next(reader) 
            query = 'INSERT INTO unknown({1}) values ({1})'
            query = query.format(','.join(columns), ','.join('?' * len(columns)))
            cursor = connection.cursor()
            for data in reader:
                cursor.execute(query, data)
            cursor.commit()
    except Exception as e:
        print("Error in SQL:\n", e)
    finally:
        db.close()
        return 'done'




if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0')
