from datetime import date, datetime

def dict2akn(dict):
    akn = {}

    verTs = datetime.utcfromtimestamp(float(dict['versions'][0]['versionTimestamp']/1000))
    verDate = str(verTs.date())

    docType = dict['extraFieldValues'].pop('documentType')
    if(docType == 'ΠΡΑΞΗ'):
        docType = 'act'
    else:
        docType = 'doc'

    dateF =  str(verTs.year) + '/' + str(verTs.month)
    baseUri = '/gr/' + docType + '/' + dateF + '/'
    expression = baseUri + verDate
    
    issueDate = str(datetime.fromtimestamp(float(dict['issueDate']/1000)).date())
    publishTimestamp = str(datetime.utcfromtimestamp(float(dict['publishTimestamp']/1000)))
    submissionTimestamp = str(datetime.utcfromtimestamp(float(dict['submissionTimestamp']/1000)))
    
    for v in dict['versions']:
        v['versionTimestamp'] = str(datetime.utcfromtimestamp(float(v['versionTimestamp']/1000)))
    
    akn['akomaNtoso'] = {
        'doc': {
            'meta': {
                'identification': {
                    'FRBRWork': {
                        'FRBRthis': baseUri,
                        'FRBRuri': baseUri,
                        'FRBRdate': {
                            'date': verDate,
                            'name': dict['versions'][0]['status']
                        },
                        'FRBRauthor': dict['versions'][0]['creator'],
                        'FRBRcountry': 'gr',
                        'FRBRname': docType
                    },
                    'FRBRExpression': {
                        'FRBRthis': expression,
                        'FRBRuri': expression,
                        'FRBRdate': {
                            'date': issueDate,
                            'status': dict['status']
                        },
                        'FRBRauthor': dict['signerIds'],
                        'FRBRcountry': 'gr',
                        'FRBRlanguage': 'gr',
                    },
                    'FRBRManifestation': {
                        'FRBRthis': expression + '.xml',
                        'FRBRuri': expression + '.akn',
                        'FRBRdate': {
                            'date': str(date.today()),
                            'name': 'AKNConversion'
                        },
                        'FRBRauthor': 'Indlovu',
                        'FRBRcountry': 'gr',
                        'FRBRlanguage': 'gr'
                    },
                    'FRBRItem': { 
                        'url': dict['url'],
                        'documentUrl': dict['warnings']
                    }
                },
                'lifecycle': dict['versions'],
                'publication': {
                    'ada': dict['ada'],
                    'protocolNumber': dict['protocolNumber'],
                    'versionId': dict['versionId'],
                    'organizationId': dict['organizationId'],
                    'signerIds': dict['signerIds'],
                    'unitIds': dict['unitIds'],
                    'publishTimestamp': publishTimestamp
                },
                'proprietary': {
                    'subject': dict['subject'],
                    'thematicCategoryIds': dict['thematicCategoryIds'],
                    'decisionTypeId': dict['decisionTypeId'],
                    'submissionTimestamp': submissionTimestamp,
                    'extraFieldValues': dict['extraFieldValues'],
                    'attachments': dict['attachments'],
                    'warnings': dict['warnings'],
                    'correctedVersionId': dict['correctedVersionId'],
                    'privateData': dict['privateData']
                }
            }
        },
        '_xmlns': 'http://docs.oasis-open.org/legaldocml/ns/akn/3.0/CSD13'
    }
    
    return akn