from flask import Flask, render_template, request

#ci runs on port 80
app = Flask(__name__)
if __name__ == '__main__':
        app.run(host='0.0.0.0', port='8085')


@app.route('/push')
def push():
        return 0

@app.route('/commit')
def commit():
        return 0

@app.route('/deploy')
def deploy():
        #test
        


        #pull
        return 0
