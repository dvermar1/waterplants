import flask
import RPi.GPIO as GPIO
import time
import asyncio
from flask import request
from flask import jsonify
from flask_cors import CORS
from okta_jwt_verifier import AccessTokenVerifier

app = flask.Flask(__name__)
CORS(app)
app.config["DEBUG"] = True

jwt_verifier = AccessTokenVerifier(issuer="https://dev-94896909.okta.com/oauth2/default",audience='api://default')

@app.route('/', methods=['GET'])
async def home():
    isAuthorized = await is_authorized(request)
    if not isAuthorized:
        return "Unauthorized", 401
    return "<h1>Distant Reading Archive</h1><p>This site is a prototype API for distant reading of science fiction novels.</p>"

@app.route('/water', methods=['POST'])
async def water_plants():
    isAuthorized = await is_authorized(request)
    if not isAuthorized:
        return "Unauthorized", 401

    var1 = request.args.get('key1')
    var2 = request.args.get('key2')

    print (var1 + "-----" + var2)

    #pump_on()

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

async def is_authorized(request):
    """Get access token from authorization header."""
    try:
        token = request.headers.get("Authorization").split("Bearer ")[1]
        #print(token)
        await jwt_verifier.verify(token)
        return True
    except Exception:
        return False

if __name__ == "__main__":
    app.run()
