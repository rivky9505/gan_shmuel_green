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


        jsonin = [('in',)]
        jsonout = [("out",)]
#        true = [('{"1": true}',)
        pformat_jsonin = pprint.pformat(jsonin)
        pformat_jsonout = pprint.pformat(jsonout)
#        pformat_true = pprint.pformat(true)



        details = request.form
        direction = details['direction']
        truckid = details['truckid']
        containers = details['containers']
        bruto = details['bruto']
        unit = details['unit']
        forc = details['forc']
        truckTara = details['bruto']
        neto = details['bruto']
        produce = details['produce']


        cur = db.cursor()
        cur.execute("INSERT INTO weight(direction, truckid, containers, bruto, unit, forc, produce) VALUES (%s, %s, %s, %s, %s, %s, %s)", (direction, truckid, containers, bruto, unit, forc, produce))

        currentval = 'select direction from weight ORDER By Created_at DESC LIMIT 1;'
        currenttruck = "SELECT truckid from weight ORDER BY created_at DESC LIMIT 1;"

        cur.execute(currenttruck)
        output_currenttruck = cur.fetchall()

        ischeckin = "SELECT JSON_OBJECT(direction='in', truckid='truckid') from weight LIMIT 1;"
        ischeckout = 'SELECT truckid from weight;'

        cur.execute(ischeckin)
        output_ischeckin = cur.fetchall()
        pformat_ischeckin = pprint.pformat(output_ischeckin)


        cur2 = db.cursor()
        cur2.execute(currentval)
        output_json2 = cur.fetchall()

        b = output_json2
        pformat_b = pprint.pformat(b)
        

        if pformat_b == pformat_jsonout:
            if pformat_ischeckin == True:
                return "That's the truck to checkout!"
#        return pformat_ischeckin


        if pformat_b == pformat_jsonin and True == True:
            cur.execute("""CREATE TABLE IF NOT EXISTS sessions(`id` int(12) NOT NULL AUTO_INCREMENT, `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP, `truckid` varchar(50) DEFAULT NULL, `bruto` int(12) DEFAULT NULL, `truckTara` int(12) DEFAULT NULL, `neto` int(12) DEFAULT NULL, PRIMARY KEY (`id`)) ENGINE=MyISAM AUTO_INCREMENT=10001""")
            cur.execute("INSERT INTO sessions(truckid, bruto, truckTara, neto) VALUES (%s, %s, %s, %s)", (truckid, bruto, truckTara, neto))

            db.commit()


        if pformat_a == pformat_b:
            return "GREAT"
        return "Not equal!"


        conn = getMysqlConnection()
        conn.commit()
        cur.close()
        return 'Success'
    return render_template('weight.html')

@app.route('/session/<id>', methods=['GET'])
def session(id):
    db = getMysqlConnection()
    if request.method == 'GET':

        getsession = "SELECT JSON_ARRAYAGG(JSON_OBJECT('id', id, 'created', created_at, 'truckid', truckid, 'Bruto', bruto, 'truckTara', truckTara, 'Neto', neto)) from sessions where id='%s'" %id


        cur = db.cursor()
        cur.execute(getsession)
        output_session = cur.fetchall()

        return jsonify(output_session)
        db.close()
    return jsonify(results=output_session)




if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0')

