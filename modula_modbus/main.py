from .config import load_config
from .odoo_client import OdooClient
from .modula_modbus_server import ModulaDataBank

from pyModbusTCP.server import ModbusServer
from time import sleep


import json

# Registro 0 es entrada de producto, registro 1 salida de producto, registro 2 estado de charola, registro 3 devolucion de charola
# Registro 4 es la posicion en x del producto, registro 5 es la posicion en y del producto, registro 6 es la dimension en x del producto
# Registro 7 es la dimension en y del producto
# si el registro 0, o el registro 1 se le da un valor de 1 entonces se realizara un pedido, cuando se le asigne el valor de 2 significara
# que el modula ya esta procesando el pedido, lo mismo pasa con el registro 3 pero este es para la devolucion de la bandeja
# para el registro 3 el valor de 1 significara que la bandeja esta en camino y el valor 2 significara que la bandeja ya ha llegado

def start(server: ModbusServer, client: OdooClient):
    print("Start server...")
    server.start()
    print("Server is online")

    state = [0]

    while True:
        # Creacion de registros y print de los registros
        if state != server.data_bank.get_holding_registers(0, 3):
            state = server.data_bank.get_holding_registers(0, 3) 
            print("Value of Registers has changed to " + str(state) + str(server.data_bank.get_coils(0,1)) + str(server.data_bank.get_discrete_inputs(0,1)) + str(server.data_bank.get_input_registers(0,5)))
  

        sleep(0.5)

def main():
    config = load_config()

    client = OdooClient(hostname=config['hostname'], user=config['user'], password=config['password'], secure=config['secure'],
                               port=config['port'])
    data_bank = ModulaDataBank(client)
    server = ModbusServer('localhost', 12345, data_bank=data_bank)

    try:
    
        start(server, client)
    except KeyboardInterrupt:
        print("Server stop")
        server.stop()
    except Exception:
        print("Server stop")
        server.stop()
        raise
