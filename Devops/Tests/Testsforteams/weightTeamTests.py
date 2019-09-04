#!/bin/python
from datetime import datetime 
import os
os.system('export URI=http://localhost:8081/ && pytest ../weight > errorLogWeight.txt')