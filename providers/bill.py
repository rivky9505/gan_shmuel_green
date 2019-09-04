from flask import Flask, request, jsonify, Response ,send_from_directory
from flask_cors import CORS, cross_origin
from openpyxl import Workbook
from datetime import datetime

import json
import mysql.connector
import logging
import csv
import xlsxwriter
import requests
import ctypes

import app


def get_all_sessions_in_array(t1,t2):
    # req_sting="http://green.develeap.com:8080/weight/?from="+t1+"&to="+t2+"&filter=out"
    # resp = requests.get(req_sting)
    # if resp.status_code != 200:
    # # This means something went wrong.
    #     return str('GET /item/ {}'.format(resp.status_code))      
    # return str(resp)
    return ( json.load(open("weight.json","r")) )

def find_providers_trucks(id):
    db = app.getMysqlConnection()
    cur = db.cursor() 
    query= "SELECT id FROM Trucks WHERE provider_id = " + str(id)
    cur.execute(query)
    return cur.fetchall() 

def make_get_item_api(truck_number,t1,t2):
    # req_sting="http://green.develeap.com:8080/item/"+truck_number+"?from="+t1+"&to="+t2
    # resp = requests.get(req_sting)
    # if resp.status_code != 200:
    # # This means something went wrong.
    #     return str('GET /item/ {}'.format(resp.status_code))      
    # return resp 
    return ( json.load(open("itam.json","r")) )



def get_provider_name(id):
    db = app.getMysqlConnection()
    cur = db.cursor()
    query= "select name from Provider where id="+str(id)
    cur.execute(query)
    return cur.fetchone() 
    
def get_rates():
    db = app.getMysqlConnection()
    cur = db.cursor(dictionary=True)
    query= "select * from Rates"
    cur.execute(query)
    return cur.fetchall()