#!/bin/python


from pyModbusTCP.server import ModbusServer, DataBank
from time import sleep
from random import uniform
import odoo_client as modula

# Create an instance of ModbusServer
#Registro 1 es entrada de producto, registro 2 salida de producto, registro 3 estado de charola, registro 4 devolucion de charola



try:    
    print("Start server...")
    server = ModbusServer('localhost', 12345, no_block=True)
    server.start()
    print("Server is online")
    state = [0]
    while True:
        
        if state != server.data_bank.get_holding_registers(0,15):
            state = server.data_bank.get_holding_registers(0,15)
            print("Value of Registers has changed to " + str(state))
        
        if state [0] == 1:
            codigo_bandeja = modula.entrada_producto(code="fix",quantity=1)
            server.data_bank.set_holding_registers(0,[2])
            
        if state[0] == 2:
            status_modula=modula.estatus_bandeja(codigo_pedido=codigo_bandeja)
        
        if state [1] == 1:  
            codigo_bandeja = modula.salida_producto(code="fix",quantity=1)
            server.data_bank.set_holding_registers(1,[2]) 

        if state[1] == 2:
            status_modula=modula.estatus_bandeja(codigo_pedido=codigo_bandeja)
        
        if state[3]== 1:
            modula.devolver_bandeja(codigo_pedido=codigo_bandeja)
            server.data_bank.set_holding_registers(0,[0])
            server.data_bank.set_holding_registers(1,[0])
            server.data_bank.set_holding_registers(2,[0])
            server.data_bank.set_holding_registers(3,[0])
            status_modula['status'] = ""
        
        if status_modula['status'] == "in picking":
            server.data_bank.set_holding_registers(2,[2]) 
        
        if status_modula['status'] == "not in picking":
            server.data_bank.set_holding_registers(2,[1])
        
        sleep(0.5)


except:
    print("Shutdown server ...")
    server.stop()
    print("Server is offline")

    #register output es para mandar registros
    #register input



# Registros = 1-Pedido, 2-Estatus de la charola, 3-Confirmacion de pick para regreso de la charola


