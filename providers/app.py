from flask import Flask, request, jsonify, Response ,send_from_directory
import json
import mysql.connector
from flask_cors import CORS, cross_origin
import logging
import csv
app = Flask(__name__)

logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')

def getMysqlConnection():
    return mysql.connector.connect(user='root', host='mysql', port='3306', password='123', database='billdb')

@app.route("/")
def hello():
    return "Gan Shmuel"

@cross_origin() # Allow all origins all methods.


# GET /health
# - By default returns "OK" and status 200 OK
# -If system depends on external resources (e.g. db), 
# and they are not available (e.g. "select 1;" fails ) 
# then it should return "Failure" and 500 Internal Server Error

@app.route('/health', methods=['GET'])
def get_health():
    db = getMysqlConnection()
    try:
        logging.info('info') # ADD TO PROPER PLACE
        logging.error('error')# ADD TO PROPER PLACE
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


# POST /provider
# Creates a new provider record:
# - name - provider name. must be unique.
# Returns a unique provider id as json: { "id":<str>}

@app.route('/provider', methods=['GET']) #CHANGE TO POST
def insertprovider():
    try:
        return request.form["name"] #CHECK INSERT
        db = getMysqlConnection()
        cur = db.cursor()  
        cur.execute('INSERT INTO Provider (`name`) VALUES ({0})',request.form["name"])
        db.commit()
        cursor.close()
        db.close()
        #ADD LOG  
        return "{ 'id' : " + request.form["name"] + " }," #CHANGE 
    except Exception as e:
        #ADD LOG
        return str(e)


# GET /rates
# Will download a copy of the same excel that was uploaded using POST /rates    
@app.route('/rates', methods=["GET"])
def getrates():
    try:
        #ADD LOG
        return send_from_directory('in', "rates.xlsx",mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    except Exception as e:
        #ADD LOG
        return "FILE NOT FOUND"
        return str(e)



# POST /rates
# - file=<filename>
# Will upload new rates from an excel file in "/in" folder. Rate excel has the following columns:
# - Product - a product id
# - Rate - integer (in agorot)
# - Scope - ALL or A provider id. 
# The new rates over-write the old ones
# A scoped rate has higher precedence than an "ALL" rate

@app.route("/rates",methods=["POST"])
def postrates():
    filename = request.args.get("file")
    try:
        db = getMysqlConnection()
        wb = xl.load_workbook("/in/" + filename )
        ws = wb.get_active_sheet()
        cur = db.cursor()
        cur.execute('TRUNCATE TABLE Rates') #TRUNCATE
        query = "INSERT INTO Rates (product_id, rate, scope) VALUES (%s, %s, %s)" #INSERT
        row = 2
        while ws.cell(row, 1).value is not None:
            product = ws.cell(row, 1).value
            rate = ws.cell(row, 2).value
            scope = ws.cell(row, 3).value
            i_tuple = (product, rate, scope)
            cursor.execute(query, i_tuple)
            row += 1

        db.commit()
        cur.close()
        db.close()
        #ADD LOG
        return "RATES UPLOADED"
    except Exception as e:
        #ADD LOG
        return e


# POST /truck
# registers a truck in the system
# - provider - known provider id
# - id - the truck license plate 

@app.route('/truck/<id>', methods=["POST"])
def inserttruck(id):
    try:
        db = getMysqlConnection()
        cur = connection.cursor()  
        cur.execute('UPDATE truck SET providerId = "{0}" WHERE truckId = {1}'.format(request.form["providerId"], id))
        db.commit()
        cur.close()
        db.close()
        #ADD LOG
        return "ok"
    except Exception as e:
        #ADD LOG
        return str(e)
    

# PUT /truck/{id} can be used to update provider id
@app.route('/truck/<id>', methods=["PUT"])
def updatetruck(id):
    return "TODO"


# GET /truck/<id>?from=t1&to=t2
# - id is the truck license. 404 will be returned if non-existent
# - t1,t2 - date-time stamps, formatted as yyyymmddhhmmss. server time is assumed.
# default t1 is "1st of month at 000000". default t2 is "now". 
# Returns a json:
# { "id": <str>,
#   "tara": <int>, // last known tara in kg
#   "sessions": [ <id1>,...] 
#}
@app.route('/truck/<id>', methods=["GET"])
def truckinfo(id):
    return "TODO"


# GET /bill/<id>?from=t1&to=t2
# - id is provider id
# - t1,t2 - date-time stamps, formatted as yyyymmddhhmmss. server time is assumed.
# default t1 is "1st of month at 000000". default t2 is "now". 
# Returns a json:
# {
#   "id": <str>,
#   "name": <str>,
#   "from": <str>,
#   "to": <str>,
#   "truckCount": <int>,
#   "sessionCount": <int>,
#   "products": [
#     { "product":<str>,
#       "count": <str>, // number of sessions
#       "amount": <int>, // total kg
#       "rate": <int>, // agorot
#       "pay": <int> // agorot
#     },...
#   ],
#   "total": <int> // agorot
# }


if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0')

