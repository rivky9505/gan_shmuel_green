
from flask import Flask, request, jsonify, Response, render_template
import json, pprint
import mysql.connector
from flask_cors import CORS, cross_origin
import logging
import datetime
import csv
app = Flask(__name__)

def getMysqlConnection():
    return mysql.connector.connect(user='root', host='mysql', port='3306', password='root', database='weight')

@app.route("/")
def hello():
    return render_template('index.html')


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
    cur = db.cursor()
    try:
        data_query = "SELECT * FROM containers_registered"
        # logging.info("Looking for items with unknown weights")
        cur = db.cursor()
        cur.execute(data_query)
        output_json = cur.fetchall()
        unknowns = []
        for row in output_json :
            if ((row[1]) == 'na') :
                unknowns.append(row[0])

    except Exception as e:
        logging.error("ERROR , while trying : %s", data_query)
        return jsonify("500 Internal server error")
    finally:
        logging.info("200 OK Weight is healthy")
        db.close()
    return render_template('unknown.html' ,unknowns=unknowns)


@app.route('/batch-weight', methods=['GET','POST'])
def post_batch_weight():
    
    if request.method == 'POST':
        file_input = request.form['file']
        formt = file_input.split(".")
        db = getMysqlConnection()
        cur = db.cursor()
        cur.execute("TRUNCATE TABLE containers_registered;")
        kg ="kg"
        na = "na"
        if (formt[1] == "csv"):
            try:
                data=[]
                with open('/app/in/%s' % file_input, 'rU') as f:   
                    reader = csv.reader(f)
                    i = next(reader)
                    for line in f:
                        line = line.replace('\n', '')
                        if (len(line) != 0):
                            data = line.split(',')
                            if ((data[1]) == 'na'):
                                cur.execute("INSERT INTO containers_registered (container_id, weight,unit) VALUES (%s,%s,%s)", (data[0], na, kg))
                            else:
                                if(i[1] == "lbs"):
                                    data[1] = int(int(data[1])*0.453592)
                                cur.execute("INSERT INTO containers_registered (container_id, weight,unit) VALUES (%s,%s,%s)", (data[0], data[1], kg))
                    db.commit()
                    cur.close()
            except Exception as e:
                logging.error("ERROR , while trying batch:")
                return jsonify("500 csv file error")
            finally:
                db.close()
            return render_template('uploaded.html')
        elif (formt[1] == "json"):
            try:
                data=[]
                with open('/app/in/%s' % file_input, 'rU') as f: 
                    next(f)
                    for line in f:
                        if( line != '[' and line != ']'):
                            line = line.replace('{', '').replace('}', '').replace('"', '').replace('\n', '').replace("unit", '').replace("id", '').replace(":", '').replace("weight", '').replace(":", '')
                            data = line.split(',')
                            if (data[1] == "na"):
                                cur.execute("INSERT INTO containers_registered (container_id, weight,unit) VALUES (%s,%s,%s)", (data[0], na, kg))
                            else:
                                if(data[2] == "lbs"):
                                    data[1] = int(int(data[1])*0.453592)
                                cur.execute("INSERT INTO containers_registered (container_id, weight,unit) VALUES (%s,%s,%s)", (data[0], data[1], kg))
                    db.commit()
                    cur.close()
            except Exception as e:
                logging.error("ERROR , while trying batch-weight")
                return jsonify("500 json file error")
            finally:
                db.close()
            return render_template('uploaded.html')

    return render_template('batch-weight.html')



        




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



# GET /weight?from=t1&to=t2&filter=f
# - t1,t2 - date-time stamps, formatted as yyyymmddhhmmss. server time is assumed.
# - f - comma delimited list of directions. default is "in,out,none"
# default t1 is "today at 000000". default t2 is "now". 
# returns an array of json objects, one per weighing (batch NOT included):
# [{ "id": <id>,
#    "direction": in/out/none,
#    "bruto": <int>, //in kg
#    "neto": <int> or "na" // na if some of containers have unknown tara
#    "produce": <str>,
#    "containers": [ id1, id2, ...]
# },...]

@app.route('/weight', methods=['GET'])
def getweight():
    if request.method == "GET":
            db = getMysqlConnection()
            serverTime = datetime.datetime.now().strftime("%Y%m%d%I%M%S")
            t1 = request.form.get('from', default = serverTime , type = str)
            t2 = request.form.get('to', default = "now" , type = str)
            filter = request.form.get('filter', default = "in,out,none" , type = str)
            filter = str(filter).split(',')

            lines = "select * from transactions where " + "datetime>='" + str(t1) + "' and datetime<='" + str(t2) + "'"
            cur = db.cursor()
            cur.execute(lines)
            output_transactions = cur.fetchall()

            weightsList = []

            for line in output_transactions :
                if line[2] in filter :
                    if any(item in str(line[4]).split(',')  for item in get_unknown()):
                        neto = None
                    else:
                        neto = line[7]

                    retweight = { 'id': line[0], 'direction': line[2], 'bruto': line[5], 'neto': neto, 'produce': line[8], 'containers': str(line[4]).split(',') }
                    weightsList.append(retweight)
    return jsonify({'weights': weightsList})                    


if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0')

