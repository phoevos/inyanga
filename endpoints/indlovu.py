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

@indlovu.route('/meta/empty', methods=['DELETE'])
def empty():
    try:
        col.delete_many({})
        return 'The local DB is now empty!'
    except:
        return 'An error occured while emptying the DB...'
 
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

@indlovu.route('/meta/textSearch/<someText>', methods=['GET'])
def getByText(someText):
    res = col.find({ 
      '$text': { '$search': someText }
    },{ 
      'score': { '$meta': "textScore" }, '_id': 0
    }
    ).sort( 'score', direction=pymongo.DESCENDING )

    return dumps(res)
  