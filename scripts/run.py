from eve import Eve
from flask import jsonify
import subprocess
app = Eve()

@app.route('/simulate/test', methods=['GET'])
def simulate_by_armory():
    print(subprocess.call(["simc", "armory=us,emerald-dream,sarrial", "json2=sarrial.json"]))
    with open('sarrial.json') as data_file:    
        data = json.load(data_file)
    return jsonify(data)
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug = False)