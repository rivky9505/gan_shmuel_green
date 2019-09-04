
from flask import Flask, request, jsonify, Response, render_template 
import json, pprint
import mysql.connector
from flask_cors import CORS, cross_origin
import logging, datetime , sys
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

def get_containers_weight(container_id):
    db = getMysqlConnection()
    cur = db.cursor()
    data_query = "SELECT * FROM containers_registered"
    # logging.info("Looking for items with unknown weights")
    cur = db.cursor()
    cur.execute(data_query)
    output_json = cur.fetchall()
    contweights = []
    for row in output_json :
        if ((row[0]) == container_id) :
            return row[1]
    logging.error("Container weights not found")
    return -1

def sum_container_weights(containers_ids_list):
    sum_of_all_containers = 0
    splitted_list = containers_ids_list.split(',')
    for contid in splitted_list :
        contwei = get_containers_weight(contid)
        if contwei != -1 :
            sum_of_all_containers = sum_of_all_containers + contwei
    return sum_of_all_containers

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
                            line = line.replace('{', '').replace('}', '').replace('"', '').replace('\n', '').replace("unit", '').replace("id", '').replace(":", '').replace("weight", '').replace(":", '').replace(" ", '')
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



        




@app.route('/item/<string:id_num>', methods=['GET'])
def get_item_id(id_num):
    db = getMysqlConnection()
    cur = db.cursor()
    #time manage
    time = datetime.datetime.now().strftime("%Y%m%d%I%M%S")
    from_t1 = request.args.get('from')
    if not from_t1:
        from_t1 = datetime.datetime.now().strftime("%Y%m"+"01000000")

    to_t2 = request.args.get('to')
    if not to_t2:
        to_t2 = time
    truck = 0
    container = 0   

    #checking id' existence
    try:
        id_query = ("SELECT * FROM  containers_registered WHERE container_id=" + "'" + id_num + "'")
        cur.execute(id_query)
        row = cur.fetchall()
        if (len(row) > 0):
            container = 1
        if (container == 0):
            id_query = ("SELECT * FROM  weight WHERE truckid="  + "'" + id_num + "'")
            cur.execute(id_query)
            row = cur.fetchall()
            if (len(row) == 0):
                logging.error("no id found")
                return jsonify("404 no id found")
            truck = 1
    except Exception:
        logging.error("ERROR , while trying : get item")
        return jsonify("nope")

    try:
        ret_id = []
        data_query = ("SELECT * FROM  sessions WHERE created_at>="  + from_t1 +" AND created_at<=" + to_t2 + " AND truckid=" + "'" +id_num +"'" + "ORDER BY created_at ASC")
        cur.execute(data_query)
        output_json = cur.fetchall()
        if (len(output_json) > 0):
            for line in output_json:
                last_weight = line[4]
                ret_id.append(line[0])
            json_data = {'id': id_num , 'tara': last_weight , 'sessions' :ret_id }
            return jsonify(json_data)
        else:
            logging.error("no session found")
            return jsonify("no session found")
    except Exception:
        logging.error("ERROR , while trying : get item")
        return jsonify("404 item id not found")
    finally:
        logging.info("200 OK Weight is healthy")
        db.close()

    


@app.route('/weight', methods=['POST'])
# @app.route('/weight', methods=['GET', 'POST'])
def postweight():
    def strip(string):
        # Cleaning JSON files
        line = "%s"%string
        if (line != '[' and line != ']'):

            line = line.replace('{', '').replace('}', '').replace('"', '').replace('\n', '').replace("unit", '').replace("id", '').replace(":", '').replace("weight", '').replace(":", '').replace('[', '').replace('(', '').replace("'", '')
        data = line.split(',')
        if (len(line) != 0):
            return (data[0])
# Starting POST/weight
    db = getMysqlConnection()
    if request.method == "POST":
        # Latest value input
        lastval = 'select direction from weight ORDER By created_at DESC LIMIT 1;'
        cur = db.cursor()
        cur.execute(lastval)
        output_json = cur.fetchall()

        a = output_json
        pformat_a = pprint.pformat(a)
# prepares JSON into comparable string

        jsonin = [('in',)]
        jsonout = [("out",)]
        true = [(1,)]
        none = [('none',)]
        pformat_none = pprint.pformat(none)

# prepares latest value and the one before for comparison
        pformat_jsonin = pprint.pformat(jsonin)
        pformat_jsonout = pprint.pformat(jsonout)
        pformat_true = pprint.pformat(true)
        strip_true = strip(pformat_true)
