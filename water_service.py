import flask
import RPi.GPIO as GPIO
import time
from flask import request
from flask import jsonify
from flask_cors import CORS
from okta_jwt_verifier import JWTVerifier

app = flask.Flask(__name__)
CORS(app)
app.config["DEBUG"] = True

jwt_verifier = JWTVerifier(issuer="https://dev-94896909.okta.com/oauth2/default",
                           client_id="0oa1ebw5njlc9Tgnz5d7",
                           audience='api://default')

@app.route('/', methods=['GET'])
def home():
    if not is_authorized(request):
        return "Unauthorized", 401
    return "<h1>Distant Reading Archive</h1><p>This site is a prototype API for distant reading of science fiction novels.</p>"

@app.route('/water', methods=['POST'])
def water_plants():
    if not is_authorized(request):
        return "Unauthorized", 401

    var1 = request.args.get('key1')
    var2 = request.args.get('key2')

    print (var1 + "-----" + var2)

    pump_on()

    resp = jsonify(success=True)
    return resp

def init_output(pin):
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(pin, GPIO.OUT)

def pump_on(pump_pin = 7):
    init_output(pump_pin)
    GPIO.output(pump_pin, GPIO.LOW)
    time.sleep(10)
    GPIO.output(pump_pin, GPIO.HIGH)

def is_authorized(request):
    """Get access token from authorization header."""
    try:
        token = request.headers.get("Authorization").split("Bearer ")[1]
        return is_access_token_valid(token, config["issuer"], config["client_id"])
    except Exception:
        return False

if __name__ == "__main__":
    app.run()
