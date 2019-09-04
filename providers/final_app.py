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



@app.route('/provider', methods=['PUT'])
def putprovider22():
    try:
        db = getMysqlConnection()
    except:
        return jsonify({ "errorCode" : -2 , "errorDescription" : "ERROR ESTABLISHING A DATABASE CONNECTION" }) , 200
    try:
        json = request.get_json()
        id = str(json["id"])
        newname = str(json["newname"])
        #newname = request.form["newname"]
    except:
        return jsonify({ "errorCode" : -5 , "errorDescription" : "ERROR/WRONG NO PARAMETERS PASSED" }) , 200
    try:    
        cur = db.cursor()  
        cur.execute('UPDATE Provider SET name = ' + '"' +str(newname)+ '"' + ' WHERE id =' + id)
    except:
        return jsonify({ "errorCode" : -3 , "errorDescription" : "ERROR DB QUERY EXECUTION" }) , 200
    try:
        db.commit()
        cur.close()
        db.close()
        logging.info('[PUT][SUCCESS] provider/<id>') 
        return jsonify({ "errorCode" : 0 , "errorDescription" : "status 200 OK" }) , 200
    except Exception as e:
        logging.error('[PUT][FAILURE] provider/<id>') 
        return jsonify({ "errorCode" : -1 , "errorDescription" : "500 Internal server error" }) , 500
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
        return jsonify({ "errorCode" : -3 , "errorDescription" : "ERROR EXECUTING QUERY IN DATABASE" }) , 200
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

@app.route('/truck', methods=["PUT"])
def updatetruck():
    # get values from query string
    result_message = ""
    result_count_string = ""
    truck_id = ""
    provider_name = ""
    if request.args.get('id') != None:
        truck_id = request.args.get('id')
    else:
        logging.error('[PUT][FAILURE] /truck/ : USER ERROR : MISSING PARAMETER IN URL QUERY')
        return jsonify({ "errorCode" : -5 , "errorDescription" : "USER ERROR MISSING PARAMETER IN URL QUERY" }) , 200

    if request.args.get('name'):
        provider_name = request.args.get('name')
    else:
        logging.error('[PUT][FAILURE] /truck/ : USER ERROR : MISSING PARAMETER IN URL QUERY')
        return jsonify({ "errorCode" : -5 , "errorDescription" : "USER ERROR MISSING PARAMETER IN URL QUERY" }) , 200
    
    try:
        db = getMysqlConnection()
    except:
        return jsonify({ "errorCode" : -2 , "errorDescription" : "ERROR ESTABLISHING A DATABASE CONNECTION" }) , 200
    
    try:
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
                cur.close()
                db.close()
                result_message = "[PUT][SUCCESS] /truck/ : Updated Truck no: " + truck_id + " for provider: " + provider_name
                logging.info(result_message)
                return jsonify({ "errorCode" : 0 , "errorDescription" : "status 200 OK"  , "result": result_message}) , 200 
            else:
                result_message = "No Truck ID with this id: " + truck_id
                logging.info(result_message)
                return jsonify({ "errorCode" : -5 , "errorDescription" : "status 200 OK"  , "result": result_message}) , 200 
        else:
            result_message = "No provider with this name: " + provider_name
            logging.info(result_message)
            return jsonify({ "errorCode" : -5 , "errorDescription" : "status 200 OK"  , "result": result_message}) , 200 
    except Exception as e:
        logging.error('[PUT][FAILURE] /truck/ : QUERY:' + querystr)
        return jsonify({ "errorCode" : -1 , "errorDescription" : "500 Internal server error" }) , 500


@app.route('/truck/<id>', methods=["GET"]) #?from=t1&to=t2
def truckinfo(id):
    try:
        fromm = str(request.args.get('from'))
        to = str(request.args.get('to'))
        resp = requests.get('http://green.develeap.com:8080/item/'+ id +' ?from='+ fromm +'&to='+ to +'')
        json_content = json.dumps(resp.json())
        return '{ "errorCode" : 0 , "errorDescription" : "status 200 OK" , "data" :' + str(json_content) + ' }' , 200
         
        #return id
        #return id+str(request.args.get('from')+str(request.args.get('to')))
        #db = getMysqlConnection()
        #cur = db.cursor() 
        #cur.execute('SELECT id , provider_id FROM Trucks WHERE id='+'"' + id + '"')
        #results = cur.fetchall()
        #return str(results)
        ##HERE WE SHOULD MAKE A REQUEST TO WEIGHT API AND GET WITH THE ID BETWEEN DATES BY ID ?
        #db.commit()
        #cur.close()
        #db.close()
        #logging.info('[GET][SUCCESS] /truck/<id>') # CHANGE TO PROPER MESSAGE
        #tempJson = { "id"}
        #return "OK"
    except Exception as e:
        logging.error('[GET][FAILURE] /truck/<id>') # CHANGE TO PROPER MESSAGE
        return jsonify({ "errorCode" : -1 , "errorDescription" : "500 Internal server error" }) , 500


@app.route('/provider/<provider_name>', methods=['POST'])
def insert_provider(provider_name):
    try:
        db = getMysqlConnection()
    except:
        return jsonify({ "errorCode" : -2 , "errorDescription" : "ERROR ESTABLISHING A DATABASE CONNECTION" }) , 200

    try:
        query_string = "INSERT INTO Provider (name) "
        query_string += "SELECT * FROM (SELECT '" + provider_name + "') AS tmp "
        query_string += "WHERE NOT EXISTS ("
        query_string += "SELECT name FROM Provider WHERE name = '" + provider_name + "'"
        query_string += ") LIMIT 1;"
        cur = db.cursor()  
        cur.execute(query_string)
        db.close()
        logging.info("[POST][SUCCESS] provider/%s", (provider_name,))
        return jsonify({ "errorCode" : 0 , "errorDescription" : "status 200 OK"  , "result": "MYSQL query completed"}) , 200
    except Exception as e:
        logging.info('[POST][FAILURE] while trying:', str(e))
        return jsonify({ "errorCode" : -1 , "errorDescription" : "500 Internal server error" }) , 500   
