
from flask import Flask, request, jsonify, Response, render_template 
import json, pprint
import mysql.connector
from flask_cors import CORS, cross_origin
import logging, datetime , sys
import csv
app = Flask(__name__)

logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')

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
        cur.execute(data_query)
        output_json = cur.fetchall()
        unknowns = []
        for row in output_json :
            if ((row[1]) == 'na') :
                unknowns.append(row[0])
    except Exception as e:
        logging.error('[GET][FAILURE] /health request . QUERY:' + data_query)
        return jsonify("500 Internal server error")
    finally:
        logging.info("[GET][SUCCESS] get item  request - : %s", (data_query))
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
        logging.error('[GET][FAILURE] /health request . QUERY:' + id_query)
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
            logging.info("[GET][SUCCESS] get item  request - : %s", (data_query))
            return jsonify(json_data)
        else:
            logging.error("no session found")
            return jsonify("no session found")
    except Exception:
        logging.error('[GET][FAILURE] /health request . QUERY:' + data_query)
        return jsonify("404 item id not found")
    finally:
        logging.info("200 OK Weight is healthy")
        db.close()

    



@app.route('/weight', methods=['GET', 'POST'])
def postweight():
    def strip(string):
        line = "%s"%string
        if (line != '[' and line != ']'):

            line = line.replace('{', '').replace('}', '').replace('"', '').replace('\n', '').replace("unit", '').replace("id", '').replace(":", '').replace("weight", '').replace(":", '').replace('[', '').replace('(', '').replace("'", '')
        data = line.split(',')
        if (len(line) != 0):
            return (data[0])

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
        true = [(1,)]

        pformat_jsonin = pprint.pformat(jsonin)
        pformat_jsonout = pprint.pformat(jsonout)
        pformat_true = pprint.pformat(true)



        details = request.form
        direction = details['direction']
        containers = details['containers']
        truckid = details['truckid']
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
        pformat_currenttruck = pprint.pformat(output_currenttruck)
        strip_truckid = strip(pformat_currenttruck)


        ischeckin = "SELECT direction='in' from weight where truckid='%s' LIMIT 1;"%strip_truckid
        ischeckout = 'SELECT truckid from weight;'
        checkout_session = "SELECT id from sessions where truckid='%s' LIMIT 1;"%strip_truckid

        cur.execute(ischeckin)
        output_ischeckin = cur.fetchall()
        pformat_ischeckin = pprint.pformat(output_ischeckin)

        cur.execute(checkout_session)
        output_checkout = cur.fetchall()
        pformat_checkout = pprint.pformat(output_checkout)


        cur2 = db.cursor()
        cur2.execute(currentval)
        output_json2 = cur.fetchall()

        b = output_json2
        pformat_b = pprint.pformat(b)
        

        if pformat_b == pformat_jsonout:
            if pformat_ischeckin == pformat_true:
                return "That's the truck to checkout!"


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





if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0')

