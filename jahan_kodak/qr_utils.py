import frappe
from io import BytesIO
from base64 import b64encode

@frappe.whitelist()
def get_qr_base64(text):
    try:
        from pyqrcode import create as qrcreate
        url = qrcreate(text)
        stream = BytesIO()
        url.svg(stream, scale=4, background="#ffffff", module_color="#000000")
        svg = stream.getvalue().decode("utf-8").replace("\n", "")
        stream.close()
        return "data:image/svg+xml;base64," + b64encode(svg.encode("utf-8")).decode("utf-8")
    except Exception as e:
        return ""
