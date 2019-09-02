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

os.chdir('/home/ubuntu/prod')
deleteRepo = 'rm -rf gan_shmuel_green/'
gitcloneCMD = 'git clone https://github.com/greendeveleap/gan_shmuel_green.git'
rmDCfile = 'rm docker-compose.yml'
copyGlobalDCF = 'cp /home/ubuntu/src/dockerComposeFiles/dcFIles/PP/docker-compose.yml /home/ubuntu/prod/gan_shmuel_green/providers/docker-compose.yml'
copyGlobalDCFW = 'cp /home/ubuntu/src/dockerComposeFiles/dcFIles/WP/docker-compose.yml /home/ubuntu/prod/gan_shmuel_green/weight/docker-compose.yml'
os.system(deleteRepo)
print("Repo deleted from prod dir")
sleep(3)
os.system(gitcloneCMD)
print("git clone cmd executed")
sleep(5)
os.chdir('/home/ubuntu/prod/gan_shmuel_green/providers')
sleep(2)
os.system(rmDCfile)
print("DC file removed from repo")
sleep(2)
os.system(copyGlobalDCF)
print ("New DC file added to the repo")
sleep(2)
runEnv()
sleep(3)
os.chdir('/home/ubuntu/prod/gan_shmuel_green/weight')
sleep(2)
os.system(rmDCfile)
sleep(2)
os.system(copyGlobalDCFW)
sleep(2)
runEnv()
