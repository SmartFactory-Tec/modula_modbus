from pyModbusTCP.server import ModbusServer, DataBank

from modula_modbus.odoo_client import OdooClient

PRODUCT_CODES = {
    1: 'fix',
    2: 'asdf',
}

FUNCTION = {
    1: 'input req',
    2: 'output req',
    3: 'tray statu',
    4: 'confirm',
}


# 1 coil - CALL
# 1 discrete input - LOCKED
# 1 holding register - FUNCTION
# 1 holding register - PRODUCT_CODE
# 1 holding register - QTY
# 1 input register - STATUS
# 1 input register - X
# 1 input register - Y
# 1 input register - width
# 1 input register - height

class ModulaDataBank(DataBank):
    def __init__(self, odoo_client: OdooClient):
        super().__init__(coils_size=1, d_inputs_size=1, h_regs_size=3, i_regs_size=5)

        self.odoo_client = odoo_client

    def on_coils_change(self, address, from_value, to_value, srv_info):
        if self.get_coils(0, 1) == 1:
            h_registers= self.get_holding_registers(0, 3)

             # Si se llega a tener un pedido de entrada de producto
            if h_registers[0]==1:
                codigo_bandeja = self.odoo_client.create_input_picking(product_code='fix', quantity= h_registers[2])
                self.set_holding_registers (1, [codigo_bandeja])
                self.set_coils(0,0)
                self.set_discrete_inputs(0,0)
            
             # Si se llega a tener un pedido de salida de producto
            if h_registers[0]==2:
                codigo_bandeja = self.odoo_client.create_output_picking(product_code='fix', quantity= 1)
                self.set_holding_registers (1, [codigo_bandeja])
                self.set_coils(0,0)
                self.set_discrete_inputs(0,0)
            
            # Revisar el estado de la bandeja y pedir datos adicionales si ya se esta en picking
            if h_registers[0] == 3:
                status_modula = self.odoo_client.get_tray_status(h_registers[1])
                
                if status_modula['status'] == "not in picking":
                    self.set_input_registers(0,1)
                
                if status_modula ['status'] == "in picking":
                    self.set_input_registers(0, [2, int(status_modula['pos_x']), int(status_modula['pos_y']), int(status_modula['dim_x']),int(status_modula['dim_y'])])
                self.set_coils(0,0)
                self.set_discrete_inputs(0,0)

            # Si se devuelve la bandeja y mandar todos los registros a un estado inicial
            if h_registers[0] == 4:
                self.odoo_client.confirm_picking(h_registers[1])
                
                self.set_holding_registers(0,[0,0,0])
                self.set_coils(0,0)
                self.set_input_registers(0,[0,0,0,0,0])
                self.set_discrete_inputs(0,0)

            pass

    def on_holding_registers_change(self, address, from_value, to_value, srv_info):
        self.set_discrete_inputs(0,1)
        pass
