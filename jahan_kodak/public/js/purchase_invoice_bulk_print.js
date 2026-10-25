frappe.ui.form.on('Purchase Invoice', {
    refresh: function(frm) {
        if (!frm.is_new()) {
            frm.add_custom_button(__('Print Barcodes'), function() {
                frappe.call({
                    method: 'jahan_kodak.item_utils.get_bulk_barcode_html',
                    args: {
                        docname: frm.doc.name,
                        doctype: 'Purchase Invoice',
                        code_type: 'barcode'
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

            frm.add_custom_button(__('Print QR Codes'), function() {
                frappe.call({
                    method: 'jahan_kodak.item_utils.get_bulk_barcode_html',
                    args: {
                        docname: frm.doc.name,
                        doctype: 'Purchase Invoice',
                        code_type: 'qr'
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
