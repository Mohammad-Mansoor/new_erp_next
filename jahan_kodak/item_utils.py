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
