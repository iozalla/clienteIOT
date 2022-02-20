#Iñigo Ozalla Ontoria Grupo 2
import sys

import psutil
import time
import urllib
import json
import requests

userAPI="3ARG82L2SZI0YU7T"


def crearCanal():#crea un canal
    metodo = 'POST'
    uri = "https://api.thingspeak.com/channels.json"
    cabeceras = {'Host': 'api.thingspeak.com',
                 'Content-Type': 'application/x-www-form-urlencoded'}
    contenido = {'api_key': userAPI,
                 'name': 'Lab1',
                 'field1': "%CPU",
                 'field2': "%RAM"}
    contenido_encoded = '&'+urllib.parse.urlencode(contenido)#AQUI HABIA QUE AÑADIR UNA & AL PRINCIPIO PARA QUE LA PETICION FUERA CORRECTA
    cabeceras['Content-Length'] = str(len(contenido_encoded))
    respuesta = requests.request(metodo, uri, data=contenido_encoded, headers=cabeceras, allow_redirects=False)
    if respuesta.status_code==402:
        print("Hay demasiados canales, borra uno y vuelve a intentarlo o usa uno ya creado")
        sys.exit()
    contenido = json.loads(respuesta.content)#devuelvo la informacion del canal para poder usar la api del canal al editar y vaciar el canal
    print(contenido)
    return contenido

def actualizarDatos(cpu,ram,apiKey):#actualiza los datos dados unos datos y una clave de canal
    metodo = 'GET'
    uri = "https://api.thingspeak.com/update.json"
    cabeceras = {'Host': 'api.thingspeak.com',
                 'Content-Type': 'application/x-www-form-urlencoded'}
    contenido = {'api_key': apiKey,
                'field1':int(cpu),
                'field2':int(ram)}
    contenido_encoded = '&'+urllib.parse.urlencode(contenido)#AQUI HABIA QUE AÑADIR UNA & AL PRINCIPIO PARA QUE LA PETICION FUERA CORRECTA
    cabeceras['Content-Length'] = str(len(contenido_encoded))
    respuesta = requests.request(metodo, uri, data=contenido_encoded, headers=cabeceras, allow_redirects=False)


def vaciarCanal(id): #vacia el canal dado un id
        metodo = 'DELETE'
        uri = 'https://api.thingspeak.com/channels/'+str(id)+'/feeds.json'
        cabeceras = {'Host': 'api.thingspeak.com','Content-Type': 'application/x-www-form-urlencoded'}
        contenido = {'api_key': userAPI}
        contenido_encoded = '&' + urllib.parse.urlencode(contenido)#AQUI HABIA QUE AÑADIR UNA & AL PRINCIPIO PARA QUE LA PETICION FUERA CORRECTA
        print(contenido_encoded)
        cabeceras['Content-Length'] = str(len(contenido_encoded))
        respuesta = requests.request(metodo, uri, data=contenido_encoded, headers=cabeceras, allow_redirects=False)
        print(respuesta.url + respuesta.request.body)
        print(respuesta)


def getCanal(): #recoge los canales que estan creados
    #metodo optativo que sirve para no tener que crear canales todo el rato y usar uno si ya esta disponible
    #he creado este metodo por que cuando llegas a 4 canales creados requiere pago
        metodo = 'GET'
        uri = "https://api.thingspeak.com/channels.json"
        cabeceras = {'Host': 'api.thingspeak.com','Content-Type': 'application/x-www-form-urlencoded'}
        contenido = {'api_key': userAPI}
        contenido_encoded = '&'+urllib.parse.urlencode(contenido)#AQUI HABIA QUE AÑADIR UNA & AL PRINCIPIO PARA QUE LA PETICION FUERA CORRECTA
        cabeceras['Content-Length'] = str(len(contenido_encoded))
        respuesta = requests.request(metodo, uri, data=contenido_encoded, headers=cabeceras, allow_redirects=False)
        contenido = json.loads(respuesta.content)#devuelvo la informacion del canal para poder usar la api del canal al editar y vaciar el canal
        print(contenido)
        for canal in contenido:#si encuentra un canal con el nombre Lab1 devuelve su clave de escritura para poder actualizarlo
            #print(canal)
            if canal['name']==sys.argv[1]:
                return canal
        return -1;#si  no encuentra ningun canal con ese nombre devuelve -1





if __name__ == '__main__':

    if userAPI == "codigo":
        print("Es necesario un codigo API que obtendras en tu perfil de ThingSpeak")
        exit
    canalDisponible=getCanal()
    print(canalDisponible)
    if canalDisponible==-1:#si no hay un canal disponible se crea unno nuevo

        contenido=crearCanal()
        id=contenido['id']
        writeApiKey=contenido['api_keys'][0]['api_key']#COGEMOS LA CLAVE DE ESCRITURA DEL CANAL CREADO

    else:#si hay un canal disponible se usa su api key
        id=canalDisponible['id']
        print("ya hay un canal disponible (Usamos ese)")
        writeApiKey=canalDisponible["api_keys"][0]['api_key']

    urlCanal="https://thingspeak.com/channels/"+str(id)+"/private_show"
    print("| URL del canal creado:" , urlCanal,"  |")


    while(True):

        try:
            cpu=psutil.cpu_percent(1)
            ram=psutil.virtual_memory().percent
            actualizarDatos(cpu,ram,writeApiKey)
            print("CPU: %" + str(cpu) + "\tRAM: %" + str(ram))
            time.sleep(14)
        except KeyboardInterrupt: #recoge el CRL+C
            print('Vaciando canal...')
            vaciarCanal(id)
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