frappe.ui.form.on('Purchase Receipt', {
    setup: function(frm) {
        frm.set_query('custom_selling_price_list', function() {
            return {
                filters: {
                    selling: 1
                }
            };
        });
    },
    refresh: function(frm) {
        if (!frm.is_new()) {
            frm.add_custom_button(__('Print Barcodes'), function() {
                frappe.call({
                    method: 'jahan_kodak.item_utils.get_bulk_barcode_html',
                    args: {
                        receipt_name: frm.doc.name
                    },
                    callback: function(r) {
                        if (r.message) {
                            var w = window.open();
                            w.document.write(r.message);
                            w.document.close();
                        }
                    }
                });
            }, __('Print'));
        }
    }
});

frappe.ui.form.on('Purchase Receipt Item', {
    item_code: function(frm, cdt, cdn) {
        let row = locals[cdt][cdn];
        if (row.item_code) {
            let price_list = frm.doc.custom_selling_price_list || 'Standard Selling';
            frappe.call({
                method: 'jahan_kodak.purchase_receipt_utils.get_item_selling_rate',
                args: {
                    item_code: row.item_code,
                    price_list: price_list
                },
                callback: function(r) {
                    if (r.message && !row.custom_selling_rate) {
                        frappe.model.set_value(cdt, cdn, 'custom_selling_rate', r.message);
                    }
                }
            });
        }
    }
});

