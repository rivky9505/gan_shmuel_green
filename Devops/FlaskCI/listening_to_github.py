from flask import json, request, Flask
import os
from time import sleep
import subprocess

app = Flask(__name__)

def runEnv():
    DCDown = 'sudo docker-compose down'
    DCUp = 'sudo docker-compose up -d --build'
    cmd = 'pwd'
    os.system(cmd)
    sleep(2)
    os.system(DCDown)
    sleep(2)
    os.system(DCUp)
def mainFunc():
    os.chdir('/home/ubuntu/prod')
    deleteRollback = 'rm -rf rollback/gan_shmuel_green/'
    copytoRollback = 'cp -r gan_shmuel_green/ rollback/'
    deleteRepo = 'rm -rf gan_shmuel_green/'
    gitcloneCMD = 'git clone https://github.com/greendeveleap/gan_shmuel_green.git'
    rmDCfile = 'rm docker-compose.yml'
    copyGlobalDCF = 'cp /home/ubuntu/src/dockerComposeFiles/dcFIles/PP/docker-compose.yml /home/ubuntu/prod/gan_shmuel_green/providers/docker-compose.yml'
    copyGlobalDCFW = 'cp /home/ubuntu/src/dockerComposeFiles/dcFIles/WP/docker-compose.yml /home/ubuntu/prod/gan_shmuel_green/weight/docker-compose.yml'
    os.system(deleteRollback)
    print("Delete rollback version")
    sleep(3)
    os.system(copytoRollback)
    print("Copying new rollback image")
    sleep(3)
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
def test(sb):
        cmdChmod = 'chmod +x /home/ubuntu/temp/gan_shmuel_green/Devops/Tests/test.bash'
        os.system(cmdChmod)
        sleep(2)
        if sb == "master":
                res = subprocess.call("../Tests/test.bash %s" % ("-m"), shell=True)
                print (res)
                print ("*****END*****")
        if sb == "weight":
                res = subprocess.call("../Tests/test.bash %s" % ("-w"), shell=True)
                print (res)
                print ("*****END*****")
        if sb == "provider":
                res = subprocess.call("../Tests/test.bash %s" % ("-p"), shell=True)
                print (res)
                print ("*****END*****")

def rollBack():
        os.chdir('/home/ubuntu/prod')
        copyfromprodtotemp = 'cp -r gan_shmuel_green/ tempforrb/'
        deleteRepoFromProd = 'rm -rf gan_shmuel_green/'
        copyfromrbtoprod = 'cp -r rollback/gan_shmuel_green/ gan_shmuel_green/'
        deleteRollback = 'rm -rf rollback/gan_shmuel_green/'
        copyfromtemptorb = 'cp -r tempforrb/gan_shmuel_green/ rollback/'
        deletefromtemp = 'rm -rf tempforrb/gan_shmuel_green/'
        os.system(copyfromprodtotemp)
        print("copying from prod to temp")
        sleep(3)
        os.system(deleteRepoFromProd)
        print("delete from prod")
        sleep(3)
        os.system(copyfromrbtoprod)
        print("Copy from rollback to prod")
        sleep(3)
        os.system(deleteRollback)
        print("Delete from rollback")
        sleep(3)
        os.system(copyfromtemptorb)
        print("copy from temp to rollback")
        sleep(3)
        os.system(deletefromtemp)
        print("delete from temp")
        sleep(3)
        os.chdir('/home/ubuntu/prod/gan_shmuel_green/providers')
        runEnv()
        sleep(5)
        os.chdir('/home/ubuntu/prod/gan_shmuel_green/weight')
        runEnv()

@app.route('/')
def api():
        strd = "Happy birthday"
        return str(strd.find("py"))

@app.route('/rollback')
def roll_back():
        rollBack()
        return "roll back done"

@app.route('/github', methods=['POST'])
def api_gh_message():
    if request.headers['Content-Type'] == 'application/json':
        info = json.dumps(request.json)
        print (info)
        TempBranch = info[info.find("refs/heads")+10:info.find("refs/heads")+50]
        branch = TempBranch[1:TempBranch.find("repo")-4]
        if branch == "master":
                print ("its a master")
                test("master")
                mainFunc()
        if branch == "weight":
                print ("its a weight")
                test("weight")
        if branch == "providers_branch":
                print ("its a provider")
                test("provider")
        print(branch)
        return info

if __name__ == '__main__':
    app.run(host="0.0.0.0",port="8085")