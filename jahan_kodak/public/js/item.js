frappe.ui.form.on('Item', {
    refresh(frm) {
        if (!frm.is_new()) {
            frm.add_custom_button(__('Print Barcode Label'), function() {
                frappe.prompt([
                    {
                        label: __('Quantity'),
                        fieldname: 'qty',
                        fieldtype: 'Int',
                        default: 1,
                        reqd: 1
                    }
                ], function(values) {
                    frappe.call({
                        method: 'jahan_kodak.print_sticker.print_item_label',
                        args: {
                            item_code: frm.doc.name,
                            qty: values.qty
                        },
                        freeze: true,
                        freeze_message: __('Sending to Label Printer...'),
                        callback: function(r) {
                            if (!r.exc && r.message) {
                                frappe.show_alert({
                                    message: r.message,
                                    indicator: 'green'
                                });
                            }
                        }
                    });
                }, __('Print Barcode Label'), __('Print'));
            }, __('Actions'));
        }
    }
});
