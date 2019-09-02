from flask import json, request, Flask, debughelpers

app = Flask(__name__)

@app.route('/github', methods=['POST'])
def api_gh_message():
    if request.headers['Content-Type'] == 'application/json':
        info = json.dumps(request.json)
        
        branch = info.ref
        print (info)
        print (branch)
        return info

if __name__ == '__main__':
    app.run(debug=True)