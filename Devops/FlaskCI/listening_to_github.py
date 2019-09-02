from flask import json, request, Flask
from startProd import mainFunc, testFunc

app = Flask(__name__)

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
                mainFunc()
        print(branch)
        return info

if __name__ == '__main__':
    app.run(host="0.0.0.0")