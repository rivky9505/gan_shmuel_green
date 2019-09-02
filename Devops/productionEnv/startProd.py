import os
from time import sleep

def runEnv():
    DCDown = 'docker-compose down'
    DCUp = 'docker-compose up -d --build'
    cmd = 'pwd'
    os.system(cmd)
    sleep(2)
    os.system(DCDown)
    sleep(2)
    os.system(DCUp)

os.chdir('./W')
runEnv()

sleep(3)

os.chdir('../P')
runEnv()
