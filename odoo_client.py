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

user = "A00227526@itesm.mx"
password = "12345678"


def entrada_producto(code,quantity):
    res = requests.post(hostname + input_req_uri, params = {"code":str(code),"qty":str(quantity)}, auth =(user, password))
    return res.text

def salida_producto(code,quantity):
    res = requests.post(hostname + output_req_uri, params = {"code":str(code),"qty":str(quantity)}, auth =(user, password))
    return res.text

def estatus_bandeja():
    res = requests.get(hostname + tray_stat_uri, auth =(user, password))
    return res.text

def devolver_bandeja(codigo_pedido):
    res = requests.post(hostname + req_confirm_uri, params = {"picking_id":str(codigo_pedido)}, auth =(user, password))
