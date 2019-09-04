#!/bin/python
from datetime import datetime 
import os
os.system('export URI=http://localhost:8089/ && pytest ../ > errorLogProvider.txt')