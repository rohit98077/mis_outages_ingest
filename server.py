'''
This is the web server that acts as a service that creates outages raw data
'''
import datetime as dt
from src.appConfig import getConfig
from src.rawDataCreators.outagesRawDataCreator import createOutageEventsRawData
from flask import Flask, request, jsonify
from src.repos.outages.outagesRepo import OutagesRepo

app = Flask(__name__)

# get application config
appConfig = getConfig()

# Set the secret key to some random bytes
app.secret_key = appConfig['flaskSecret']


@app.route('/')
def hello():
    return "This is the web server that acts as a service that creates outages raw data"


@app.route('/raw_outages', methods=['POST'])
def createRawOutages():
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
        return jsonify({'message': 'raw data creation was not success'}), 500


@app.route('/outages', methods=['GET'])
def getOutages():
    # get start and end dates from request query parameters
    try:
        startDateStr = request.args.get('startDate', None, type=str)
        endDateStr = request.args.get('endDate', None, type=str)
        startDate = dt.datetime.strptime(startDateStr, '%Y-%m-%d')
        endDate = dt.datetime.strptime(endDateStr, '%Y-%m-%d')
    except Exception as ex:
        return jsonify({'message': 'Unable to parse start and end dates of this request body'}), 400

    # get the instance of outages repository
    outagesRepo = OutagesRepo(appConfig['appDbConStr'])

    # fetch outage events from reporting software db
    outages = outagesRepo.getOutages(startDate, endDate)
    return jsonify({'message': 'Success!!!', 'data': outages, 'startDate': startDate, 'endDate': endDate})


@app.route('/transElOutages', methods=['GET'])
def getTransElOutages():
    # get start and end dates from request query parameters
    try:
        startDateStr = request.args.get('startDate', None, type=str)
        endDateStr = request.args.get('endDate', None, type=str)
        startDate = dt.datetime.strptime(startDateStr, '%Y-%m-%d')
        endDate = dt.datetime.strptime(endDateStr, '%Y-%m-%d')
    except Exception as ex:
        return jsonify({'message': 'Unable to parse start and end dates of this request body'}), 400

    # get the instance of outages repository
    outagesRepo = OutagesRepo(appConfig['appDbConStr'])

    # fetch outage events from reporting software db
    outages = outagesRepo.getTransElOutages(startDate, endDate)
    return jsonify({'message': 'Success!!!', 'data': outages, 'startDate': startDate, 'endDate': endDate})


@app.route('/majorGenOutages', methods=['GET'])
def getMajorGenOutages():
    # get start and end dates from request query parameters
    try:
        startDateStr = request.args.get('startDate', None, type=str)
        endDateStr = request.args.get('endDate', None, type=str)
        startDate = dt.datetime.strptime(startDateStr, '%Y-%m-%d')
        endDate = dt.datetime.strptime(endDateStr, '%Y-%m-%d')
    except Exception as ex:
        return jsonify({'message': 'Unable to parse start and end dates of this request body'}), 400

    # get the instance of outages repository
    outagesRepo = OutagesRepo(appConfig['appDbConStr'])

    # fetch outage events from reporting software db
    outages = outagesRepo.getMajorGenOutages(startDate, endDate)
    return jsonify({'message': 'Success!!!', 'data': outages, 'startDate': startDate, 'endDate': endDate})


@app.route('/longTimeUnrevForced', methods=['GET'])
def getLongTimeUnrevivedForcedOutages():
    # get start and end dates from request query parameters
    try:
        startDateStr = request.args.get('startDate', None, type=str)
        endDateStr = request.args.get('endDate', None, type=str)
        startDate = dt.datetime.strptime(startDateStr, '%Y-%m-%d')
        endDate = dt.datetime.strptime(endDateStr, '%Y-%m-%d')
    except Exception as ex:
        return jsonify({'message': 'Unable to parse start and end dates of this request body'}), 400

    # get the instance of outages repository
    outagesRepo = OutagesRepo(appConfig['appDbConStr'])

    # fetch outage events from reporting software db
    outages = outagesRepo.getLongTimeUnrevivedForcedOutages(startDate, endDate)
    return jsonify({'message': 'Success!!!', 'data': outages, 'startDate': startDate, 'endDate': endDate})


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(appConfig['flaskPort']), debug=True)
