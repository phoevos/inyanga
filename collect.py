import datetime
import pymongo
import requests
from dict2akn import dict2akn

client = pymongo.MongoClient("mongodb://localhost:27017/")

db = client['diavgeia']
col = db['meta']
col.create_index([('$**', 'text')])

address = 'https://test3.diavgeia.gov.gr/luminapi/opendata'

def collect(size, from_date, to_date):
    err = validate_input(size, from_date, to_date)
    if err:
        return 'red'+ err
    size = 'size=' + size
    from_date = '&from_issue_date=' + from_date
    to_date = '&to_issue_date=' + to_date

    response = requests.get(address + '/search.json?' + size + from_date + to_date)

    countIns = 0
    countFound = 0
    documents = []

    if response.status_code == 200:
        res = response.json()
        for dec in res['decisions']:
            ada = dec['ada']
            res = col.find_one({'akomaNtoso.doc.meta.publication.ada': ada})
            if res == None:
                countIns += 1
                logres = requests.get(address + '/decisions/{}/versionlog.json'.format(ada))
                if logres.status_code == 200:
                    log = logres.json()
                    dec['versions'] = log['versions']

                akn = dict2akn(dec)
                documents.append(akn)
            else:
                countFound += 1

        if documents:
            col.insert_many(documents)

    result = 'Inserted {} new documents.\n'.format(countIns) + ' {} of the fetched documents were already in the DB.'.format(countFound)
    return result


def validate_input(size, from_date, to_date):
    if size:
        if int(size) <= 0:
            return "The number of documents has to be greater than 0."
    date_format = '%Y-%m-%d'
    if from_date:
        try:
            datetime.datetime.strptime(from_date, date_format)
        except ValueError:
            return "Incorrect date format, From Date should be YYYY-MM-DD"
    if to_date:
        try:
            datetime.datetime.strptime(to_date, date_format)
        except ValueError:
            return "Incorrect date format, To Date should be YYYY-MM-DD"
    if from_date > to_date:
        return "The provided dates were the wrong way round, try again."
    return ""