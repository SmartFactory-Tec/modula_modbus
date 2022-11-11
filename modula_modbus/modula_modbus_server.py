from pyModbusTCP.server import ModbusServer, DataBank

from modula_modbus.odoo_client import OdooClient

PRODUCT_CODES = {
    1: 'fix',
    2: 'asdf',
}

FUNCTION = {
    0: 'input req',
    1: 'output req',
    2: 'tray statu',
    3: 'confirm',
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

        pass

    def on_holding_registers_change(self, address, from_value, to_value, srv_info):
        pass
