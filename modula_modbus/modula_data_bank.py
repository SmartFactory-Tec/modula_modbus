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
        super().__init__()
        self.picking_id = None
        self.odoo_client = odoo_client

    def _on_input_request(self):
        [product_code, qty] = self.get_holding_registers(1, 2)

        if product_code == 1:
            self.picking_id = self.odoo_client.create_input_picking(product_code='fix', quantity=qty)
        elif product_code == 2:
            self.picking_id = self.odoo_client.create_input_picking(product_code='asdf', quantity=qty)

    def _on_output_request(self):
        [product_code, qty] = self.get_holding_registers(1, 2)
        if product_code == 1:
            self.picking_id = self.odoo_client.create_output_picking(product_code='fix', quantity=qty)
        elif product_code == 2:
            self.picking_id = self.odoo_client.create_output_picking(product_code='asdf', quantity=qty)

    def _on_tray_status(self):
        status_modula = self.odoo_client.get_tray_status(self.picking_id)

        if status_modula['status'] == "not in picking":
            self.set_input_registers(0, [1])

        if status_modula['status'] == "in picking":
            self.set_input_registers(0, [2, int(status_modula['pos_x']), int(status_modula['pos_y']),
                                         int(status_modula['dim_x']), int(status_modula['dim_y'])])

    def _on_request_confirmation(self):
        self.odoo_client.confirm_picking(self.picking_id)

        self.set_holding_registers(0, [0, 0, 0])
        self.set_input_registers(0, [0, 0, 0, 0, 0])


def on_coils_change(self, address, from_value, to_value, srv_info):
    # check it's only the function call coil
    if address != 0: return

    # if set to true
    if to_value:
        [function_id] = self.get_holding_registers(0, 1)

        if function_id == 1:
            self._on_input_request()
        elif function_id == 2:
            self._on_output_request()
        elif function_id == 3:
            self._on_tray_status()
        elif function_id == 4:
            self._request_confirmation()

        self.set_discrete_inputs(0, [0])
        self.set_coils(0, [0])


def on_holding_registers_change(self, address, from_value, to_value, srv_info):
    self.set_discrete_inputs(0, [1])
