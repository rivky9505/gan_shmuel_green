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
def test(sb):
        if sb == "master":
                cmdChmod = 'chmod +x ../Tests/test.bash'
                os.system(cmdChmod)
                sleep(2)
                res = subprocess.call("../Tests/test.bash %s" % ("-m"), shell=True)
                print (res)
                print ("*****END*****")
        if sb == "weight":
                cmdChmod = 'chmod +x ../Tests/test.bash'
                os.system(cmdChmod)
                sleep(2)
                res = subprocess.call("../Tests/test.bash %s" % ("-w"), shell=True)
                print (res)
                print ("*****END*****")
        if sb == "provider":
                cmdChmod = 'chmod +x ../Tests/test.bash'
                os.system(cmdChmod)
                sleep(2)
                res = subprocess.call("../Tests/test.bash %s" % ("-p"), shell=True)
                print (res)
                print ("*****END*****")

@app.route('/')
def api():
        strd = "Happy birthday"
        return str(strd.find("py"))

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