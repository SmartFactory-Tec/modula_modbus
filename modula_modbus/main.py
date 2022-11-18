from .config import load_config
from .odoo_client import OdooClient
from .modula_data_bank import ModulaDataBank
from pyModbusTCP.server import ModbusServer


# Registro 0 es entrada de producto, registro 1 salida de producto, registro 2 estado de charola, registro 3 devolucion de charola
# Registro 4 es la posicion en x del producto, registro 5 es la posicion en y del producto, registro 6 es la dimension en x del producto
# Registro 7 es la dimension en y del producto
# si el registro 0, o el registro 1 se le da un valor de 1 entonces se realizara un pedido, cuando se le asigne el valor de 2 significara
# que el modula ya esta procesando el pedido, lo mismo pasa con el registro 3 pero este es para la devolucion de la bandeja
# para el registro 3 el valor de 1 significara que la bandeja esta en camino y el valor 2 significara que la bandeja ya ha llegado

def main():
    config = load_config()

    client = OdooClient(
        hostname=config['odoo_hostname'],
        user=config['odoo_user'],
        password=config['odoo_password'],
        secure=config['odoo_secure'],
        port=config['odoo_port']
    )

    data_bank = ModulaDataBank(client)

    server = ModbusServer(
        host=config['hostname'],
        port=int(config['port']),
        data_bank=data_bank
    )

    server.start()
