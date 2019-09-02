from flask import Flask, request, render_template ,jsonify  
#!Author  Roi Alfassi

app = Flask(__name__)


@app.route("/weight/healthlog" , methods=['GET'])
def whealthlog:
    #TODO add path to the log file in order for us to get the log file
    with open('path', 'r') as file:
    data = []
    for line in file:
        data.append(line.strip() + "\n")
    return jsonify(data)



@app.route("/provider/healthlog" , methods=['GET'])
def whealthlog: 
    #TODO add path to the log file in order for us to get the log file
    with open('path', 'r') as file:
    data = []
    for line in file:
        data.append(line.strip() + "\n")
    return jsonify(data)

##TODO add host Ktovet 
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')