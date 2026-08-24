frappe.ui.form.on('Purchase Receipt', {
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
