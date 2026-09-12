import frappe
from frappe import _
from frappe.utils import flt, get_datetime
from erpnext.accounts.doctype.pos_closing_entry.pos_closing_entry import POSClosingEntry
import erpnext.accounts.doctype.pos_closing_entry.pos_closing_entry as pce
from erpnext.accounts.doctype.pos_invoice_merge_log.pos_invoice_merge_log import (
	consolidate_pos_invoices,
)

def auto_consolidate_pos_invoice(doc, method=None):
	"""
	Synchronously consolidates a submitted POS Invoice immediately upon submission,
	creating the corresponding Sales Invoice (with update_stock=1), Stock Ledger Entries (SLE),
	General Ledger Entries (GLE), and Payment Ledger Entries (PLE) in real-time.
	"""
	if doc.docstatus != 1:
		return

	# Prevent re-entry / recursion if already consolidated or currently consolidating
	if doc.consolidated_invoice or getattr(frappe.flags, "in_pos_consolidation", False):
		return

	# Check DB to be 100% sure it's not already consolidated
	already_consolidated = frappe.db.get_value("POS Invoice", doc.name, "consolidated_invoice")
	if already_consolidated:
		return

	frappe.flags.in_pos_consolidation = True

	try:
		pos_transaction = [
			frappe._dict(
				{
					"pos_invoice": doc.name,
					"posting_date": doc.posting_date,
					"grand_total": doc.grand_total,
					"customer": doc.customer,
					"is_return": doc.is_return,
				}
			)
		]

		consolidate_pos_invoices(pos_invoices=pos_transaction)

	finally:
		frappe.flags.in_pos_consolidation = False


@frappe.whitelist()
def get_pos_invoices_for_closing(start, end, pos_profile, user):
	"""
	Returns all submitted POS Invoices for the cashier/profile in the specified timeframe,
	including those already consolidated in real-time, so POS Closing Entry can accurately
	display pos_transactions, payment reconciliation, taxes, and expected cash amounts.
	"""
	data = frappe.db.sql(
		"""
		select
			name, timestamp(posting_date, posting_time) as "timestamp"
		from
			`tabPOS Invoice`
		where
			owner = %s and docstatus = 1 and pos_profile = %s
		order by
			timestamp
		""",
		(user, pos_profile),
		as_dict=1,
	)

	data = list(filter(lambda d: get_datetime(start) <= get_datetime(d.timestamp) <= get_datetime(end), data))
	data = [frappe.get_doc("POS Invoice", d.name).as_dict() for d in data]

	return data

# Monkey-patch ERPNext's internal get_pos_invoices so backend functions (like make_closing_entry_from_opening)
# and frontend RPC calls both receive all shift invoices for complete reconciliation calculations.
pce.get_pos_invoices = get_pos_invoices_for_closing


class CustomPOSClosingEntry(POSClosingEntry):
	def validate_pos_invoices(self):
		invalid_rows = []
		for d in self.pos_transactions:
			invalid_row = {"idx": d.idx}
			pos_invoice = frappe.db.get_values(
				"POS Invoice",
				d.pos_invoice,
				["consolidated_invoice", "pos_profile", "docstatus", "owner"],
				as_dict=1,
			)[0]
			# Notice: We intentionally do NOT block invoices that have consolidated_invoice populated,
			# because under our real-time architecture, POS Invoices are consolidated immediately at checkout.
			if pos_invoice.pos_profile != self.pos_profile:
				invalid_row.setdefault("msg", []).append(
					_("POS Profile doesn't match {}").format(frappe.bold(self.pos_profile))
				)
			if pos_invoice.docstatus != 1:
				invalid_row.setdefault("msg", []).append(_("POS Invoice is not submitted"))
			if pos_invoice.owner != self.user:
				invalid_row.setdefault("msg", []).append(
					_("POS Invoice isn't created by user {}").format(frappe.bold(self.user))
				)

			if invalid_row.get("msg"):
				invalid_rows.append(invalid_row)

		if not invalid_rows:
			return

		error_list = []
		for row in invalid_rows:
			for msg in row.get("msg"):
				error_list.append(_("Row #{}: {}").format(row.get("idx"), msg))

		frappe.throw(error_list, title=_("Invalid POS Invoices"), as_list=True)

	def on_submit(self):
		unconsolidated_invoices = []
		for d in self.pos_transactions:
			consolidated = frappe.db.get_value("POS Invoice", d.pos_invoice, "consolidated_invoice")
			if not consolidated:
				unconsolidated_invoices.append(d)

		if unconsolidated_invoices:
			consolidate_pos_invoices(pos_invoices=unconsolidated_invoices, closing_entry=self)
		else:
			self.set_status(update=True, status="Submitted")
			self.db_set("error_message", "")
			self.update_opening_entry()

		frappe.publish_realtime(
			f"poe_{self.pos_opening_entry}_closed",
			self,
			docname=f"POS Opening Entry/{self.pos_opening_entry}",
		)
