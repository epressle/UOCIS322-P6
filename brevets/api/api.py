import os
from pymongo import MongoClient
from flask import Flask, request, jsonify
from flask_restful import Resource, Api


app = Flask(__name__)
api = Api(app)

client = MongoClient('mongodb://' + os.environ['MONGODB_HOSTNAME'], 27017)
db = client.brevetdb

def convert_to_csv(data):
    return data

def get_data(type_arg='all'):
    if type_arg == 'close':
        entries = db.brevetdb.find({}, {'_id': 0, 'brev_distance': 0, 'open_times': 0, 'kms': 0})
    elif type_arg == 'open':
        entries = db.brevetdb.find({}, {'_id': 0, 'brev_distance': 0, 'close_times': 0, 'kms': 0})
    else:
        entries = db.brevetdb.find({}, {'_id': 0, 'brev_distance': 0, 'kms': 0})
    app.logger.debug("entries = " + str(list(entries)))
    return list(entries)


class ListAll(Resource):
    def get(self, ext='json'):
        entries = get_data('all')
        print(entries)
        if ext == 'csv':
            return convert_to_csv(entries)
        else:
            return entries

class ListOpenOnly(Resource):
    def get(self, ext='json'):
        entries = get_data('open')
        print(entries)
        if ext == 'csv':
            return convert_to_csv(entries)
        else:
            return entries

class ListCloseOnly(Resource):
    def get(self, ext='json'):
        entries = get_data('close')
        print(entries)
        if ext == 'csv':
            return convert_to_csv(entries)
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
