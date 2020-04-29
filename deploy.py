from flask import Flask, request
import threading
import time
import requests
app = Flask(__name__)

volume = 0
reator = {
    'solucao':{
        'oleo': 0,
        'ETOH': 0,
        'NAOH': 0,

    },
    'volume': 0
}

@app.route('/reator', methods=['POST'])
def post(self):
        json_data = request.get_json(force=True)
        volume = json_data.get('volume', None)
        
        if volume is None:
            json = {
                "status_code": 400,
                "body": "Bad Request"
            }
            
        if reator['volume'] < int(volume):
            json = {
                "status_code": 204,
                "body": "Nao ha volume suficiente no tanque"
            }
        else:
            json = {
                "status_code": 200,
                "nome": "solucao",
                "volume": volume 
            }
            reator['volume'] = 0
            reator['solucao']['NAOH'] = 0
            reator['solucao']['ETOH'] = 0
            reator['solucao']['oleo'] = 0
        
        # requests.post(url=REATOR_URL, json=json, headers={"Content_Type": "application/json"})
        return json


@app.route('/reator', methods=['GET'])
def getVolume():
    global reator
    response = {
        'reator': reator
    }
    return response


class Secador(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        while True:
            global volume
            if volume > 0:
                time.sleep(3)
                request = {
                    'biodiesel': volume
                }
                print('sending volume to storage tank')
                print(request)
                #fazer callout pro tanque de biodisel
                volume = 0

class Reator(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        while True:
            if reator['volume'] < 50:
                
                time.sleep(1)
                json = {
                    'NAOH':0.5,
                    'ETOH':1.9,
                }
                #response = requests.post(url='', json=json, headers={"Content_Type": "application/json"}).json()
                #reator['solucao']['NAOH'] = response['NAOH']
                #reator['solucao']['ETOH'] = response['ETOH']
                json = {
                    'volume': 47.6
                }
                response = requests.post(url='https://programacao-concorrente.herokuapp.com/oleo', json=json, headers={"Content_Type": "application/json"}).json()
                oleo = response.get('volume',None)
                if(oleo is not None):
                    reator['solucao']['oleo'] = response['volume']

                reator['volume'] += reator['solucao']['oleo']+reator['solucao']['NAOH']+reator['solucao']['ETOH']
            #else:
            #    pergunta se manda pro thomas
             #   if manda, eu mando

def create_app():
    global app
    print('starting logic thread...')
    sec = Reator()
    sec.start()
    print('logic thread started!')
    print('starting flask server')
    return app


   