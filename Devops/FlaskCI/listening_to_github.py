from flask import json, request, Flask, debughelpers

app = Flask(__name__)

def find_str(s, char):
    index = 0

    if char in s:
        c = char[0]
        for ch in s:
            if ch == c:
                if s[index:index+len(char)] == char:
                    return index

            index += 1

    return -1

@app.route('/')
def api():
    strd = "Happy birthday"
    return str(strd.find("py"))

@app.route('/github', methods=['POST'])
def api_gh_message():
    if request.headers['Content-Type'] == 'application/json':
        info = json.dumps(request.json)
        branch = info[info.find("refs/heads/Devops_branch")+10:info.find("refs/heads/Devops_branch")+20]   
        print (info)
        print (branch)
        return info

if __name__ == '__main__':
    app.run(debug=True)