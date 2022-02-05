import psutil
import time
import urllib
import json
import requests

# Press the green button in the gutter to run the script.
userAPI="3ARG82L2SZI0YU7T"
def crearCanal():
    metodo = 'POST'
    uri = "https://api.thingspeak.com/channels.json"
    cabeceras = {'Host': 'api.thingspeak.com',
                 'Content-Type': 'application/x-www-form-urlencoded'}
    contenido = {'api_key': userAPI,
                 'name': 'Lab111',
                 'field1': "%CPU",
                 'field2': "%RAM"}
    contenido_encoded = '&'+urllib.parse.urlencode(contenido)
    print(contenido_encoded)
    cabeceras['Content-Length'] = str(len(contenido_encoded))
    respuesta = requests.request(metodo, uri, data=contenido_encoded, headers=cabeceras, allow_redirects=False)
    #print(respuesta.url+respuesta.request.body)
    codigo = respuesta.status_code
    descripcion = respuesta.reason
    print(str(codigo) + " " + descripcion)
    contenido = json.loads(respuesta.content)
    print(contenido['api_keys'][0])
    return contenido


def deleteChannel(id):
    metodo = 'DELETE'
    uri = 'https://api.thingspeak.com/channels/'+str(id)+'.json'
    cabeceras = {'Host': 'api.thingspeak.com',
                 'Content-Type': 'application/x-www-form-urlencoded'}
    contenido = {'api_key': userAPI}
    contenido_encoded = '&' + urllib.parse.urlencode(contenido)
    print(contenido_encoded)
    cabeceras['Content-Length'] = str(len(contenido_encoded))
    respuesta = requests.request(metodo, uri, data=contenido_encoded, headers=cabeceras, allow_redirects=False)
    print(respuesta.url + respuesta.request.body)
    print(respuesta)




def actualizarDatos(cpu,ram,apiKey):
    metodo = 'GET'
    uri = "https://api.thingspeak.com/update.json"
    cabeceras = {'Host': 'api.thingspeak.com',
                 'Content-Type': 'application/x-www-form-urlencoded'}
    contenido = {'api_key': apiKey,
                'field1':int(cpu),
                'field2':int(ram)}
    contenido_encoded = '&'+urllib.parse.urlencode(contenido)
    #print(contenido_encoded)
    cabeceras['Content-Length'] = str(len(contenido_encoded))
    respuesta = requests.request(metodo, uri, data=contenido_encoded, headers=cabeceras, allow_redirects=False)
    #print(respuesta.url + respuesta.request.body)
    codigo = respuesta.status_code
    descripcion = respuesta.reason
    #print(str(codigo) + " " + descripcion)
    contenido = respuesta.content
    #print(contenido)


if __name__ == '__main__':
    contenido=crearCanal()
    writeApiKey=contenido['api_keys'][0]['api_key']
    id=contenido['id']
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    urlCanal="https://thingspeak.com/channels/"+str(id)+"/private_show"
    print("| URL del canal creado:" , urlCanal,"  |")
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')


    while(True):
        try:
            cpu=psutil.cpu_percent(1)
            ram=psutil.virtual_memory().percent
            actualizarDatos(cpu,ram,writeApiKey)
            print('CPU:',cpu,'% RAM:',ram,'%')
            time.sleep(14)
        except KeyboardInterrupt: #recoge el CRL+C

            print('Cerrando...')
            deleteChannel(id)
            exit()


######################################
#               BURP                 #
######################################

#crear canal
#POST /channels.json HTTP/1.1
#Host: api.thingspeak.com
#Content-Type: application/x-www-form-urlencoded
#Content-Length: 118

#api_key=3ARG82L2SZI0YU7T&description=&field1=&field2=&latitude=&longitude=&name=channel&public_flag=false&tags=&url=


#Update canal
#POST /update.json HTTP/2
#Host: api.thingspeak.com
#Content-Type: application/x-www-form-urlencoded
#Content-Length: 43

#api_key=X1TCB1GEG809CCW5&field1=1&field2=12