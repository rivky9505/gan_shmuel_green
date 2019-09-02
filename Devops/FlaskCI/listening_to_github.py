from flask import json, request, Flask

app = Flask(__name__)

@app.route('/github', methods=['POST'])
def api_gh_message():
    if request.headers['Content-Type'] == 'application/json':
        info = json.dumps(request.json)
        print (info)
        return info

if __name__ == '__main__':
    app.run(debug=True)