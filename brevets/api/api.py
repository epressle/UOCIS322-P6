import os
from pymongo import MongoClient
from flask import Flask, request, jsonify
from flask_restful import Resource, Api
import json

app = Flask(__name__)
api = Api(app)

client = MongoClient('mongodb://' + os.environ['MONGODB_HOSTNAME'], 27017)
db = client.brevetdb

def csv_convert(data, out):
    str = ""
    app.logger.debug(type(data))
    if out == 'open':
        str += "open_times\n"
    elif out == 'close':
        str += "close_times\n"
    else:
        str += "open_times,close_times\n"
    return str


def get_data(type_arg='all'):
    if type_arg == 'close':
        entries = db.brevetdb.find({}, {'_id': 0, 'brev_distance': 0, 'open_times': 0, 'kms': 0})
    elif type_arg == 'open':
        entries = db.brevetdb.find({}, {'_id': 0, 'brev_distance': 0, 'close_times': 0, 'kms': 0})
    else:
        entries = db.brevetdb.find({}, {'_id': 0, 'brev_distance': 0, 'kms': 0})
    entries = str(list(entries))
    app.logger.debug("entries in get_data = " + entries)
    return entries


class ListAll(Resource):
    def get(self, ext='json'):
        entries = get_data('all')
        if ext == 'csv':
            return csv_convert(entries, 'all')
        else:
            return entries

class ListOpenOnly(Resource):
    def get(self, ext='json'):
        entries = get_data('open')
        if ext == 'csv':
            return csv_convert(entries, 'open')
        else:
            return entries

class ListCloseOnly(Resource):
    def get(self, ext='json'):
        entries = get_data('close')
        if ext == 'csv':
            return csv_convert(entries, 'close')
        else:
            return entries


# Create routes
# Another way, without decorators
api.add_resource(ListAll, '/listAll', '/listAll/<string:ext>')
api.add_resource(ListOpenOnly, '/listOpenOnly', '/listOpenOnly/<string:ext>')
api.add_resource(ListCloseOnly, '/listCloseOnly', '/listCloseOnly/<string:ext>')

# Run the application
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
