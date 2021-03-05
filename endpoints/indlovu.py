import pymongo
from flask import Blueprint
from bson.json_util import dumps

indlovu = Blueprint('indlovu', __name__)
client = pymongo.MongoClient("mongodb://localhost:27017/")

db = client['diavgeia']
col = db['meta']

@indlovu.route('/meta', methods=['GET'])
def meta():
    res = col.find({}, {'_id': 0})
    return dumps(res)
 
@indlovu.route('/meta/<ada>', methods=['GET'])
def getByAda(ada):
    res = col.find_one({'akomaNtoso.doc.meta.publication.ada': ada}, {'_id': 0})
    return dumps(res)
   
@indlovu.route('/meta/date/<fromDate>/<toDate>', methods=['GET'])
def getByDate(fromDate, toDate):
    res = col.find({'akomaNtoso.doc.meta.identification.FRBRExpression.FRBRdate.date': {
        '$gte': fromDate,
        '$lte': toDate
    }}, {'_id': 0})
    return dumps(res)
  