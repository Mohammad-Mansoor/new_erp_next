frappe.provide("jahan_kodak.pos");

jahan_kodak.POSExchangeUI = class POSExchangeUI {
    constructor(opts) {
        this.original_invoice_doc = opts.original_invoice;
        this.idempotency_key = frappe.utils.get_random(20);
        
        this.state = {
            return_items: {},      // item_code: qty
            replacement_items: [], // [{item_code, qty}]
            preview: null,
            submitting: false,
            loading: false
        };
        
        this.setup_overlay();
        this.render_base_layout();
        this.bind_events();
        this.fetch_remaining_quantities();
        this.setup_item_search();
        this.calculate_exchange();
    }

    setup_overlay() {
        this.$wrapper = $(`<div class="pos-exchange-overlay" style="
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            background-color: var(--bg-color, #f8f9fa);
            z-index: 10000;
            overflow-y: auto;
            padding: 20px;
            display: flex;
            justify-content: center;
        ">
            <div class="exchange-container" style="
                width: 100%;
                max-width: 1000px;
                background: var(--card-bg, #ffffff);
                border-radius: 8px;
                box-shadow: var(--shadow-sm);
                padding: 20px;
                display: flex;
                flex-direction: column;
                gap: 20px;
            ">
            </div>
        </div>`);
        $("body").append(this.$wrapper);
    }

    render_base_layout() {
        const doc = this.original_invoice_doc;
        const container = this.$wrapper.find(".exchange-container");
        
        container.html(`
            <!-- Header -->
            <div class="exchange-header" style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid var(--border-color); padding-bottom: 15px;">
                <div>
                    <h3 style="margin: 0; color: var(--text-color);">${__("POS EXCHANGE")}</h3>
                    <div style="color: var(--text-muted); margin-top: 5px;">
                        <strong>${__("Original Invoice:")}</strong> ${doc.name} | <strong>${__("Customer:")}</strong> ${doc.customer}
                    </div>
                </div>
                <button class="btn btn-default btn-cancel-exchange" style="font-weight: bold;">${__("✕ Cancel")}</button>
            </div>

            <div class="row">
                <!-- Left Column (Items) -->
                <div class="col-md-8">
                    <!-- Return Items -->
                    <div class="exchange-section return-items-section">
                        <h4 style="margin-top: 0;">${__("Return Items")}</h4>
                        <table class="table table-bordered">
                            <thead class="bg-light">
                                <tr>
                                    <th>${__("Item")}</th>
                                    <th class="text-right">${__("Price")}</th>
                                    <th class="text-right">${__("Original Qty")}</th>
                                    <th class="text-right">${__("Already Returned")}</th>
                                    <th class="text-right">${__("Remaining")}</th>
                                    <th class="text-center" style="width: 120px;">${__("Return Qty")}</th>
                                    <th class="text-right">${__("Total Price")}</th>
                                </tr>
                            </thead>
                            <tbody id="return-items-body">
                                <tr><td colspan="7" class="text-center text-muted">${__("Calculating returnable quantities...")}</td></tr>
                            </tbody>
                        </table>
                    </div>

                    <!-- Replacement Items -->
                    <div class="exchange-section replacement-items-section mt-4">
                        <h4>${__("Replacement Items")}</h4>
                        <div class="form-group">
                            <input type="text" id="replacement-item-search" class="form-control" placeholder="${__('📷 Scan barcode or search item...')}" style="border: 2px solid #3498db; font-size: 14px;">
                        </div>
                        <table class="table table-bordered">
                            <thead class="bg-light">
                                <tr>
                                    <th>${__("Item")}</th>
                                    <th class="text-right" style="width: 100px;">${__("Qty")}</th>
                                    <th class="text-right">${__("Price")}</th>
                                    <th class="text-right">${__("Total Price")}</th>
                                    <th class="text-center" style="width: 50px;"></th>
                                </tr>
                            </thead>
                            <tbody id="replacement-items-body">
                                <tr><td colspan="5" class="text-center text-muted">${__("No replacement items selected.")}</td></tr>
                            </tbody>
                        </table>
                    </div>
                </div>

                <!-- Right Column (Summary) -->
                <div class="col-md-4">
                    <div class="exchange-summary-box p-4" style="background: var(--bg-light); border-radius: 8px; border: 1px solid var(--border-color);">
                        <h4 style="margin-top: 0; border-bottom: 1px solid var(--border-color); padding-bottom: 10px;">${__("Exchange Summary")}</h4>
                        
                        <div style="display: flex; justify-content: space-between; margin-bottom: 10px; font-size: 15px;">
                            <span>${__("Returned Amount:")}</span>
                            <strong id="summary-returned-amount">0.00</strong>
                        </div>
                        <div style="display: flex; justify-content: space-between; margin-bottom: 15px; font-size: 15px;">
                            <span>${__("Replacement Amount:")}</span>
                            <strong id="summary-replacement-amount">0.00</strong>
                        </div>
                        
                        <hr>
                        
                        <div class="text-center mb-3">
                            <div id="summary-settlement-label" style="font-size: 12px; font-weight: bold; color: var(--text-muted); text-transform: uppercase;">${__("NO PAYMENT REQUIRED")}</div>
                            <div id="summary-difference" style="font-size: 28px; font-weight: bold; color: var(--text-color);">0.00</div>
                        </div>

                        <div id="payment-method-container" style="display: none; margin-bottom: 20px;">
                            <label style="font-size: 12px;">${__("Payment Method")}</label>
                            <select id="payment-method-select" class="form-control"></select>
                        </div>

                        <button id="btn-submit-exchange" class="btn btn-primary btn-block btn-lg" style="font-weight: bold;">
                            ${__("EXCHANGE & SUBMIT")}
                        </button>
                    </div>
                </div>
            </div>
        `);
        
        // Initial setup
        this.fetch_remaining_quantities();
        this.setup_item_search();
    }

    fetch_remaining_quantities() {
        frappe.call({
            method: "jahan_kodak.api.pos_exchange.service.get_remaining_returnable_qty",
            args: {
                original_invoice_name: this.original_invoice_doc.name
            },
            callback: (r) => {
                this.remaining_qty_map = r.message || {};
                this.render_return_items();
            }
        });
    }

    render_return_items() {
        const tbody = this.$wrapper.find("#return-items-body");
        tbody.empty();

        let has_returnable = false;

        this.original_invoice_doc.items.forEach(item => {
            // Already returned = original - remaining
            const remaining = this.remaining_qty_map[item.item_code] || 0;
            const already_returned = item.qty - remaining;
            
            if (remaining > 0) {
                has_returnable = true;
                const current_return_qty = this.state.return_items[item.item_code] || 0;
                
                const tr = $(`
                    <tr>
                        <td><strong>${item.item_name}</strong><br><small class="text-muted">${item.item_code}</small></td>
                        <td class="text-right">${format_currency(item.rate, this.original_invoice_doc.currency)}</td>
                        <td class="text-right">${item.qty}</td>
                        <td class="text-right">${already_returned}</td>
                        <td class="text-right" style="font-weight: bold;">${remaining}</td>
                        <td class="text-center">
                            <input type="number" 
                                class="form-control input-sm text-center return-qty-input" 
                                data-item-code="${item.item_code}" 
                                data-remaining="${remaining}"
                                data-rate="${item.rate}"
                                min="0" 
                                max="${remaining}" 
                                value="${current_return_qty > 0 ? current_return_qty : ''}" 
                                placeholder="0" />
                        </td>
                        <td class="text-right font-weight-bold return-amount-cell">
                            ${format_currency(current_return_qty * item.rate, this.original_invoice_doc.currency)}
                        </td>
                    </tr>
                `);
                tbody.append(tr);
            }
        });

        if (!has_returnable) {
            tbody.html('<tr><td colspan="7" class="text-center text-muted">${__("No returnable items available on this invoice.")}</td></tr>');
            frappe.show_alert({message: __("This invoice has no remaining items available for return."), indicator: "orange"});
        }
    }

    render_replacement_items() {
        const tbody = this.$wrapper.find("#replacement-items-body");
        tbody.empty();

        if (this.state.replacement_items.length === 0) {
            tbody.html('<tr><td colspan="5" class="text-center text-muted">${__("No replacement items selected.")}</td></tr>');
            return;
        }

        // If we have preview data, use it for authoritative rates/amounts
        let preview_items_map = {};
        if (this.state.preview && this.state.preview.replacement_items_preview) {
            this.state.preview.replacement_items_preview.forEach(p => {
                preview_items_map[p.item_code] = p;
            });
        }

        this.state.replacement_items.forEach((item, index) => {
            const preview_data = preview_items_map[item.item_code] || {};
            const rate = preview_data.rate !== undefined ? format_currency(preview_data.rate, this.original_invoice_doc.currency) : "---";
            const amount = preview_data.amount !== undefined ? format_currency(preview_data.amount, this.original_invoice_doc.currency) : "---";

            const tr = $(`
                <tr>
                    <td><strong>${item.item_code}</strong></td>
                    <td class="text-right">
                        <input type="number" class="form-control input-sm text-center replace-qty-input" data-index="${index}" min="1" value="${item.qty}">
                    </td>
                    <td class="text-right">${rate}</td>
                    <td class="text-right font-weight-bold">${amount}</td>
                    <td class="text-center">
                        <button class="btn btn-xs btn-danger btn-remove-replace" data-index="${index}">✕</button>
                    </td>
                </tr>
            `);
            tbody.append(tr);
        });
    }

    setup_item_search() {
        const me = this;
        const $input = this.$wrapper.find("#replacement-item-search");


        // Handle barcode scanner 'Enter' explicitly
        $input.on("keypress", function(e) {
            if (e.which === 13) {
                e.preventDefault();
                e.stopPropagation();
                e.stopImmediatePropagation();
                const term = $(this).val().trim();
                if (term) {
                    frappe.call({
                        method: "erpnext.selling.page.point_of_sale.point_of_sale.get_items",
                        args: {
                            search_term: term,
                            pos_profile: me.original_invoice_doc.pos_profile,
                            price_list: me.original_invoice_doc.selling_price_list,
                            page_length: 1,
                            start: 0,
                            item_group: ""
                        },
                        callback: function(r) {
                            if (r.message && r.message.barcode) {
                                me.add_replacement_item(r.message.barcode);
                            } else if (r.message && r.message.items && r.message.items.length > 0) {
                                me.add_replacement_item(r.message.items[0].item_code);
                            } else {
                                frappe.show_alert({message: __("Item not found"), indicator: "orange"});
                            }
                            $input.val('');
                        }
                    });
                }
            }
        });
    }

    add_replacement_item(item_code) {
        // Merge identical items
        const existing = this.state.replacement_items.find(i => i.item_code === item_code);
        if (existing) {
            existing.qty += 1;
        } else {
            this.state.replacement_items.push({ item_code: item_code, qty: 1 });
        }
        this.render_replacement_items();
        this.debounce_calculate();
    }

    bind_events() {
        const me = this;
        
        this.$wrapper.on("click", ".btn-cancel-exchange", () => {
            this.close();
        });

        // Handle return qty inputs
        this.$wrapper.on("input", ".return-qty-input", function() {
            const item_code = $(this).attr("data-item-code");
            let val = parseInt($(this).val()) || 0;
            const max = parseInt($(this).attr("data-remaining"));
            
            if (val > max) {
                val = max;
                $(this).val(val);
                frappe.show_alert({message: __("Max returnable for {0} is {1}", [item_code, max]), indicator: "orange"});
            }
            if (val < 0) {
                val = 0;
                $(this).val('');
            }
            
            if (val > 0) {
                me.state.return_items[item_code] = val;
            } else {
                delete me.state.return_items[item_code];
            }
            
            // Instantly update the Total Price cell for this row
            const rate = parseFloat($(this).attr("data-rate")) || 0;
            $(this).closest("tr").find(".return-amount-cell").text(format_currency(val * rate, me.original_invoice_doc.currency));
            me.debounce_calculate();
        });

        // Handle replacement qty edits
        this.$wrapper.on("input", ".replace-qty-input", function() {
            const idx = parseInt($(this).attr("data-index"));
            let val = parseFloat($(this).val()) || 1;
            if (val <= 0) val = 1;
            
            me.state.replacement_items[idx].qty = val;
            me.debounce_calculate();
        });

        // Handle replacement item removal
        this.$wrapper.on("click", ".btn-remove-replace", function() {
            const idx = parseInt($(this).attr("data-index"));
            me.state.replacement_items.splice(idx, 1);
            me.render_replacement_items();
            me.debounce_calculate();
        });

        // Handle Submit
        this.$wrapper.on("click", "#btn-submit-exchange", () => {
            this.submit_exchange();
        });
    }

    debounce_calculate() {
        if (this.calc_timeout) clearTimeout(this.calc_timeout);
        this.calc_timeout = setTimeout(() => {
            this.calculate_exchange();
        }, 400); // 400ms debounce
    }

    get_payload() {
        // Build payload matching service.py contract
        const ret_items = [];
        for (const [item_code, qty] of Object.entries(this.state.return_items)) {
            ret_items.push({ item_code: item_code, qty: parseFloat(qty) });
        }
        
        return {
            idempotency_key: this.idempotency_key,
            original_invoice: this.original_invoice_doc.name,
            return_items: ret_items,
            new_items: [...this.state.replacement_items],
            payments: [] // Populated during submit
        };
    }

    calculate_exchange() {
        const payload = this.get_payload();
        
        // If no items, reset summary
        if (payload.return_items.length === 0 && payload.new_items.length === 0) {
            this.state.preview = null;
            this.update_summary_ui();
            return;
        }

        frappe.call({
            method: "jahan_kodak.api.pos_exchange.service.calculate_exchange",
            args: { payload: payload },
            callback: (r) => {
                if (!r.exc && r.message) {
                    this.state.preview = r.message;
                    this.render_replacement_items(); // Update authoritative prices
                    this.update_summary_ui();
                }
            }
        });
    }

    update_summary_ui() {
        const currency = this.original_invoice_doc.currency;
        
        if (!this.state.preview) {
            this.$wrapper.find("#summary-returned-amount").text(format_currency(0, currency));
            this.$wrapper.find("#summary-replacement-amount").text(format_currency(0, currency));
            this.$wrapper.find("#summary-difference").text(format_currency(0, currency));
            this.$wrapper.find("#summary-settlement-label").text("NO PAYMENT REQUIRED").css("color", "var(--text-muted)");
            this.$wrapper.find("#payment-method-container").hide();
            return;
        }

        const p = this.state.preview;
        
        this.$wrapper.find("#summary-returned-amount").text(format_currency(Math.abs(p.return_total), p.currency));
        this.$wrapper.find("#summary-replacement-amount").text(format_currency(p.replacement_total, p.currency));
        
        let label_text = __("NO PAYMENT REQUIRED");
        let label_color = "var(--text-muted)";
        let diff_color = "var(--text-color)";
        
        if (p.settlement_type === "customer_pays") {
            label_text = __("CUSTOMER PAYS");
            label_color = "#dc3545"; // Red
            diff_color = "#dc3545";
        } else if (p.settlement_type === "customer_refund") {
            label_text = __("CUSTOMER REFUND");
            label_color = "#28a745"; // Green
            diff_color = "#28a745";
        }

        this.$wrapper.find("#summary-settlement-label").text(label_text).css("color", label_color);
        this.$wrapper.find("#summary-difference").text(format_currency(Math.abs(p.difference), p.currency)).css("color", diff_color);

        const pm_container = this.$wrapper.find("#payment-method-container");
        const pm_select = this.$wrapper.find("#payment-method-select");
        
        if (p.payment_required && p.settlement_type === "customer_pays") {
            pm_container.show();
            if (pm_select.children().length === 0 && p.payment_methods) {
                // Populate dropdown once
                p.payment_methods.forEach(pm => {
                    pm_select.append(`<option value="${pm.mode_of_payment}" ${pm.default ? 'selected' : ''}>${pm.mode_of_payment}</option>`);
                });
            }
        } else {
            pm_container.hide();
        }
    }

    submit_exchange() {
        const payload = this.get_payload();
        
        if (payload.return_items.length === 0 && payload.new_items.length === 0) {
            frappe.show_alert({message: __("Please select items to return or replace."), indicator: "orange"});
            return;
        }

        if (this.state.submitting) return; // Double click protection
        
        const preview = this.state.preview;
        if (!preview) {
            frappe.show_alert({message: __("Still calculating totals, please wait..."), indicator: "orange"});
            return;
        }

        // Prepare payment object if required
        if (preview.payment_required && preview.settlement_type === "customer_pays") {
            const mode = this.$wrapper.find("#payment-method-select").val();
            if (!mode) {
                frappe.show_alert({message: __("Please select a payment method."), indicator: "red"});
                return;
            }
            payload.payments = [{
                mode_of_payment: mode,
                amount: Math.abs(preview.difference)
            }];
        } else if (preview.payment_required && preview.settlement_type === "customer_refund") {
            // For refund, backend handles the default cash refund if not specified, 
            // or we pass the default POS refund mode. We'll pass Cash by default.
            payload.payments = [{
                mode_of_payment: "Cash",
                amount: preview.difference // negative
            }];
        }

        // Lock UI
        this.state.submitting = true;
        const btn = this.$wrapper.find("#btn-submit-exchange");
        btn.prop("disabled", true).text(__("PROCESSING..."));

        frappe.call({
            method: "jahan_kodak.api.pos_exchange.service.process_exchange",
            args: { payload: payload },
            callback: (r) => {
                if (r.message && r.message.status === "success") {
                    this.show_success(r.message);
                }
            },
            error: (r) => {
                this.state.submitting = false;
                btn.prop("disabled", false).text(__("EXCHANGE & SUBMIT"));
                // The frappe.call automatically shows the user-friendly exception thrown by validators.py
            }
            // In case of timeout, state.submitting remains true, blocking further clicks.
            // If the user refreshes, they can retry. The idempotency_key prevents duplication.
        });
    }

    show_success(result) {
        const container = this.$wrapper.find(".exchange-container");
        let settlement_text = __("NO PAYMENT REQUIRED");
        if (result.settlement_type === "customer_pays") {
            settlement_text = __("CUSTOMER PAYS: {0}", [format_currency(result.difference, this.original_invoice_doc.currency)]);
        } else if (result.settlement_type === "customer_refund") {
            settlement_text = __("CUSTOMER REFUND: {0}", [format_currency(Math.abs(result.difference), this.original_invoice_doc.currency)]);
        }

        container.html(`
            <div class="text-center" style="padding: 40px 20px;">
                <h2 style="color: #28a745; margin-bottom: 20px;">✓ ${__("EXCHANGE COMPLETED")}</h2>
                
                <div style="font-size: 16px; line-height: 2; margin-bottom: 30px;">
                    <div><strong>${__("Exchange:")}</strong> ${result.exchange_id}</div>
                    <div><strong>${__("Original:")}</strong> ${result.original_invoice}</div>
                    ${result.return_invoice ? `<div><strong>${__("Return:")}</strong> ${result.return_invoice}</div>` : ''}
                    ${result.new_invoice ? `<div><strong>${__("New Sale:")}</strong> ${result.new_invoice}</div>` : ''}
                </div>
                
                <h3 style="margin-bottom: 40px; color: var(--text-color);">${settlement_text}</h3>
                
                <div style="display: flex; justify-content: center; gap: 20px;">
                    <button class="btn btn-default btn-lg btn-print-receipt" data-exchange="${result.exchange_id}">${__("PRINT RECEIPT")}</button>
                    <button class="btn btn-primary btn-lg btn-close-success">${__("NEW EXCHANGE / CLOSE")}</button>
                </div>
            </div>
        `);

        container.on("click", ".btn-print-receipt", function() {
            const exchange_id = $(this).attr("data-exchange");
            frappe.utils.print(
                "POS Exchange", 
                exchange_id, 
                "POS Exchange Receipt", 
                null, 
                frappe.boot.lang
            );
        });

        container.on("click", ".btn-close-success", () => {
            this.close();
            // Refresh POS cart if necessary, but returning to POS clears it
        });
    }

    close() {
        this.$wrapper.remove();
        // Remove object reference
        if (window.cur_pos_exchange) {
            delete window.cur_pos_exchange;
        }
    }
}