# Harvesting form data
        # details = request.form
        # direction = details['direction']
        # containers = details['containers']
        # truckid = details['truckid']
        # bruto = details['bruto']
        # unit = details['unit']
        # forc = details['forc']
        # truckTara = details['bruto']
        # produce = details['produce']


        direction = request.args.get('direction')
        containers = request.args.get('containers')
        truckid = request.args.get('truckid')
        bruto = request.args.get('bruto')
        unit = request.args.get('unit')
        forc = request.args.get('forc')
        truckTara = request.args.get('bruto')
        produce = request.args.get('produce')


        cur = db.cursor()
        cur.execute("INSERT INTO weight(direction, truckid, containers, bruto, unit, forc) VALUES (%s, %s, %s, %s, %s, %s)", (direction, truckid, containers, bruto, unit, forc))
# Expect conversion error of comma delimited values of containers

# Taking latest truckID and direction
        currentval = 'SELECT direction from weight ORDER BY created_at DESC LIMIT 1;'
        currenttruck = "SELECT truckid from weight ORDER BY created_at DESC LIMIT 1;" 

        cur.execute(currenttruck)
        output_currenttruck = cur.fetchall()
        pformat_currenttruck = pprint.pformat(output_currenttruck)
        strip_truckid = strip(pformat_currenttruck)

        cur2 = db.cursor()
        cur2.execute(currentval)
        output_json2 = cur.fetchall()
        b = output_json2
        pformat_b = pprint.pformat(b)
        # pformat_a is the previous direction
        # pformat_b is the current direction

        ischeckin = "SELECT direction='in' from weight where truckid='%s' LIMIT 1;"%strip_truckid
        # ischeckout = 'SELECT truckid from weight;'
        checkout_session = "SELECT id from sessions where truckid='%s' ORDER BY created_at DESC LIMIT 1;"%strip_truckid
        isforce = "SELECT forc from weight where truckid='%s' ORDER BY created_at DESC LIMIT 1;"%strip_truckid  ### Added ORDER BY, if not working - DELETE
# Check if truck already checked in
        strip_checkin =""
        cur.execute(ischeckin)
        output_ischeckin = cur.fetchall()
        pformat_ischeckin = pprint.pformat(output_ischeckin)
        strip_checkin = strip(pformat_ischeckin)

        strip_force = 0

        
        strip_checkin = ""

        if pformat_a == pformat_b and strip_checkin == strip_true:
            # If current and previous directions are equal (in after in OR out after out) AND truck had already checked in
            if strip_force == '1':
                # then override latest bruto weight of this truckID
                cur.execute("UPDATE weight SET bruto = '%s' WHERE truckid = '%s';" %(bruto, strip_truckid))
                # return "Is forced and updated bruto value %s"%strip_force
            # else :
                # return "Error! You already checked-in, use the 'Force = 1' option to overwrite entry..."
        if pformat_b == pformat_jsonin or pformat_b == pformat_none: 
            if pformat_b == pformat_none and strip_checkin == strip_true:
                return "Error! Entering None after already being checked-in isn't going to work..."
# Open session for direction (in/none) ,truckID, bruto
            cur.execute("INSERT INTO sessions(direction, truckid, bruto) VALUES (%s, %s, %s)", (direction, truckid, bruto))

        
        #ischeckin = "SELECT direction='in' from weight where truckid='%s' LIMIT 1;"%strip_truckid
        # ischeckout = 'SELECT truckid from weight;'
        #checkout_session = "SELECT id from sessions where truckid='%s' ORDER BY created_at DESC LIMIT 1;"%strip_truckid
        #isforce = "SELECT forc from weight where truckid='%s' ORDER BY created_at DESC LIMIT 1;"%strip_truckid  ### Added ORDER BY, if not working - DELETE
