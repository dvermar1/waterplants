import flask
from flask import request
from flask import jsonify

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    return "<h1>Distant Reading Archive</h1><p>This site is a prototype API for distant reading of science fiction novels.</p>"

@app.route('/water', methods=['POST'])
def water_plants():
    var1 = request.args.get('key1')
    var2 = request.args.get('key2')

    print (var1 + "-----" + var2)
    resp = jsonify(success=True)
    return resp

app.run(host="0.0.0.0")
