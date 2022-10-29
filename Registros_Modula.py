import random
from pyModbusTCP.client import ModbusClient
import numpy as np
import time
import requests

prod_req_uri = '/modula/product_request' #direccion para solicitar el producto
tray_stat_uri = '/modula/tray_status'    #direccion por la cual se recibira el estado de bandeja
req_confirm_uri = '/modula/request_confirmation' #direccion por la cual se le avisara a modula que ya se completo la recogida del produto

hostname = 'http://10.22.128.137:8069' 

producto = {'params': {'code': 'llavero','qty':10}} # codigo del producto y cantiadad

confirm = {'Entregado': 'test'}


myhost = "192.168.0.15"
myport = 12345
c = ModbusClient(host=myhost,port=myport)

class Registros:

    def __init__(self):
        
        # Registros = 1-Pedido, 2-Estatus de la charola, 3-Confirmacion de pick para regreso de la charola
        self.informacion=[0,0,0]

    def pedido(self, item):
        res = requests.post(hostname + prod_req_uri, json = item)
        body = res.json()['result']
        Registros.informacion[0] = body

    def status(self):
        res = requests.get(hostname + tray_stat_uri, json={})
        body = res.json()['result']
        Registros.informacion[1] = body

    def confirmacion_pedido(self,):
        res = requests.post(hostname + req_confirm_uri, json = confirm)
        body = res.json()['result']
        Registros.informacion[2] = body
        
    """
    def send_info(self):

        if c.open():
                    
            bits = c.read_holding_registers(0, 3)
            Registros.informacion[1]=bits[1]


            c.write_multiple_registers(0,[Registros.informacion[1]])
            time.sleep(1)

        else:
            print("unable to connect to "+myhost+":"+str(myport))
    """



        # archivo de configuraccion y diccionarios