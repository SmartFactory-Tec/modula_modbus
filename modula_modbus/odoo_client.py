import requests

INPUT_REQ_URI = '/modula/input_request'
OUTPUT_REQ_URI = '/modula/output_request'
TRAY_STATUS_URI = '/modula/tray_status'
REQ_CON_URI = '/modula/request_confirmation'


# TODO add error handling to all methods (except init I guess?)
class OdooClient:
    def __init__(self, hostname: str, user: str, password: str, port: int, secure: bool):
        self.hostname = hostname
        self.port = port
        self.secure = secure

        # construct connection url
        self.url = f'{"https" if secure else "http"}://{hostname}:{port}'

        self.auth = (user, password)

    def create_input_picking(self, product_code: str, quantity: int) -> int:
        res = requests.post(self.url + INPUT_REQ_URI, params={
            "code": product_code,
            "qty": str(quantity),
        }, auth=self.auth)

        return int(res.text)

    def create_output_picking(self, product_code: str, quantity: int) -> int:
        res = requests.post(self.url + OUTPUT_REQ_URI, params={
            "code": product_code,
            "qty": str(quantity),
        }, auth=self.auth)

        return int(res.text)

    def get_tray_status(self, picking_id: int) -> dict:
        res = requests.get(self.url + TRAY_STATUS_URI, params={
            "picking_id": picking_id,
        }, auth=self.auth)
        body = res.json()
        return body

    def confirm_picking(self, picking_id: str):
        requests.post(self.url + REQ_CON_URI, params={
            "picking_id": picking_id,
        }, auth=self.auth)
