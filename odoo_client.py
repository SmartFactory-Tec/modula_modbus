import requests

INPUT_REQ_URI = '/modula/input_request'
OUTPUT_REQ_URI = '/modula/output_request'
TRAY_STATUS_URI = '/modula/tray_status'
REQ_CON_URI = '/modula/request_confirmation'


# TODO add error handling to all methods (except init I guess?)
class OdooClient:
    def __init__(self, hostname: str, user: str, password: str, port: int = 80, secure: bool = True):
        self.hostname = hostname
        self.port = port
        self.secure = secure

        # construct connection url
        self.url = 'https' if secure else 'http' + '://' + hostname + ':' + str(port)

        self.auth = (user, password)

    def create_input_picking(self, product_code: str, quantity: int) -> int:
        res = requests.post(self.url + INPUT_REQ_URI, params={
            "code": product_code,
            "qty": str(quantity),
        }, auth=self.auth)

        # TODO return picking ID
        return res.text

    def create_output_picking(self, product_code: str, quantity: int) -> int:
        res = requests.post(self.url + OUTPUT_REQ_URI, params={
            "code": product_code,
            "qty": str(quantity),
        }, auth=self.auth)

        # TODO return picking ID
        return res.text

    # TODO add type hint for return of this method
    def get_tray_status(self, picking_id: int):
        res = requests.get(self.url + TRAY_STATUS_URI, params={
            "picking_id": picking_id,
        }, auth=self.auth)
        return res.text

    def confirm_picking(self, picking_id: str):
        requests.post(self.url + REQ_CON_URI, params={
            "picking_id": picking_id,
        }, auth=self.auth)
