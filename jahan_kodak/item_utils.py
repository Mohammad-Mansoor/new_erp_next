import frappe

def auto_generate_barcode(doc, method=None):
	"""
	Hook fired before creating any new Item.
	Automatically populates doc.barcodes with doc.item_code if no barcode exists.
	"""
	code_to_use = doc.item_code or doc.name
	if not code_to_use:
		return

	barcode_exists = False
	if doc.get("barcodes"):
		for b in doc.barcodes:
			if b.barcode == code_to_use:
				barcode_exists = True
				break

	if not barcode_exists:
		doc.append("barcodes", {
			"barcode": code_to_use
		})


def backfill_item_barcodes():
	"""
	Backfills barcodes for all existing items in the database that currently lack barcode entries.
	"""
	items = frappe.get_all("Item", fields=["name", "item_code"])
	count = 0
	for item in items:
		code = item.item_code or item.name
		if not code:
			continue
		
		# Check if barcode entry already exists
		exists = frappe.db.exists("Item Barcode", {"parent": item.name, "barcode": code})
		if not exists:
			b = frappe.get_doc({
				"doctype": "Item Barcode",
				"parent": item.name,
				"parentfield": "barcodes",
				"parenttype": "Item",
				"barcode": code
			})
			b.insert(ignore_permissions=True)
			count += 1

	frappe.db.commit()
	return count


def get_barcode_svg(text, height=80, bar_width=3, show_text=False):
	"""
	Generates Code 128 (B) vector SVG string for offline thermal/sticker printing.
	"""
	if not text:
		return ""

	text = str(text).strip()

	PATTERNS = [
		'212222', '222122', '222221', '121223', '121322', '131222', '122213', '122312', '132212', '221213',
		'221312', '231212', '112232', '122132', '122231', '113222', '123122', '123221', '223211', '221132',
		'221231', '213212', '223112', '312131', '311222', '321122', '321221', '312212', '322112', '322211',
		'212123', '212321', '232121', '111323', '131123', '131321', '112313', '132113', '132311', '211313',
		'231113', '231311', '112133', '112331', '132131', '113123', '113321', '133121', '313121', '211331',
		'231131', '213113', '213311', '213131', '311123', '311321', '331121', '312113', '312311', '332111',
		'314111', '221411', '431111', '111224', '111422', '121124', '121421', '141122', '141221', '112214',
		'112412', '122114', '122411', '142112', '142211', '241211', '221114', '413111', '241112', '134111',
		'111242', '121142', '121241', '114212', '124112', '124211', '411212', '421112', '421211', '212141',
		'214121', '412121', '111143', '111341', '131141', '114113', '114311', '411113', '411311', '113141',
		'114131', '311141', '411131', '211412', '211214', '211232', '2331112'
	]

	START_B = 104
	patterns = [PATTERNS[START_B]]
	checksum = START_B

	for i, char in enumerate(text):
		val = ord(char) - 32
		if 0 <= val < 95:
			patterns.append(PATTERNS[val])
			checksum += val * (i + 1)
		else:
			val = 0
			patterns.append(PATTERNS[val])
			checksum += val * (i + 1)

	checksum %= 103
	patterns.append(PATTERNS[checksum])
	patterns.append('2331112') # Stop code + termination bar

	pattern_str = ''.join(patterns)
	x = 10
	svg_elements = []
	is_bar = True

	for digit in pattern_str:
		w = int(digit) * bar_width
		if is_bar:
			svg_elements.append(f'<rect x="{x}" y="0" width="{w}" height="{height}" fill="#000000"/>')
		x += w
		is_bar = not is_bar

	total_width = x + 10
	svg_body = ''.join(svg_elements)

	text_element = ""
	view_height = height
	if show_text:
		text_x = total_width / 2
		text_element = f'<text x="{text_x}" y="{height + 14}" font-family="Arial, sans-serif" font-size="12" font-weight="bold" text-anchor="middle" fill="#000000">{text}</text>'
		view_height += 18

	return f'<svg xmlns="http://www.w3.org/2000/svg" width="100%" height="100%" viewBox="0 0 {total_width} {view_height}" preserveAspectRatio="none">{svg_body}{text_element}</svg>'


