from flask import Flask, render_template, request, jsonify
import requests
import os
import json

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def home():
    return render_template('index.html')

@app.route('/list', methods=['POST'])
def listEntries():
    out = request.form.get('out')
    app.logger.debug("Out = " + str(out))
    k = request.form.get('number')

    if k is None or int(k) < 0:
        k = '0'

    app.logger.debug("k = " + k)
    output = request.form.get('types')
    if output is None:
        output = 'json'
    app.logger.debug("output = " + str(output))
    data = requests.get("http://" + os.environ['BACKEND_ADDR'] + ":" + os.environ['BACKEND_PORT'] + "/" + out + "/" + output + "?top=" + k)
    app.logger.debug(data.text)
    ret = data.text
    return jsonify(ret)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
