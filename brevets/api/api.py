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
    num = request.args.get('top', type=int)
    if num is None or num <= 0:
        return ""
    str = ""
    data = data[1:]
    data = data[:-1]
    app.logger.debug("data str = " + data)

    data = data.replace('"', "")
    data = data.replace("'", "")
    data = data.replace(" ", "")
    data = data.replace("{", "")
    data = data.replace("}", "")

    if out == 'open':
        str += "open_times\n"
        while data:
            start_val = data.find("[")
            end_val = data.find("]")
            snippet = data[start_val + 1:end_val]
            o_times = snippet.split(",")
            for x in o_times:
                str += x + "\n"
            remove_str = 'open_times:[' + snippet + ']'
            data = data.replace(remove_str + ",", "")
            data = data.replace(remove_str, "")
    elif out == 'close':
        str += "close_times\n"
        while data:
            start_val = data.find("[")
            end_val = data.find("]")
            snippet = data[start_val + 1:end_val]
            c_times = snippet.split(",")
            for x in c_times:
                str += x + "\n"
            remove_str = 'close_times:[' + snippet + ']'
            app.logger.debug('remove_str = ' + remove_str)
            data = data.replace(remove_str + ",", "")
            data = data.replace(remove_str, "")
    else:
        remove_str = ""
        str += "open_times,close_times\n"
        count = 0
        while data:
            app.logger.debug(data)
            start_val = data.find("[")
            end_val = data.find("]")
            snippet = data[start_val + 1:end_val]
            a_times = snippet.split(",")
            for x in a_times:
                str += x
                if count % 2 == 0:
                    str += " "
                else:
                    str += "\n"
            if count % 2 == 0:
                remove_str = 'open_times:[' + snippet + ']'
            else:
                remove_str = 'close_times:[' + snippet + ']'
            app.logger.debug('remove_str = ' + remove_str)
            data = data.replace(remove_str + ",", "")
            data = data.replace(remove_str, "")
            count += 1
    return str


def get_data(type_arg='all'):
    num = request.args.get('top', type=int)
    if num is None or num <= 0:
        return ""
    if type_arg == 'close':
        entries = db.brevetdb.find({}, {'_id': 0, 'brev_distance': 0, 'open_times': 0, 'kms': 0}).limit(num)
    elif type_arg == 'open':
        entries = db.brevetdb.find({}, {'_id': 0, 'brev_distance': 0, 'close_times': 0, 'kms': 0}).limit(num)
    else:
        entries = db.brevetdb.find({}, {'_id': 0, 'brev_distance': 0, 'kms': 0}).limit(num)
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
