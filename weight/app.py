from flask import Flask, request, jsonify, Response
import json
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
        logging.error("ERROR , while trying : %s", sqlstr)
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
        logging.error("ERROR , while trying : %s", data_query)
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

@app.route('/item/<id>', methods=['GET'])
def get_item_id(id):
# GET /item/<id>?from=t1&to=t2
# - id is for an item (truck or container). 404 will be returned if non-existent
# - t1,t2 - date-time stamps, formatted as yyyymmddhhmmss. server time is assumed.
# default t1 is "1st of month at 000000". default t2 is "now". 
# Returns a json:
# { "id": <str>,
#   "tara": <int> OR "na", // for a truck this is the "last known tara"
#   "sessions": [ <id1>,...] 
# }
    db = getMysqlConnection()
    from_t1 = request.form.get('from', default = "1st of month at 000000" , type = str)
    to_t2 = request.form.get('to', default = "now" , type = str)
    item_id = id

    try:
        # Query all entries in containers_registered between times
        data_query = ("SELECT * FROM containers_registered WHERE Created_at BETWEEN %s AND %s" , from_t1 , to_t2 )
        cur = db.cursor()
        cur.execute(data_query)
        output_json = cur.fetchall()
#Pending to see database structure to harvest tara and session IDs values 
        # item_id_json = dict({"id": item_id, 
        #         "tara": <int> , #OR "na" , for a truck this is the "last known tara"
        #         "sessions": [ <id1>,...] })
        # scan the IDs for matches in containers, then in trucks 
        if item_id in output_json :
            #add for to run on all items found
            logging.info(" %s found in containers_registered" , item_id )
            print(" %s found in containers_registered" , item_id )
            # append to JSON to return

# trucks querying,

    except Exception:
        logging.error("ERROR , while trying : %s", data_query)
        return jsonify("404 item id not found")
    finally:
        logging.info("200 OK Weight is healthy")
        db.close()
    return jsonify(results=item_id_json)


if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0')

