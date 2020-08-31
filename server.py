'''
This is the web server that acts as a service that creates outages raw data
'''
import datetime as dt
from src.appConfig import getConfig
from src.rawDataCreators.outagesRawDataCreator import createOutageEventsRawData
from flask import Flask, request, jsonify

app = Flask(__name__)

# get application config
appConfig = getConfig()

# Set the secret key to some random bytes
app.secret_key = appConfig['flaskSecret']


@app.route('/')
def hello():
    return "This is the web server that acts as a service that creates outages raw data"


@app.route('/raw_outages', methods=['POST'])
def create_raw_outages():
    # get start and end dates from post request body
    reqData = request.get_json()
    try:
        startDate = dt.datetime.strptime(reqData['startDate'], '%Y-%m-%d')
        endDate = dt.datetime.strptime(reqData['endDate'], '%Y-%m-%d')
    except Exception as ex:
        return jsonify({'message': 'Unable to parse start and end dates of this request body'}), 400
    # create outages raw data between start and end dates
    isRawDataCreationSuccess = createOutageEventsRawData(
        appConfig, startDate, endDate)
    if isRawDataCreationSuccess:
        return jsonify({'message': 'raw data creation successful!!!', 'startDate': startDate, 'endDate': endDate})
    else:
        return jsonify({'message': 'raw data creation was not success'}), 400


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(appConfig['flaskPort']), debug=True)
