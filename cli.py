import requests
import os
import json
from datetime import date
from PyInquirer import style_from_dict, Token, prompt

from dict2xml import dict2xml
from collect import collect, validate_input

baseURL = 'http://127.0.0.1:8765/meta'

style = style_from_dict({
    Token.QuestionMark: '#E91E63 bold',
    Token.Selected: '#673AB7 bold',
    Token.Instruction: '#0bf416',
    Token.Answer: '#2196f3 bold',
    Token.Question: '#0bf416 bold',
})

def red(string):
    return '\033[1;91m {}\033[00m\n'.format(string)

def yellow(string):
    return '\033[1;93m {}\033[00m\n'.format(string)

def saveFile(doc, ada, format):
    if not os.path.exists('docs'):
        os.makedirs('docs')
    if not os.path.exists('docs/' + format):
        os.makedirs('docs/' + format)
    path = 'docs/' + format + '/' + ada + '.' + format
    with open(path, 'w', encoding='utf-8') as f: 
        if format == 'json':
            json.dump(doc, f, indent=4, ensure_ascii=False)
        else:
            f.write(doc)
    return path

def client():
    os.system('cls||clear')
    yellow('What a beautiful day to enter the cult...')
    while True:
        print('----------------------------------------------------------------------')
        method_q = [
            {
                'type': 'list',
                'name': 'method',
                'message': 'What would you like to do?',
                'choices': ['Collect data from the Diavgeia OpenDataAPI', 'Search by ADA', 'Search by Date', 'Search by Text', 'Empty local DB', 'Exit']
            }]
        method_a = prompt(method_q, style=style)['method']
        os.system('cls||clear')
        if method_a == 'Collect data from the Diavgeia OpenDataAPI':
            print('Collect data from the Diavgeia OpenDataAPI.')
            print('If no input is given, the default parameters will be used...')
            print('----------------------------------------------------------------------')
            fetch_q = [
                {
                    'type': 'input',
                    'name': 'size',
                    'message': 'Number of documents to fetch:',
                    'filter': lambda val: str(val)
                },
                {
                    'type': 'input',
                    'name': 'from',
                    'message': 'From Date:',
                    'filter': lambda val: str(val)
                },
                {
                    'type': 'input',
                    'name': 'to',
                    'message': 'To Date:',
                    'filter': lambda val: str(val)
                }
                ]
            fetch_a = prompt(fetch_q, style=style)
            print_size = fetch_a['size'] if fetch_a['size'] else '10'
            print_from = fetch_a['from'] if fetch_a['from'] else 'default starting date'
            print_to = fetch_a['to'] if fetch_a['to'] else 'default finishing date'
            print('\nConfirm insertion:')
            fetch_confirm_q = [
                {
                    'type': 'confirm',
                    'name': 'fetch_confirm',
                    'message': 'Would you like to fetch ' + print_size + ' documents from ' + print_from + ' to ' + print_to + '?',
                    'default': True
                }
            ]
            fetch_confirm_a = prompt(fetch_confirm_q)['fetch_confirm']
            if fetch_confirm_a:
                print(yellow('\n Fetching...'))
                print(yellow('This could take a while...'))
                response = collect(fetch_a['size'], fetch_a['from'], fetch_a['to'])
                if len(response.split('red')) > 1:
                    print(red(response.split('red')[1]))
                else:
                    print(yellow(response))
                continue

        elif method_a == 'Search by ADA':
            print('Look for a specific document in the local DB.')
            print('If no ADA is provided, all documents will be returned...')
            print('You can opt to save the returned documents in AKN or JSON format.')
            print('----------------------------------------------------------------------\n')
            search_q = [
                {
                    'type': 'input',
                    'name': 'ada',
                    'message': 'Provide document ADA (Αριθμός Διαδικτυακής Ανάρτησης):',
                    'filter': lambda val: str(val)
                },
                {
                    'type': 'confirm',
                    'name': 'akn',
                    'message': 'Would you like to save the returned documents as .akn files?',
                    'default': False
                },
                {
                    'type': 'confirm',
                    'name': 'json',
                    'message': 'Would you like to save the returned documents as .json files?',
                    'default': False
                }
            ]
            search_a = prompt(search_q, style=style)
            
            ada = '/' + search_a['ada'] if search_a['ada'] else ''
            endpoint = baseURL + ada
            response = requests.get(endpoint)
            if response.status_code == 200:
                if not response.json():
                    print(red('\n  No documents were found!'))
                elif len(response.json()) > 1:
                    count = 0
                    for dec in response.json():
                        count += 1
                        ada = dec['akomaNtoso']['doc']['meta']['publication']['ada']

                        print(yellow('----------------------------------------------------------------------'))
                        
                        if search_a['json']:
                            path = saveFile(dec, ada, 'json')
                            print(yellow('Saved in JSON format: ./' + path))
                            
                        dec = dict2xml(dec)
                        
                        if search_a['akn']:
                            path = saveFile(dec, ada, 'akn')
                            print(yellow('Saved in AKN format: ./' + path))
                        
                        print(yellow('----------------------------------------------------------------------'))

                        print(yellow(dec))
                        
                    print(yellow('{} documents were found.'.format(count)))
                    
                else:
                    dec = response.json()
                    ada = dec['akomaNtoso']['doc']['meta']['publication']['ada']

                    print(yellow('----------------------------------------------------------------------'))
                    
                    if search_a['json']:
                        path = saveFile(dec, ada, 'json')
                        print(yellow('Saved in JSON format: ./' + path))
                        
                    dec = dict2xml(response.json())
                    
                    if search_a['akn']:
                        path = saveFile(dec, ada, 'akn')
                        print(yellow('Saved in AKN format: ./' + path))
                    
                    print(yellow('----------------------------------------------------------------------'))

                    print(yellow(dec))
                    
            continue

        elif method_a == 'Search by Date':
            print('Search for documents by date in the local DB.')
            print('If no input is given, the default parameters will be used...')
            print('----------------------------------------------------------------------')
            search_q = [
                {
                    'type': 'input',
                    'name': 'from',
                    'message': 'From Date:',
                    'filter': lambda val: str(val),
                    'default': '1800-01-22'
                },
                {
                    'type': 'input',
                    'name': 'to',
                    'message': 'To Date:',
                    'filter': lambda val: str(val),
                    'default': str(date.today())
                },
                {
                    'type': 'confirm',
                    'name': 'akn',
                    'message': 'Would you like to save the returned documents as .akn files?',
                    'default': False
                },
                {
                    'type': 'confirm',
                    'name': 'json',
                    'message': 'Would you like to save the returned documents as .json files?',
                    'default': False
                }
                ]
            search_a = prompt(search_q, style=style)
            print_from = search_a['from'] if search_a['from'] else 'default starting date'
            print_to = search_a['to'] if search_a['to'] else 'default finishing date'
            print(yellow('\n  Fetching documents from ' + print_from + ' to ' + print_to + '...'))
            search_confirm_a = True
            if search_confirm_a:
                err = validate_input(10, search_a['from'], search_a['to'])
                if err:
                    print(red(' ' + err))
                    continue
                print(yellow(' Fetching from DB...'))
                dateF = '/date/' + search_a['from'] + '/' + search_a['to']
                endpoint = baseURL + dateF
                response = requests.get(endpoint)
                if response.status_code == 200:
                    if len(response.json()) > 1:
                        count = 0
                        for dec in response.json():
                            count += 1
                            ada = dec['akomaNtoso']['doc']['meta']['publication']['ada']
                        
                            print(yellow('----------------------------------------------------------------------'))

                            if search_a['json']:
                                path = saveFile(dec, ada, 'json')
                                print(yellow('Saved in JSON format: ./' + path))
                                
                            dec = dict2xml(dec)
                            
                            if search_a['akn']:
                                path = saveFile(dec, ada, 'akn')
                                print(yellow('Saved in AKN format: ./' + path))
                            
                            print(yellow('----------------------------------------------------------------------'))

                            print(yellow(dec))
                            
                        print(yellow('{} documents were found.'.format(count)))
                        
                    elif len(response.json()) == 1:
                        dec = response.json()
                        dic = dec[0]
                        ada = dic['akomaNtoso']['doc']['meta']['publication']['ada']
                        
                        print(yellow('----------------------------------------------------------------------'))

                        if search_a['json']:
                            path = saveFile(dic, ada, 'json')
                            print(yellow('Saved in JSON format: ./' + path))
                            
                        dic = dict2xml(response.json())
                        
                        if search_a['akn']:
                            path = saveFile(dic, ada, 'akn')
                            print(yellow('Saved in AKN format: ./' + path))

                        print(yellow('----------------------------------------------------------------------'))

                        print(yellow(dic))
                        
                    else:
                        print(red(' No documents were found!'))

                continue
        
        elif method_a == 'Search by Text':
            print('Search by Text.')
            print('----------------------------------------------------------------------')
            text_q = [
                {
                    'type': 'input',
                    'name': 'search',
                    'message': 'Search:',
                    'filter': lambda val: str(val)
                },
                {
                    'type': 'confirm',
                    'name': 'akn',
                    'message': 'Would you like to save the returned documents as .akn files?',
                    'default': False
                },
                {
                    'type': 'confirm',
                    'name': 'json',
                    'message': 'Would you like to save the returned documents as .json files?',
                    'default': False
                }
                ]
            text_a = prompt(text_q, style=style)
            if text_a['search']:
                response = requests.get(baseURL + '/textSearch/' + text_a['search'])
                if response.status_code == 200:
                    if len(response.json()) > 1:
                        count = 0
                        for dec in response.json():
                            count += 1
                            dec.pop('score')
                            ada = dec['akomaNtoso']['doc']['meta']['publication']['ada']
                        
                            print(yellow('----------------------------------------------------------------------'))

                            if text_a['json']:
                                path = saveFile(dec, ada, 'json')
                                print(yellow('Saved in JSON format: ./' + path))
                                
                            dec = dict2xml(dec)
                            
                            if text_a['akn']:
                                path = saveFile(dec, ada, 'akn')
                                print(yellow('Saved in AKN format: ./' + path))
                            
                            print(yellow('----------------------------------------------------------------------'))

                            print(yellow(dec))
                            
                        print(yellow('{} documents were found.'.format(count)))
                        
                    elif len(response.json()) == 1:
                        dec = response.json()
                        dic = dec[0]
                        dic.pop('score')
                        ada = dic['akomaNtoso']['doc']['meta']['publication']['ada']
                        
                        print(yellow('----------------------------------------------------------------------'))

                        if text_a['json']:
                            path = saveFile(dic, ada, 'json')
                            print(yellow('Saved in JSON format: ./' + path))
                            
                        dic = dict2xml(response.json())
                        
                        if text_a['akn']:
                            path = saveFile(dic, ada, 'akn')
                            print(yellow('Saved in AKN format: ./' + path))

                        print(yellow('----------------------------------------------------------------------'))

                        print(yellow(dic))
                        
                    else:
                        print(red('\n  No documents were found!'))
            else:
                print(red('\n A search term has to be provided!'))
            continue

        elif method_a == 'Empty local DB':
            print('Empty local DB.')
            print('----------------------------------------------------------------------')
            empty_q = [
                {
                    'type': 'confirm',
                    'name': 'empty',
                    'message': 'Would you like to empty the local DB?',
                    'default': False
                }
                ]
            empty_a = prompt(empty_q, style=style)
            if empty_a['empty']:
                response = requests.delete(baseURL + '/empty')
                print(yellow('\n  ' + response.text))
            continue

        elif method_a == 'Exit':
            os.system('cls||clear')
            break

        else:
            break

if __name__ == '__main__':
    
    client()