frappe.provide("jahan_kodak.pos");

(function() {
	function getRouteStr() {
		if (typeof frappe === "undefined" || !frappe || !frappe.router || !frappe.router.current_route || typeof frappe.get_route_str !== "function") {
			return "";
		}
		try {
			return frappe.get_route_str() || "";
		} catch (e) {
			return "";
		}
	}

	function renderQuickReturn() {
		if (typeof $ === "undefined") return;
		const route = getRouteStr();
		if (route !== "point-of-sale" && !window.location.hash.includes("point-of-sale")) {
			return;
		}

		if ($("#pos-quick-return-wrapper").length > 0) {
			return; // Already rendered
		}

		const $pageActions = $(".page-head:visible .page-actions");
		const $customActions = $(".page-head:visible .custom-actions");
		const $target = $pageActions.length ? $pageActions : $customActions;

		if (!$target.length) {
			return;
		}

		const $returnContainer = $(`
			<div id="pos-quick-return-wrapper" style="display: inline-flex; align-items: center; margin-right: 10px; z-index: 999;">
				<input type="text" 
					id="pos-quick-return-input" 
					class="form-control input-sm" 
					placeholder="📷 Scan / Type Receipt # for Return..." 
					style="width: 250px; height: 32px; font-size: 12px; border: 2px solid #f39c12; border-radius: 6px; padding: 0 10px; background-color: #fffde7; color: #111; font-weight: 500;" />
				<button id="btn-quick-return-submit" class="btn btn-xs btn-warning ml-1" style="height: 32px; font-weight: bold; padding: 0 12px; border-radius: 6px; background-color: #f39c12; border-color: #e67e22; color: #fff;">
					Return ↵
				</button>
			</div>
		`);

		$target.prepend($returnContainer);

		const executeReturn = function () {
			const invoiceId = $("#pos-quick-return-input").val().trim();
			if (!invoiceId) {
				frappe.show_alert({ message: __("Please scan or type a Receipt #"), indicator: "orange" });
				return;
			}

			if (!window.cur_pos) {
				frappe.msgprint(__("POS Controller not initialized. Please refresh the POS page."));
				return;
			}

			frappe.dom.freeze(__("Checking Invoice for Return..."));

			frappe.db
				.get_doc("POS Invoice", invoiceId)
				.then((doc) => {
					if (!doc || !doc.name) {
						frappe.dom.unfreeze();
						frappe.msgprint({
							title: __("Invoice Not Found"),
							indicator: "red",
							message: __("Invoice <b>{0}</b> was not found in the system.", [frappe.utils.escape_html(invoiceId)]),
						});
						return;
					}

					if (doc.docstatus !== 1) {
						frappe.dom.unfreeze();
						frappe.msgprint({
							title: __("Cannot Return Invoice"),
							indicator: "orange",
							message: __("Invoice <b>{0}</b> is not submitted (DocStatus = {1}).", [frappe.utils.escape_html(invoiceId), doc.docstatus]),
						});
						return;
					}

					if (doc.is_return) {
						frappe.dom.unfreeze();
						frappe.msgprint({
							title: __("Already a Return Document"),
							indicator: "orange",
							message: __("Invoice <b>{0}</b> is already a return document.", [frappe.utils.escape_html(invoiceId)]),
						});
						return;
					}

					// Check if a return invoice has ALREADY been created against this original invoice
					frappe.db
						.get_value("POS Invoice", { return_against: doc.name, docstatus: 1 }, "name")
						.then((r) => {
							frappe.dom.unfreeze();

							if (r && r.message && r.message.name) {
								frappe.msgprint({
									title: __("Already Returned"),
									indicator: "orange",
									message: __("Invoice <b>{0}</b> has already been returned via Return Invoice <b>{1}</b>.", [
										frappe.utils.escape_html(doc.name),
										frappe.utils.escape_html(r.message.name),
									]),
								});
								return;
							}

							// Execute POS Return Flow
							frappe.run_serially([
								() => window.cur_pos.make_return_invoice(doc),
								() => window.cur_pos.cart.load_invoice(),
								() => window.cur_pos.item_selector.toggle_component(true),
							]);

							$("#pos-quick-return-input").val("");
							frappe.show_alert({
								message: __("Loaded return for Receipt <b>{0}</b>. Click Checkout to complete.", [frappe.utils.escape_html(invoiceId)]),
								indicator: "green",
							});
						})
						.catch(() => {
							frappe.dom.unfreeze();
						});
				})
				.catch((err) => {
					frappe.dom.unfreeze();
					frappe.msgprint({
						title: __("Error Loading Invoice"),
						indicator: "red",
						message: __("Could not fetch Invoice <b>{0}</b>. Please check the Receipt ID.", [frappe.utils.escape_html(invoiceId)]),
					});
				});
		};

		$(document).on("keypress", "#pos-quick-return-input", function (e) {
			if (e.which === 13) {
				e.preventDefault();
				executeReturn();
			}
		});

		$(document).on("click", "#btn-quick-return-submit", function () {
			executeReturn();
		});
	}

	function overridePosPaymentTotals() {
		if (!window.erpnext || !erpnext.PointOfSale || !erpnext.PointOfSale.Payment) {
			return;
		}

		if (erpnext.PointOfSale.Payment.prototype._totals_color_overridden) {
			return;
		}

		erpnext.PointOfSale.Payment.prototype._totals_color_overridden = true;

		erpnext.PointOfSale.Payment.prototype.update_totals_section = function (doc) {
			if (!doc) doc = this.events.get_frm().doc;
			const paid_amount = doc.paid_amount || 0;
			const disable_rounded = (typeof frappe !== "undefined" && frappe.sys_defaults) ? frappe.sys_defaults.disable_rounded_total : 0;
			const grand_total = cint(disable_rounded)
				? doc.grand_total
				: doc.rounded_total;
			const remaining = grand_total - paid_amount;
			const change = doc.change_amount || (remaining <= 0 ? -1 * remaining : undefined);
			const currency = doc.currency;
			const label = __("Change Amount");

			if (!this.$totals || !this.$totals.is(":visible")) {
				return;
			}

			const precision = (typeof frappe !== "undefined" && frappe.defaults) ? (frappe.defaults.get_default("currency_precision") || 2) : 2;
			const rem_flt = flt(remaining, precision);

			let value_style = "font-weight: 600;";
			if (rem_flt === 0) {
				value_style += " color: inherit;";
			} else if (rem_flt < 0) {
				value_style += " color: #28a745;";
			} else {
				value_style += " color: #dc3545;";
			}

			this.$totals.html(
				`<div class="col">
					<div class="total-label">${__("Grand Total")}</div>
					<div class="value">${format_currency(grand_total, currency)}</div>
				</div>
				<div class="seperator-y"></div>
				<div class="col">
					<div class="total-label">${__("Paid Amount")}</div>
					<div class="value">${format_currency(paid_amount, currency)}</div>
				</div>
				<div class="seperator-y"></div>
				<div class="col">
					<div class="total-label">${label}</div>
					<div class="value" style="${value_style}">${format_currency(change || remaining, currency)}</div>
				</div>`
			);
		};

		if (window.cur_pos && window.cur_pos.payment) {
			window.cur_pos.payment.update_totals_section();
		}
	}

	function applyItemCardVisibilityToggle() {
		if (typeof $ === "undefined") return;
		const route = getRouteStr();
		if (route !== "point-of-sale" && !window.location.hash.includes("point-of-sale")) {
			return;
		}

		if (!window.cur_pos) {
			return;
		}

		const $itemsSelector = $(".items-selector");
		if (!$itemsSelector.length) {
			return;
		}

		if ($("#pos-hide-item-cards-style").length === 0) {
			$("head").append(`
				<style id="pos-hide-item-cards-style">
					.items-selector.hide-item-cards-view .items-container,
					.items-selector.hide-item-cards-view .filter-section .label,
					.items-selector.hide-item-cards-view .filter-section .item-group-field {
						display: none !important;
					}
					.items-selector.hide-item-cards-view .filter-section .search-field {
						width: 100% !important;
						flex: 1 1 100% !important;
					}
					.items-selector.hide-item-cards-view .filter-section {
						margin-bottom: 0 !important;
					}
				</style>
			`);
		}

		const settings = window.cur_pos.settings || {};
		const hideCards = cint(settings.hide_item_cards) === 1;

		if (hideCards) {
			$itemsSelector.addClass("hide-item-cards-view");
		} else {
			$itemsSelector.removeClass("hide-item-cards-view");
		}
	}

	setInterval(renderQuickReturn, 1000);
	setInterval(overridePosPaymentTotals, 1000);
	setInterval(applyItemCardVisibilityToggle, 1000);

	if (typeof $ !== "undefined") {
		$(document).on("page-change route", function () {
			setTimeout(renderQuickReturn, 500);
			setTimeout(overridePosPaymentTotals, 500);
			setTimeout(applyItemCardVisibilityToggle, 500);
		});
	}
})();
