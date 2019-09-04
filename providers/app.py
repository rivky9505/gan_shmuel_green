from flask import Flask, request, jsonify, Response ,send_from_directory , render_template
import json
import mysql.connector
from flask_cors import CORS, cross_origin
import logging
import csv
from openpyxl import Workbook , load_workbook
import xlsxwriter
import os.path
import requests
from datetime import datetime
import bill

app = Flask(__name__)

logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
#
def getMysqlConnection():
    return mysql.connector.connect(user='root', host='mysql', port='3306', password='root', database='billdb')

@app.route("/")
def hello():
    return render_template('ProviderMainPage.html')

@cross_origin() # Allow all origins all methods.


#ERROR CODES 
#(0) - SUCCESS
#(-1) - 500 INTERNAL SERVER ERROR
#(-2) - DATABASE CONNECTION ERROR
#(-3) - DATABASE BASE QUERY EXECUTION ERROR
#(-4) - I/O ERROR


# GET /health
# - By default returns "OK" and status 200 OK
# -If system depends on external resources (e.g. db), 
# and they are not available (e.g. "select 1;" fails ) 
# then it should return "Failure" and 500 Internal Server Error
@app.route('/health', methods=['GET'])
def checkhealth():
    try:
        db = getMysqlConnection()
    except:
        return jsonify({ "errorCode" : -2 , "errorDescription" : "ERROR ESTABLISHING A DATABASE CONNECTION" }) , 200
    try:
        query = "SELECT 1"
        cur = db.cursor()
        cur.execute(query)
        result = cur.fetchall()
        logging.info('[GET][SUCCESS] health request . QUERY:' + query)
        return jsonify({ "errorCode" : 0 , "errorDescription" : "status 200 OK" }) , 200 
    except Exception as e:
        logging.error('[GET][FAILURE] /health request . QUERY:' + query)
        return jsonify({ "errorCode" : -1 , "errorDescription" : "500 Internal server error" }) , 500 
    finally:
        logging.info("200 OK")
        db.close()


def json_to_excel(ws, data, row=0, col=0):
    ws.write('A1', 'Product')
    ws.write('B1', 'Rate')
    ws.write('C1', 'Scope')
    row += 1
    for product_id, rate, scope in data:
        ws.write(row, col, str(product_id))
        ws.write(row, col + 1, str(rate))
        ws.write(row, col + 2, str(scope))
        row += 1

