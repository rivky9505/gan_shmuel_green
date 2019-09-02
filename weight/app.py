from flask import Flask, request, jsonify, Response, render_template
import json, pprint
import mysql.connector
from flask_cors import CORS, cross_origin
import logging
import csv
app = Flask(__name__)

def getMysqlConnection():
    return mysql.connector.connect(user='root', host='mysql', port='3306', password='root', database='weight')

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

@app.route('/unknown', methods=['GET'])
def get_unknown():
    db = getMysqlConnection()
    try:
        data_query = "SELECT * FROM unknown"
        logging.info("This is an unknown request massege")
        cur = db.cursor()
        cur.execute(data_query)
        output_json = cur.fetchall()
    except Exception as e:
        logging.error("ERROR , while trying :", data_query)
        return jsonify("500 Internal server error")
    finally:
        logging.info("200 OK Weight is healthy")
        db.close()
    return jsonify(results=output_json)


@app.route('/batch-weight', methods=['GET','POST'])
def post_batch_weight():
    db = getMysqlConnection()
    try:
        with open ('containers1.csv', 'r') as f:
            reader = csv.reader(f)
            data = next(reader) 
            query = 'insert into containers_registered values ({0})'
            query = query.format(','.join('?' * len(data)))
            cursor = db.cursor()
            cursor.execute(query, data)
            for data in reader:
                cursor.execute(query, data)
            cursor.commit()
    except Exception as e:
        print("Error in SQL:\n", e)
    finally:
        db.close()
        return 'done'

@app.route('/weight', methods=['GET', 'POST'])
def postweight():
    db = getMysqlConnection()
    if request.method == "POST":

        lastval = 'select direction from weight ORDER By Created_at DESC LIMIT 1;'
        cur = db.cursor()
        cur.execute(lastval)
        output_json = cur.fetchall()

        a = output_json
        pformat_a = pprint.pformat(a)


        details = request.form
        direction = details['direction']
        truckid = details['truckid']
        containers = details['containers']
        weight = details['weight']
        unit = details['unit']
        forc = details['forc']
        produce = details['produce']
        cur = db.cursor()
        cur.execute("INSERT INTO weight(direction, truckid, containers, weight, unit, forc, produce) VALUES (%s, %s, %s, %s, %s, %s, %s)", (direction, truckid, containers, weight, unit, forc, produce))

        currentval = 'select direction from weight ORDER By Created_at DESC LIMIT 1;'
        cur2 = db.cursor()
        cur2.execute(currentval)
        output_json2 = cur.fetchall()

        b = output_json2
        pformat_b = pprint.pformat(b)


        if pformat_a == pformat_b:
            return "GREAT"
        return "Not equal!"


        conn = getMysqlConnection()
        conn.commit()
        cur.close()
        return 'Success'
    return render_template('weight.html')




if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0')

