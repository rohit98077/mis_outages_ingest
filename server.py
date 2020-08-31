'''
This is the web server that acts as a service that creates outages raw data
'''
import argparse
import datetime as dt
from src.appConfig import getConfig
from src.rawDataCreators.outagesRawDataCreator import createOutageEventsRawData
from flask import Flask

app = Flask(__name__)

# get application config
appConfig = getConfig()

# Set the secret key to some random bytes
app.secret_key = appConfig['flaskSecret']


@app.route('/')
def hello():
    return "This is the web server that acts as a service that creates outages raw data"


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(appConfig['flaskPort']), debug=True)
