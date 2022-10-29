#!/bin/python


from pyModbusTCP.server import ModbusServer, DataBank
from time import sleep
from random import uniform

# Create an instance of ModbusServer
server = ModbusServer("192.168.0.15", 12345, no_block=True)


try:    
    print("Start server...")
    server.start()
    print("Server is online")
    state = [0]
    while True:
        #DataBank.set_words(0, [int(uniform(0, 100))])
        if state != server.data_bank.get_holding_registers(0,15):
            state = server.data_bank.get_holding_registers(0,15)
            print("Value of Registers has changed to " +str(state))
        sleep(0.5)

except:
    print("Shutdown server ...")
    server.stop()
    print("Server is offline")

    #register output es para mandar registros
    #register input



# Registros = 1-Pedido, 2-Estatus de la charola, 3-Confirmacion de pick para regreso de la charola