# GET /rates
# Will download a copy of the same excel that was uploaded using POST /rates 
@app.route('/rates', methods=['GET'])
def get_rates():
    try:
        db = getMysqlConnection()
    except:
        return jsonify({ "errorCode" : -2 , "errorDescription" : "ERROR ESTABLISHING A DATABASE CONNECTION" }) , 200
    try:
        sqlstr = "SELECT * FROM Rates"
        cur = db.cursor()
        cur.execute(sqlstr)
        output_jason = cur.fetchall()
        db.close()
        logging.info("[GET][SUCCESS] rates request - : %s", (sqlstr))
    except Exception :
        logging.error("[GET][FAILURE] rates request , ON QUERY: %s", (sqlstr))
        return jsonify("ERROR , while trying: %s", (sqlstr))
    try:  # Create and save Excel file
        dir_name = "out"
        file_name = "output.xlsx"
        excel_path = "./" + dir_name + "/" + file_name
        data = output_jason
        wb = xlsxwriter.Workbook(excel_path)
        ws = wb.add_worksheet()
        json_to_excel(ws, data)
        wb.close()
        logging.info("[GET][SUCCESS] rates request : Excel file created in: %s", (excel_path))
    except:
        logging.error("[GET][FAILURE] rates request : Excel file NOT created in: %s", (excel_path))
        return jsonify({ "errorCode" : -4 , "errorDescription" : "I/O ERROR : writing Excel file" }) , 500
    try: # send excel file as http response
        if os.path.exists(excel_path):
            logging.info("[GET][SUCCESS] rates request : Excel file from: %s was sent for download", (excel_path))
            return send_from_directory(dir_name, filename=file_name, as_attachment=True, attachment_filename="Rates.xlsx", mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    except:
        logging.error("[GET][FAILURE] rates request : Excel file from: %s was NOT sent for download", (excel_path))
        return jsonify({ "errorCode" : -1 , "errorDescription" : "status 404 Not Found : Excel file not found" }) , 500


        

# POST /provider
# Creates a new provider record:
# - name - provider name. must be unique.
# Returns a unique provider id as json: { "id":<str>}
@cross_origin() # allow all origins all methods.

@app.route('/selectAll', methods=['GET'])
def selectAll():
    db = getMysqlConnection()
    try:
        data_query = "SELECT * from Provider"
        logging.info("This is an select all request massege")
        cur = db.cursor()
        cur.execute(data_query)
        
    except Exception as e:
        return("Error in SQL:\n", e)
    finally:
        output_json = cur.fetchall()
        db.close()
        return jsonify(results=output_json)
        # return "Hello"


@app.route('/provider/<provider_name>', methods=['GET','POST'])
def insert_provider(provider_name):
    db = getMysqlConnection()
    try:
        data_query = "INSERT INTO Provider (`name`) VALUES  (%s)"
        data=(provider_name,)
        logging.info("[POST][SUCCESS] provider/<provider_name>")
        cur = db.cursor()  
        cur.execute(data_query,data)
        output_json = cur.lastrowid
        output_json = cur.fetchone()
    except Exception as e:
        print('[POST][FAILURE] while trying:', str(e))
    finally:
        db.close()
        return jsonify( "id:",(output_json))


#FOR TESTING
@app.route('/provider2/<provider_name>', methods=['GET','POST'])
def insert_provider2(provider_name):
    try:
        db = getMysqlConnection()
    except:
        return jsonify({ "errorCode" : -2 , "errorDescription" : "ERROR ESTABLISHING A DATABASE CONNECTION" }) , 200
    try:
        data_query = "INSERT INTO Provider (`name`) VALUES  (%s)"
        data=(provider_name,)
        logging.info("[POST][SUCCESS] provider/<provider_name>")
        cur = db.cursor()  
        cur.execute(data_query,data)
        output_json = cur.lastrowid
        output_json = cur.fetchone()
        return jsonify({ "errorCode" : 0 , "errorDescription" : "status 200 OK" , "id:":(output_json) }) , 200
    except Exception as e:
        logging.error('[POST][FAILURE] while trying:', str(e))
        return jsonify({ "errorCode" : -1 , "errorDescription" : "500 Internal server error" }) , 500
    finally:
        db.close()
        
#PUT /provider/{id} can be used to update provider name 
# @app.route('/provider/<id>', methods=['PUT'])
# def putprovider(id):
#     try:
#         newname = request.form["newname"]
#         #return newname
#         db = getMysqlConnection()
#         cur = db.cursor()  
#         cur.execute('UPDATE Provider SET name = ' + '"' +str(newname)+ '"' + ' WHERE id =' + id)
#         db.commit()
#         cur.close()
#         db.close()
#         logging.info('[PUT][SUCCESS] provider/<id>') # CHANGE TO PROPER MESSAGE
#         return id
#     except Exception as e:
#         logging.error('[PUT][FAILURE] provider/<id>') # CHANGE TO PROPER MESSAGE
#         return str(e)


@app.route('/provider/<id>', methods=['PUT'])
def putprovider2(id):
    try:
        db = getMysqlConnection()
    except:
        return jsonify({ "errorCode" : -2 , "errorDescription" : "ERROR ESTABLISHING A DATABASE CONNECTION" }) , 200
    try:
        newname = request.form["newname"]
        cur = db.cursor()  
        cur.execute('UPDATE Provider SET name = ' + '"' +str(newname)+ '"' + ' WHERE id =' + id)
        db.commit()
        cur.close()
        db.close()
        logging.info('[PUT][SUCCESS] provider/<id>') 
        return jsonify({ "errorCode" : 0 , "errorDescription" : "status 200 OK" }) , 200
    except Exception as e:
        logging.error('[PUT][FAILURE] provider/<id>') 
        return jsonify({ "errorCode" : -1 , "errorDescription" : "500 Internal server error" }) , 500


# POST /rates
# - file=<filename>
# Will upload new rates from an excel file in "/in" folder. Rate excel has the following columns:
# - Product - a product id
# - Rate - integer (in agorot)
# - Scope - ALL or A provider id. 
# The new rates over-write the old ones
# A scoped rate has higher precedence than an "ALL" rate

# @app.route("/rates",methods=["POST"])
# def postrates():
#     #filename = "./in/rates.xlsx"
    
#     try:
#         details = request.form
#         filename = str(details["file"])
        
#         db = getMysqlConnection()
#         #wb = load_workbook(filename)
        
#         wb = load_workbook('./in/'+filename)
        
#         ws = wb.get_active_sheet()
#         cur = db.cursor()
        
#         cur.execute('TRUNCATE TABLE Rates') 
#         query = "INSERT INTO Rates (product_id, rate, scope) VALUES (%s, %s, %s)" #INSERT
#         row = 2
#         while ws.cell(row, 1).value is not None:
#             product = ws.cell(row, 1).value
#             rate = ws.cell(row, 2).value
#             scope = ws.cell(row, 3).value
#             i_tuple = (product, rate, scope)
#             cur.execute(query, i_tuple)
#             row += 1

#         db.commit()
#         cur.close()
#         db.close()
#         logging.info('[POST][SUCCESS] /rates ') # CHANGE TO PROPER MESSAGE
#         return jsonify({ "errorCode" : 0 , "errorDescription" : "status 200 OK" }) , 200
#     except Exception as e:
#         logging.error('[POST][FAILURE] /rates') # CHANGE TO PROPER MESSAGE
#         return jsonify({ "errorCode" : -1 , "errorDescription" : "500 Internal server error" }) , 500


@app.route("/rates",methods=["POST"])
def postrates():
    #filename = "./in/rates.xlsx"
    try:
        db = getMysqlConnection()
    except:
        return jsonify({ "errorCode" : -2 , "errorDescription" : "ERROR ESTABLISHING A DATABASE CONNECTION" }) , 200
    try:
        filename_tmp = request.get_json()
        filename = str(filename_tmp["file"])
    except:
        return jsonify({ "errorCode" : -5 , "errorDescription" : "NO PARAMETERS PASSED" }) , 500
        
    try:
        wb = load_workbook("./in/" + filename) # rates2.xlsx")
    except: 
        return jsonify({ "errorCode" : -4 , "errorDescription" : "FILE NOT FOUND" }) , 500
    try:
        ws = wb.get_active_sheet()
        cur = db.cursor()
        cur.execute('TRUNCATE TABLE Rates') 
        query = "INSERT INTO Rates (product_id, rate, scope) VALUES (%s, %s, %s)" #INSERT
    except:
        return jsonify({ "errorCode" : -5 , "errorDescription" : "DB ERROR WRONG PARAMETERS PASSED" }) , 500
        
    try:    
        row = 2
        while ws.cell(row, 1).value is not None:
            product = ws.cell(row, 1).value
            rate = ws.cell(row, 2).value
            scope = ws.cell(row, 3).value
            i_tuple = (product, rate, scope)
            cur.execute(query, i_tuple)
            row += 1
        db.commit()
        cur.close()
        db.close()
        logging.info('[POST][SUCCESS] /rates ') # CHANGE TO PROPER MESSAGE
        return jsonify({ "errorCode" : 0 , "errorDescription" : "status 200 OK" }) , 200
    except Exception as e:
        logging.error('[POST][FAILURE] /rates') # CHANGE TO PROPER MESSAGE
        return jsonify({ "errorCode" : -1 , "errorDescription" : "500 Internal server error" }) , 500

# POST /truck
# registers a truck in the system
# - provider - known provider id
# - id - the truck license plate 

@app.route('/truck/<provider_id>/<truck_lisence>', methods=['GET','POST'])
def inserttruck(provider_id, truck_lisence):
    try:
        db = getMysqlConnection()
        cur = db.cursor()  
        cur.execute('')
        cur = connection.cursor()  
        cur.execute('')
        data_query2="SELECT id FROM Provider WHERE id="+str(provider_id)
        cur = db.cursor()
        cur.execute(data_query2)
        if cur.fetchone() != None:
            data_query = "INSERT  INTO Trucks (`id`,`provider_id`) VALUES  (%s,%s)"
            data=(truck_lisence,provider_id)
            cur.execute(data_query,data)
        db.commit()
        cur.close()
        db.close()
        return jsonify("OK")
    except Exception as e:
        logging.error('[POST][FAILURE] /truck/<provider_id>/<truck_lisence>' + data_query) # CHANGE TO PROPER MESSAGE
        return str(e)
    

#FOR TESTING
@app.route('/truck2/<provider_id>/<truck_lisence>', methods=['GET','POST'])
def inserttruck2(provider_id, truck_lisence):
    try:
        db = getMysqlConnection()
    except:
        return jsonify({ "errorCode" : -2 , "errorDescription" : "ERROR ESTABLISHING A DATABASE CONNECTION" }) , 200
    try:
        cur = db.cursor()  
        data_query2="SELECT id FROM Provider WHERE id="+str(provider_id)
        cur.execute(data_query2)
        if cur.fetchone() != None:
            data_query = "INSERT  INTO Trucks (`id`,`provider_id`) VALUES  (%s,%s)"
            data=(truck_lisence,provider_id)
            cur.execute(data_query,data)
        db.commit()
        cur.close()
        db.close()
        return jsonify({ "errorCode" : 0 , "errorDescription" : "status 200 OK" }) , 200
    except Exception as e:
        logging.error('[POST][FAILURE] /truck/<provider_id>/<truck_lisence>') # CHANGE TO PROPER MESSAGE
        return jsonify({ "errorCode" : -1 , "errorDescription" : "500 Internal server error" }) , 500
# PUT /truck/{id} can be used to update provider id
# This request needs two argumnets.
# Implenting as a query string in url
# http://localhost:5000/truck/?id=222-33-111&name=new_provider_for_truck
@app.route('/truck/', methods=["PUT"])
def updatetruck():
    result_message = ""
    result_count_string = ""
    try:
        # get values from query string
        truck_id = request.args.get('id')
        provider_name = request.args.get('name')

        db = getMysqlConnection()
        cur = db.cursor()
        # get id of provider (owner of the truck id)
        querystr = "SELECT id FROM Provider WHERE name = '" + provider_name + "'"
        cur.execute(querystr)
        query_result = cur.fetchall()
        result_count_string = "   Result count: " + str(cur.rowcount)
        if cur.rowcount > 0: # test if there is at least one record
            provider_id = str(query_result[0][0])
            # count how many records have the desired truck id
            querystr = "SELECT COUNT(IF(id='" + truck_id + "',1, NULL)) 'id' FROM Trucks"
            cur.execute(querystr)
            query_result = cur.fetchall()
            if int(query_result[0][0]) > 0: # if more than 0, then update the record.
                querystr = "UPDATE Trucks SET provider_id = '" + provider_id + "' WHERE id = '" + truck_id + "'" 
                cur.execute(querystr)
                db.commit()
                result_message = "Updated Truck no: " + truck_id + " for provider: " + provider_name
            else:
                result_message = "No Truck ID with this id: " + truck_id
        else:
            result_message = "No provider with this name: " + provider_name
        cur.close()
        db.close()
        logging.info('[PUT][SUCCESS] /truck/') # CHANGE TO PROPER MESSAGE
        return result_message
    except Exception as e:
        logging.error('[PUT][FAILURE] /truck/ : QUERY:' + querystr) # CHANGE TO PROPER MESSAGE
        return str(e)

#FOR TESTING
@app.route('/truck2/', methods=["PUT"])
def updatetruck2():
    result_message = ""
    result_count_string = ""
    try:
        db = getMysqlConnection()
    except:
        return jsonify({ "errorCode" : -2 , "errorDescription" : "ERROR ESTABLISHING A DATABASE CONNECTION" }) , 200
    try:
        # get values from query string
        truck_id = request.args.get('id')
        provider_name = request.args.get('name')

        cur = db.cursor()
        # get id of provider (owner of the truck id)
        querystr = "SELECT id FROM Provider WHERE name = '" + provider_name + "'"
        cur.execute(querystr)
        query_result = cur.fetchall()
        result_count_string = "   Result count: " + str(cur.rowcount)
        if cur.rowcount > 0: # test if there is at least one record
            provider_id = str(query_result[0][0])
            # count how many records have the desired truck id
            querystr = "SELECT COUNT(IF(id='" + truck_id + "',1, NULL)) 'id' FROM Trucks"
            cur.execute(querystr)
            query_result = cur.fetchall()
            if int(query_result[0][0]) > 0: # if more than 0, then update the record.
                querystr = "UPDATE Trucks SET provider_id = '" + provider_id + "' WHERE id = '" + truck_id + "'" 
                cur.execute(querystr)
                db.commit()
                result_message = "Updated Truck no: " + truck_id + " for provider: " + provider_name
            else:
                result_message = "No Truck ID with this id: " + truck_id
        else:
            result_message = "No provider with this name: " + provider_name
        cur.close()
        db.close()
        logging.info('[PUT][SUCCESS] /truck/') # CHANGE TO PROPER MESSAGE
        return jsonify({ "errorCode" : 0 , "errorDescription" : "status 200 OK"  , "result": result_message}) , 200 
    except Exception as e:
        logging.error('[PUT][FAILURE] /truck/ : QUERY:') # CHANGE TO PROPER MESSAGE
        return jsonify({ "errorCode" : -1 , "errorDescription" : "500 Internal server error" }) , 500

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
    try:
        #return id
        #return id+str(request.args.get('from')+str(request.args.get('to')))
        db = getMysqlConnection()
        cur = db.cursor()  
        cur.execute('SELECT id , provider_id FROM Trucks WHERE id='+'"' + id + '"')
        results = cur.fetchall()
        return str(results)
        #HERE WE SHOULD MAKE A REQUEST TO WEIGHT API AND GET WITH THE ID BETWEEN DATES BY ID ?
        db.commit()
        cur.close()
        db.close()
        logging.info('[GET][SUCCESS] /truck/<id>') # CHANGE TO PROPER MESSAGE
        tempJson = { "id"}
        return "OK"
    except Exception as e:
        logging.error('[GET][FAILURE] /truck/<id>') # CHANGE TO PROPER MESSAGE
        return str(e)


#FOR TESTING
@app.route('/truck2/<id>', methods=["GET"])
def truckinfo2(id):
    try:
        db = getMysqlConnection()
    except:
        return jsonify({ "errorCode" : -2 , "errorDescription" : "ERROR ESTABLISHING A DATABASE CONNECTION" }) , 200
    try:
        #return id
        #return id+str(request.args.get('from')+str(request.args.get('to')))
        cur = db.cursor()  
        cur.execute('SELECT id , provider_id FROM Trucks WHERE id='+'"' + id + '"')
        results = cur.fetchall()
        return str(results)
        #HERE WE SHOULD MAKE A REQUEST TO WEIGHT API AND GET WITH THE ID BETWEEN DATES BY ID ?
        db.commit()
        cur.close()
        db.close()
        logging.info('[GET][SUCCESS] /truck/<id>') # CHANGE TO PROPER MESSAGE
        tempJson = { "id"}
        return jsonify({ "errorCode" : 0 , "errorDescription" : "status 200 OK" }) , 200
    except Exception as e:
        logging.error('[GET][FAILURE] /truck/<id>') # CHANGE TO PROPER MESSAGE
        return jsonify({ "errorCode" : -1 , "errorDescription" : "500 Internal server error" }) , 500

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
@app.route('/bill/<id>', methods=["GET"])
def getbilling(id):
    try:
        # id
        result={"id" : id}
        # name
        name = bill.get_provider_name(id)
        result.update({"name" : name})
        # t1 & t2
        now = datetime.now()
        t1 = now.strftime("%Y%m01000000")
        t2 = now.strftime("%Y%m%d%H%M%S")
        if request.args.get('t1')!=None:
            t1 = request.args.get('t1')
        if request.args.get('t2')!=None:
            t2 = request.args.get('t2')
        result.update({ "from" : t1 })
        result.update({ "to" : t1 })
        
        trucks_list=bill.find_providers_trucks()
        weights_list=bill.get_all_sessions_in_array(t1,t2)
        rates_dictionary=bill.get_rates()
        # sessionCount
        GlobalSessionsCount=0
        # products
        products={}
        # truck_in_weights
        trucks_in_weights=[]
        # foreach truck - look for its sessions/weights
        for truck in trucks_list:
            truck_number = str(truck[0])
            truck_sessions_count=0
            if truck_number not in trucks_in_weights:
                trucks_in_weights.append(truck_number)
            universalSessionsCount += truck_sessions.len()
            for weight in weights_list:
                if weight["truck"] == truck_number:
                    truck_sessions_count += 1
                    if weight["produce"] not in products.values():
                        products_and_neto_weihgt.update({'produce' : weight["produce"] , 'count' : 1 , 'amount' : weight["neto"] , })
                    else:
                        val=weight["neto"]+products_and_neto_weihgt[weight["produce"]]
                        products_and_neto_weihgt.update({'produce' : val })
                    


                        

                        
                
        db.commit()
        cur.close()
        db.close()
        logging.info('[GET][SUCCESS] /bill/<id>?from=<t1>&to=<t2>') # CHANGE TO PROPER MESSAGE
        
    except Exception as e:
        logging.error('[GET][FAILURE] /bill/<id>?from=<t1>&to=<t2>') # CHANGE TO PROPER MESSAGE
        return str(e)

@app.route('/getlogs', methods=["GET"])
def getlogs():
    try:
        with open('app.log', 'r') as file:
            return file.read()
    except Exception as e:
        logging.error('file not found')
        return str(e)

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0')
