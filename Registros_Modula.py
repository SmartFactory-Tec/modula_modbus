from pyModbusTCP.client import ModbusClient
import time
import requests
import json

input_req_uri = '/modula/input_request' #direccion para ingresar productos
output_req_uri = '/modula/output_request' #direccion para sacar productos
tray_stat_uri = '/modula/tray_status'    #direccion por la cual se recibira el estado de bandeja
req_confirm_uri = '/modula/request_confirmation' #direccion por la cual se le avisara a modula que ya se completo la recogida del produto

hostname = 'http://localhost:8069' 

producto = {'params': {'code': 'llavero','qty':10}} # codigo del producto y cantiadad

confirm = {'Entregado': 'test'}

user = "A00227526@itesm.mx"
password = "12345678"


myhost = 'localhost'
myport = 12345
c = ModbusClient(host=myhost,port=myport)

class Registros:

    def __init__(self):
        
        # Registros = 1-Pedido, 2-Estatus de la charola, 3-Confirmacion de pick para regreso de la charola
        self.informacion=[0,0,0]

    def pedido(self, item): 
        res = requests.post(hostname + input_req_uri, params = {"code":"fix","qty":"1"}, auth =(user, password))
        print(res.text)
        return res.text
        #body = res.json()['result']
        #Registros.informacion[0] = body
        if item == 'fix':
            self.informacion[0] = 10
            self.send_info()

    def status(self,p): # 1 indica que la bandeja esta en proceso, 2 indica que la bandeja ha llegado, 3 indica un error
        res = requests.get(hostname + tray_stat_uri, params = {"picking_id" : str(p)} , auth =(user, password))
        m=json.loads(res.text)
        print(m["status"])
        #print(m["status"])

        """
        body = res.json()['result']
        print(body)
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
        """

    def devolver(self,p):
        res = requests.post(hostname + req_confirm_uri, params = {"picking_id":str(p)}, auth =(user, password))
        
        
    def send_info(self):

        if c.open():
                    
            bits = c.read_holding_registers(0, 3)
            
            self.informacion[1]=bits[1]
            print( self.informacion[0])


            c.write_multiple_registers(0, [self.informacion[0], self.informacion[1], self.informacion[2]])
            time.sleep(1)

        else:
            print("unable to connect to " + myhost + ":" + str(myport))



pedido1 = Registros()
p=pedido1.pedido('')

while True:
    pedido1.status(p)
    time.sleep(.5)


"""
pedido1.devolver(13)
pedido1.pedido('')
pedido1.status()


while True:
    pedido1.status()
    time.sleep(.5)
"""
#while True:
    
 #   time.sleep(1)


#  archivo de configuraccion TOML 