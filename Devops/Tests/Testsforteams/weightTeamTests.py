#!/bin/python3
from datetime import datetime 
import os
os.system('export URI=http://localhost:8081/ && pytest ../ > errorLogWeight.txt')