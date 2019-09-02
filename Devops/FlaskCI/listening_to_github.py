from flask import json, request, Flask

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
        print (info)
        print (branch)
        return info

if __name__ == '__main__':
    app.run(debug=True)