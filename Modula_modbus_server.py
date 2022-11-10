#!/bin/python

from pyModbusTCP.server import ModbusServer, DataBank
from time import sleep
import odoo_client as modula
import json

# Create an instance of ModbusServer
#Registro 1 es entrada de producto, registro 2 salida de producto, registro 3 estado de charola, registro 4 devolucion de charola
#Registro 5 es la posicion en x del producto, registro 6 es la posicion en y del producto, registro 7 es la dimension en x del producto
#Registro 8 es la dimension en y del producto

#si el registro 1, o el registro 2 se le da un valor de 1 entonces se realizara un pedido, cuando se le asigne el valor de 2 significara
#que el modula ya esta procesando el pedido, lo mismo pasa con el registro 4 pero este es para la devolucion de la bandeja

#para el registro 3 el valor de 1 significara que la bandeja esta en camino y el valor 2 significara que la bandeja ya ha llegado


status_modula={"status":""}

#try:    
print("Start server...")
server = ModbusServer('localhost', 12345, no_block=True)
server.start()
print("Server is online")
state = [0]
while True:
    # Creacion de registros y print de los registros
    if state != server.data_bank.get_holding_registers(0,15):
        state = server.data_bank.get_holding_registers(0,15)
        print("Value of Registers has changed to " + str(state))
    
    #Si se llega a tener un pedido de entrada de producto
    if state [0] == 1:
        codigo_bandeja = modula.entrada_producto(code="fix",quantity=1)
        server.data_bank.set_holding_registers(0,[2])
        
    # Si se realizo un peido actualizar el estado de la bandeja
    if state[0] == 2:
        status_modula= json.loads(modula.estatus_bandeja(codigo_pedido=codigo_bandeja))
    
    #Si se llega a tener un pedido de salida de producto
    if state [1] == 1:  
        codigo_bandeja = modula.salida_producto(code="fix",quantity=1)
        server.data_bank.set_holding_registers(1,[2]) 

    # Si se realizo un peido actualizar el estado de la bandeja
    if state[1] == 2:
        status_modula=json.loads(modula.estatus_bandeja(codigo_pedido=codigo_bandeja))
    
    # Si se devuelve la bandeja mandar todos los registros a un estado inicial
    if state[3]== 1:
        modula.devolver_bandeja(codigo_pedido=codigo_bandeja)
        server.data_bank.set_holding_registers(0,[0])
        server.data_bank.set_holding_registers(1,[0])
        server.data_bank.set_holding_registers(2,[0])
        server.data_bank.set_holding_registers(3,[0])
        server.data_bank.set_holding_registers(4,[0])
        server.data_bank.set_holding_registers(5,[0])
        server.data_bank.set_holding_registers(6,[0])
        server.data_bank.set_holding_registers(7,[0])
        status_modula["status"] = ""

    # Si la bandeja esta lista se actualizara el registro 3 y los demas registros referenctes a las caracteristicas del producto
    if status_modula["status"] == "in picking":
        server.data_bank.set_holding_registers(2,[2]) 

        server.data_bank.set_holding_registers(4,[int(status_modula['pos_x'])]) 
        server.data_bank.set_holding_registers(5,[int(status_modula['pos_y'])])
        server.data_bank.set_holding_registers(6,[int(status_modula['dim_x'])])
        server.data_bank.set_holding_registers(7,[int(status_modula['dim_y'])])
    
    # Si la bandeja esta en proceso de llegar se actualizara el registro 3
    if status_modula["status"] == "not in picking":
        server.data_bank.set_holding_registers(2,[1])
    

    
    sleep(0.5)

"""
except:
    print("Shutdown server ...")
    server.stop()
    print("Server is offline")


"""


