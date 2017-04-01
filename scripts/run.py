from eve import Eve
import flask
import os
import subprocess
app = Eve()

@app.route('/test', methods=['GET'])
def test_endpoint():
    subprocess.call(["simc", "armory=us,emerald-dream,sarrial", "json2=sarrial.json"])
    return "Something"

@app.route('/test', methods=['POST'])
def test_endpoint_post():
    request_json = flask.request.get_json()
    if request_json['realm'] and request_json['name']:
        subprocess.call(["simc", "armory=us," + request_json['realm'] + "," + 
            request_json['name'], "json2=result.json"])
    return get_result_json()

@app.route('/simulate/test', methods=['GET'])
def simulate_by_armory():
    subprocess.call(["simc", "armory=us,emerald-dream,sarrial", "json2=result.json"])
    return get_result_json()

def get_result_json():
    with open('result.json') as result_json:    
        data = flask.json.load(result_json)
    return flask.jsonify(data)

if __name__ == '__main__':
    with open("/root/.simc_apikey", "w") as f: 
        f.write(os.environ['APIKEY']) 
    app.run(host='0.0.0.0', debug = False)