@frappe.whitelist()
def get_bulk_barcode_html(docname=None, receipt_name=None, doctype=None, code_type="barcode"):
	"""
	Generates raw HTML for bulk printing barcode / QR stickers based on a Purchase Receipt or Purchase Invoice items and quantities.
	"""
	name_to_use = docname or receipt_name
	if not name_to_use:
		frappe.throw("Document name is required")

	# Auto-detect doctype if not provided
	if not doctype:
		if receipt_name or name_to_use.startswith("MAT-PRE-") or frappe.db.exists("Purchase Receipt", name_to_use):
			doctype = "Purchase Receipt"
		elif name_to_use.startswith("ACC-PINV-") or frappe.db.exists("Purchase Invoice", name_to_use):
			doctype = "Purchase Invoice"
		else:
			doctype = "Purchase Receipt"

	doc = frappe.get_doc(doctype, name_to_use)
	
	html_parts = []
	doc_title = f"{doctype} - {name_to_use}"
	html_parts.append(f'''<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<title>Bulk Print Stickers - {doc_title}</title>
	<style>
		@page {{ size: 50mm 35mm; margin: 0; }}
		html, body {{ margin: 0; padding: 0; background-color: #ffffff; color: #000000; font-family: 'Segoe UI', Tahoma, Arial, sans-serif; }}
		.sticker {{
			width: 50mm;
			height: 35mm;
			box-sizing: border-box;
			page-break-after: always;
			overflow: hidden;
			display: flex;
			flex-direction: column;
			justify-content: space-between;
			padding: 1.5mm 1mm;
			text-align: center;
		}}
		.sticker:last-child {{
			page-break-after: auto;
		}}
		.header {{
			font-size: 11px;
			font-weight: 800;
			text-transform: uppercase;
			letter-spacing: 0.5px;
			white-space: nowrap;
			overflow: hidden;
			text-overflow: ellipsis;
			color: #000000;
		}}
		.subheader {{
			font-size: 11px;
			font-weight: bold;
			color: #000000;
			margin-bottom: 1mm;
			white-space: nowrap;
			overflow: hidden;
			text-overflow: ellipsis;
			unicode-bidi: plaintext;
		}}
		.code-container {{
			width: 46mm;
			height: 18mm;
			margin: 0 auto;
			display: flex;
			align-items: center;
			justify-content: center;
		}}
		.qr-image {{
			width: 18mm;
			height: 18mm;
			object-fit: contain;
			margin: 0 auto;
			display: block;
		}}
		.price {{
			font-size: 12px;
			font-weight: bold;
			color: #000000;
			margin-top: 1mm;
			white-space: nowrap;
			overflow: hidden;
			text-overflow: ellipsis;
		}}
	</style>
</head>
<body onload="setTimeout(function(){{ window.print(); }}, 500);">''')

	is_qr = (code_type == "qr")

	# Get items and their prices/barcodes
	for item_row in doc.items:
		item_doc = frappe.get_doc("Item", item_row.item_code)
		
		# Get barcode / QR code payload
		barcode_val = item_doc.item_code
		if item_doc.get("barcodes") and len(item_doc.barcodes) > 0 and item_doc.barcodes[0].barcode:
			barcode_val = item_doc.barcodes[0].barcode
		
		# Get selling price:
		# 1. Row custom selling rate if set
		item_price = (
			getattr(item_row, "custom_selling_rate", None)
			or getattr(item_row, "custom_selling_rate_", None)
			or getattr(item_row, "custom_selling_price", None)
		)
		# 2. Item Price list (selling: 1)
		if not item_price:
			item_price = frappe.db.get_value("Item Price", {"item_code": item_doc.name, "selling": 1}, "price_list_rate")
		# 3. Item standard/valuation rate
		if not item_price:
			item_price = item_doc.standard_rate or item_doc.valuation_rate or 0

		price_str = f"Price: {frappe.utils.fmt_money(item_price)}" if item_price else ""
		
		# Generate code element (QR image or 1D Barcode SVG)
		if is_qr:
			qr_uri = get_qr_code_base64(barcode_val)
			code_element = f'<img class="qr-image" src="{qr_uri}" alt="{barcode_val}" />'
		else:
			barcode_svg = get_barcode_svg(barcode_val, height=80, bar_width=3, show_text=False)
			code_element = barcode_svg

		# Generate QTY times
		qty = int(frappe.utils.flt(item_row.qty))
		if qty <= 0:
			qty = 1

		for _ in range(qty):
			sticker_html = f'''
		<div class="sticker">
			<div>
				<div class="header">{item_doc.item_code}</div>
				<div class="subheader" dir="auto">{item_doc.item_name}</div>
			</div>
			<div class="code-container">
				{code_element}
			</div>
			<div class="price">{price_str}</div>
		</div>'''
			html_parts.append(sticker_html)

	html_parts.append('</body></html>')
	return ''.join(html_parts)


def get_qr_code_base64(text):
	"""
	Generates a 2D QR Code PNG Base64 data URI string for instant scanning with any iPhone / Smartphone Camera.
	"""
	if not text:
		return ""
	import pyqrcode
	qr = pyqrcode.create(str(text).strip())
	base64_str = qr.png_as_base64_str(scale=5)
	return f"data:image/png;base64,{base64_str}"
