import random
from pyModbusTCP.client import ModbusClient
import numpy as np
import time
import requests

input_req_uri = '/modula/input_request' #direccion para ingresar productos
output_req_uri = '/modula/output_request' #direccion para sacar productos
tray_stat_uri = '/modula/tray_status'    #direccion por la cual se recibira el estado de bandeja
req_confirm_uri = '/modula/request_confirmation' #direccion por la cual se le avisara a modula que ya se completo la recogida del produto

hostname = 'http://localhost:8069' 

producto = {'params': {'code': 'llavero','qty':10}} # codigo del producto y cantiadad

confirm = {'Entregado': 'test'}

user = "a00227526@tec.mx"
password = "12345"


myhost = 'localhost'
myport = 12345
c = ModbusClient(host=myhost,port=myport)

class Registros:

    def __init__(self):
        
        # Registros = 1-Pedido, 2-Estatus de la charola, 3-Confirmacion de pick para regreso de la charola
        self.informacion=[0,0,0]

    def pedido(self, item): 
        res = requests.post(hostname + output_req_uri, json = item, auth =(user, password))
        #body = res.json()['result']
        #Registros.informacion[0] = body
        if item == 'fixture':
            self.informacion[0] = 10
            self.send_info()

    def status(self): # 1 indica que la bandeja esta en proceso, 2 indica que la bandeja ha llegado, 3 indica un error
        res = requests.get(hostname + tray_stat_uri, json={})
        body = res.json()['result']
        if body == '403':
            self.informacion[1] = 1
        elif body == '200':
            self.informacion[1] = 2
        else:
            self.informacion[1] = 3

    def confirmacion_pedido(self):
        res = requests.post(hostname + req_confirm_uri, json = confirm)
        body = res.json()['result']
        self.informacion[2] = body
        
    
    def send_info(self):

        if c.open():
                    
            bits = c.read_holding_registers(0, 3)
            
            self.informacion[1]=bits[1]
            print( self.informacion[0])


            c.write_multiple_registers(0,[self.informacion[0],self.informacion[1],self.informacion[2]])
            time.sleep(1)

        else:
            print("unable to connect to "+myhost+":"+str(myport))
    
pedido1 = Registros()
pedido1.pedido('fixture')



#   query parameters, basic auth 
        # archivo de configuraccion TOML y diccionarios