# Check if truck already checked in
        #strip_checkin =""
        #cur.execute(ischeckin)
        #output_ischeckin = cur.fetchall()
        #pformat_ischeckin = pprint.pformat(output_ischeckin)
       # strip_checkin = strip(pformat_ischeckin)

        cur.execute(checkout_session)
        output_checkout = cur.fetchall()
        pformat_checkout = pprint.pformat(output_checkout)
        strip_checkoutid = strip(pformat_checkout)


        # cur.execute(isforce)
        # output_force = cur.fetchall()
        # pformat_force = pprint.pformat(output_force)
        # strip_force = strip(pformat_force)


        last_checkinid = "SELECT id from weight where truckid='%s' ORDER BY direction LIMIT 1;"%truckid

        cur.execute(last_checkinid)
        output_lastcheckinid = cur.fetchall()
        pformat_lastcheckinid = pprint.pformat(output_lastcheckinid)
        strip_lastcheckinid = strip(pformat_lastcheckinid)


        last_checkoutid = "SELECT id FROM weight WHERE direction = 'out' ORDER BY created_at DESC LIMIT 1;"
        cur.execute(last_checkoutid)
        output_lastcheckoutid = cur.fetchall()
        pformat_lastcheckoutid = pprint.pformat(output_lastcheckoutid)
        strip_lastcheckoutid = strip(pformat_lastcheckoutid)

        truckTara_query = "SELECT bruto FROM weight WHERE direction = 'out' ORDER BY created_at DESC LIMIT 1;"
        bruto_query = "SELECT bruto from weight WHERE id = '%s';"%strip_lastcheckinid

        cur.execute(bruto_query)
        output_bruto = cur.fetchall()
        pformat_bruto = pprint.pformat(output_bruto)
        strip_bruto = strip(pformat_bruto)
        

        cur.execute(truckTara_query)
        output_truckTara = cur.fetchall()
        pformat_truckTara = pprint.pformat(output_truckTara)
        strip_truckTara = strip(pformat_truckTara)

        strip_bruto = int(strip_bruto)
        strip_truckTara = int(strip_truckTara)
        neto = (strip_bruto - strip_truckTara)
      
        containers_on_truck_query = "select containers from weight where truckid= %s" %strip_truckid
        cur.execute(containers_on_truck_query)
        output_containers_on_truck = cur.fetchall()
        if neto != output_containers_on_truck :
            return "ERROR neto != output_containers_on_truck "
      
        successin = "SELECT JSON_OBJECT('id', id, 'created', created_at, 'truckid', truckid, 'Bruto', bruto) from sessions ORDER BY created_at DESC LIMIT 1;"
        cur.execute(successin)
        output_successin = cur.fetchall()
        pformat_successin = pprint.pformat(output_successin)

        if pformat_b == pformat_jsonout:
            if pformat_ischeckin == pformat_true:
                cur.execute("INSERT INTO sessions(direction, truckid, bruto, truckTara, neto) VALUES (%s, %s, %s, %s, %s)", (direction, truckid, strip_bruto, truckTara, neto))
                successout = "SELECT JSON_OBJECT('id', id, 'created', created_at, 'truckid', truckid, 'Bruto', bruto, 'truckTara', %s, 'Neto', neto) from sessions ORDER BY created_at DESC LIMIT 1;"%strip_truckTara
                cur.execute(successout)
                output_successout = cur.fetchall()

                pformat_successout = pprint.pformat(output_successout)
                return "Seccessfully checked-out with last entrance session ID: %s and output: %s" % (strip_checkoutid, pformat_successout) ## Thats the truck to checkout
            else:
                ## Checkout without check-in, raise error!
                return "Error! Trying to checkout without any check-in..."



        # return "Successfully added entry: %s"%pformat_successin

        conn = getMysqlConnection()
        conn.commit()
        cur.close()
    # return render_template('weight.html')




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
        # data_query = ("SELECT * FROM  sessions WHERE created_at>="  + from_t1 +" AND created_at<=" + to_t2 + " AND truckid=" + "'" +id_num +"'" + "ORDER BY created_at ASC")

            lines = "select * from weight where " + "created_at>='" + t1 + "' and created_at<='" + t2 + "'"
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

                    retweight = { 'id': line[0], 'truck': line[3],'direction': line[2], 'bruto': line[5], 'neto': neto, 'produce': line[8], 'containers': str(line[4]).split(',') }
                    weightsList.append(retweight)
    return jsonify({'weights': weightsList})                    


if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0')

@app.route('/session/<id>', methods=['GET'])
def session(id):
    db = getMysqlConnection()
    if request.method == 'GET':

        getsession = "SELECT JSON_ARRAYAGG(JSON_OBJECT('id', id, 'created', created_at, 'truckid', truckid, 'Bruto', bruto, 'truckTara', truckTara, 'Neto', neto)) from sessions where id='%s'" %id


        cur = db.cursor()
        cur.execute(getsession)
        output_session = cur.fetchall()
        db.close()
        return jsonify(output_session)

    return jsonify(results=output_session)
