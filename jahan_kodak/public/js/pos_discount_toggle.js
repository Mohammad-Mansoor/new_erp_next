/**
 * Jahan Kodak Custom POS Cart Extensions:
 * 1. Option A: Custom POS Discount Toggle (% vs Fixed Price)
 * 2. Option 3: Sticky Top-of-Cart Grand Total Card
 * 
 * Works cleanly with ERPNext POS and taxes_and_totals without modifying core files.
 */

frappe.provide("erpnext.PointOfSale");
frappe.provide("jahan_kodak.pos");

(function () {
	function initPOSCartCustomizations() {
		if (
			typeof erpnext === "undefined" ||
			!erpnext.PointOfSale ||
			!erpnext.PointOfSale.ItemCart
		) {
			setTimeout(initPOSCartCustomizations, 50);
			return;
		}

		const ItemCart = erpnext.PointOfSale.ItemCart;

		// Prevent multiple patching
		if (ItemCart.prototype.__jk_cart_customizations_patched) return;
		ItemCart.prototype.__jk_cart_customizations_patched = true;

		// -------------------------------------------------------------
		// Option 3: Sticky Top-of-Cart Grand Total Card
		// -------------------------------------------------------------
		ItemCart.prototype.make_top_grand_total_card = function () {
			if (!this.$component || this.$component.find(".pos-top-grand-total-card").length) {
				return;
			}

			const card_html = `
				<div class="pos-top-grand-total-card" style="
					background: linear-gradient(135deg, #0f766e 0%, #047857 100%);
					color: #ffffff;
					border-radius: var(--border-radius-md, 8px);
					padding: 10px 14px;
					margin-bottom: var(--margin-md, 12px);
					box-shadow: 0 4px 12px rgba(4, 120, 87, 0.22);
					display: flex;
					align-items: center;
					justify-content: space-between;
					flex-shrink: 0;
					box-sizing: border-box;
					width: 100%;
				">
					<div style="display: flex; flex-direction: column;">
						<span style="font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.8px; color: #a7f3d0;">
							${__("Grand Total Payable")}
						</span>
						<span class="pos-top-grand-total-value" style="font-size: 24px; font-weight: 900; line-height: 1.2; letter-spacing: -0.5px; color: #ffffff;">
							0.00 AFN
						</span>
					</div>
					<div style="display: flex; flex-direction: column; align-items: flex-end; justify-content: center;">
						<span class="pos-top-item-count" style="font-size: 12px; font-weight: 600; color: #d1fae5;">
							0 items
						</span>
						<span class="pos-top-discount-pill" style="display: none; font-size: 10px; font-weight: 700; background: rgba(255,255,255,0.25); padding: 1px 6px; border-radius: 4px; margin-top: 3px; color: #ffffff;">
							-0.00
						</span>
					</div>
				</div>
			`;

			this.$component.prepend(card_html);
		};

		// Hook into update_totals_section to keep top card synchronized
		const original_update_totals_section = ItemCart.prototype.update_totals_section;
		ItemCart.prototype.update_totals_section = function (frm) {
			original_update_totals_section.apply(this, arguments);

			this.make_top_grand_total_card();

			if (!frm) frm = this.events.get_frm();
			if (!frm || !frm.doc) return;

			const doc = frm.doc;
			const currency = doc.currency || frappe.boot.sysdefaults.currency || "AFN";
			const grand_total = cint(frappe.sys_defaults.disable_rounded_total)
				? doc.grand_total
				: doc.rounded_total;

			let total_qty = 0;
			(doc.items || []).forEach((item) => {
				total_qty += flt(item.qty);
			});

			const $card = this.$component.find(".pos-top-grand-total-card");
			if ($card.length) {
				$card.find(".pos-top-grand-total-value").text(format_currency(grand_total, currency));
				$card
					.find(".pos-top-item-count")
					.text(`${total_qty} ${total_qty === 1 ? __("item") : __("items")}`);

				const disc_amt = flt(doc.discount_amount);
				const $disc_pill = $card.find(".pos-top-discount-pill");
				if (disc_amt > 0) {
					$disc_pill.text(`-${format_currency(disc_amt, currency)}`).show();
				} else {
					$disc_pill.hide();
				}
			}
		};

		// -------------------------------------------------------------
		// Option A: Custom POS Discount Toggle (% vs Fixed Price)
		// -------------------------------------------------------------
		ItemCart.prototype.show_discount_control = function () {
			const me = this;
			const frm = me.events.get_frm();
			if (!frm || !frm.doc) return;

			// Respect POS Profile discount permissions
			if (!this.allow_discount_change) {
				frappe.show_alert({
					indicator: "red",
					message: __("Editing discount is not allowed as per POS Profile settings."),
				});
				frappe.utils.play_sound("error");
				return;
			}

			const doc = frm.doc;
			if (!doc.items || !doc.items.length) {
				frappe.show_alert({
					indicator: "orange",
					message: __("Please add items to cart before applying discount."),
				});
				frappe.utils.play_sound("error");
				return;
			}

			const curr_pct = flt(doc.additional_discount_percentage);
			const curr_amt = flt(doc.discount_amount);
			const currency = doc.currency || frappe.boot.sysdefaults.currency || "AFN";

			// Default mode is always Fixed Amount ("amount") unless percentage discount is already active
			let active_mode = curr_pct > 0 ? "percentage" : "amount";

			this.$add_discount_elem.css({
				padding: "0px",
				border: "none",
				background: "transparent",
			});

			const initial_val =
				active_mode === "percentage"
					? curr_pct > 0
						? curr_pct
						: ""
					: curr_amt > 0
					? curr_amt
					: "";

			const amt_placeholder = __("Enter fixed amount in {0} (e.g. 100)", [currency]);
			const pct_placeholder = __("Enter discount % (e.g. 10)");

			const html = `
				<div class="pos-discount-toggle-box" style="
					width: 100%;
					padding: 8px 10px;
					background: var(--card-bg, #ffffff);
					border: 1px solid var(--border-color, #d1d8dd);
					border-radius: var(--border-radius-md, 8px);
					box-shadow: 0 2px 6px rgba(0,0,0,0.08);
					box-sizing: border-box;
				">
					<div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 6px;">
						<span style="font-size: 11px; font-weight: 700; color: var(--text-muted, #6c757d); text-transform: uppercase; letter-spacing: 0.5px;">
							${__("Discount Type")}
						</span>
						<div class="btn-group btn-group-xs discount-mode-toggle" style="display: inline-flex; border-radius: 4px; overflow: hidden; border: 1px solid var(--border-color, #ced4da);">
							<button type="button" class="btn btn-xs btn-mode-amt ${
								active_mode === "amount"
									? "btn-primary text-white font-weight-bold"
									: "btn-default"
							}" style="padding: 2px 12px; font-size: 11px;">
								${currency} (${__("Fixed")})
							</button>
							<button type="button" class="btn btn-xs btn-mode-pct ${
								active_mode === "percentage"
									? "btn-primary text-white font-weight-bold"
									: "btn-default"
							}" style="padding: 2px 10px; font-size: 11px;">
								%
							</button>
						</div>
						<button type="button" class="btn btn-link btn-xs btn-disc-cancel text-muted" style="padding: 0 4px; font-size: 18px; line-height: 1; text-decoration: none;" title="${__(
							"Close"
						)}">
							&times;
						</button>
					</div>

					<div style="display: flex; gap: 6px; align-items: center;">
						<input type="number" step="any" min="0" class="form-control input-xs pos-discount-input" 
							placeholder="${active_mode === "amount" ? amt_placeholder : pct_placeholder}" 
							value="${initial_val}"
							style="height: 30px; font-size: 12px; font-weight: 600; border-radius: 4px;" />
						<button type="button" class="btn btn-primary btn-xs btn-apply-discount" style="height: 30px; padding: 0 12px; font-weight: 700; white-space: nowrap; border-radius: 4px;">
							${__("Apply")}
						</button>
						<button type="button" class="btn btn-danger btn-xs btn-clear-discount" style="height: 30px; padding: 0 8px; border-radius: 4px;" title="${__(
							"Remove Discount"
						)}">
							<i class="fa fa-trash"></i>
						</button>
					</div>
				</div>
			`;

			this.$add_discount_elem.html(html);

			const $box = this.$add_discount_elem.find(".pos-discount-toggle-box");
			const $input = $box.find(".pos-discount-input");
			const $btnAmt = $box.find(".btn-mode-amt");
			const $btnPct = $box.find(".btn-mode-pct");
			const $btnApply = $box.find(".btn-apply-discount");
			const $btnClear = $box.find(".btn-clear-discount");
			const $btnCancel = $box.find(".btn-disc-cancel");

			// Prevent clicks inside the discount box from bubbling to .add-discount-wrapper
			$box.on("click", function (e) {
				e.stopPropagation();
			});

			// Setup dummy discount_field to satisfy keyboard shortcuts (e.g. Escape)
			this.discount_field = {
				parent: this.$add_discount_elem,
				set_value: function () {
					me.hide_discount_control();
				},
			};

			// Mode switch to Fixed Amount
			$btnAmt.on("click", function (e) {
				e.preventDefault();
				active_mode = "amount";
				$btnAmt
					.removeClass("btn-default")
					.addClass("btn-primary text-white font-weight-bold");
				$btnPct
					.removeClass("btn-primary text-white font-weight-bold")
					.addClass("btn-default");
				$input.attr("placeholder", amt_placeholder);
				$input.focus().select();
			});

			// Mode switch to Percentage
			$btnPct.on("click", function (e) {
				e.preventDefault();
				active_mode = "percentage";
				$btnPct
					.removeClass("btn-default")
					.addClass("btn-primary text-white font-weight-bold");
				$btnAmt
					.removeClass("btn-primary text-white font-weight-bold")
					.addClass("btn-default");
				$input.attr("placeholder", pct_placeholder);
				if (flt($input.val()) > 100) {
					$input.val("");
				}
				$input.focus().select();
			});

			// Cancel / Close
			$btnCancel.on("click", function (e) {
				e.preventDefault();
				me.hide_discount_control();
			});

			// Clear discount
			$btnClear.on("click", function (e) {
				e.preventDefault();
				me.apply_discount_values(0, "clear");
			});

			// Apply discount logic
			const doApply = function () {
				const val = flt($input.val());

				if (val < 0) {
					frappe.msgprint({
						title: __("Invalid Discount"),
						indicator: "red",
						message: __("Discount cannot be negative."),
					});
					frappe.utils.play_sound("error");
					return;
				}

				if (val === 0) {
					me.apply_discount_values(0, "clear");
					return;
				}

				if (active_mode === "percentage") {
					if (val > 100) {
						frappe.msgprint({
							title: __("Invalid Discount"),
							indicator: "red",
							message: __("Discount percentage cannot be greater than 100%."),
						});
						frappe.utils.play_sound("error");
						return;
					}
					me.apply_discount_values(val, "percentage");
				} else {
					// Fixed Amount
					const total_before_discount = flt(doc.grand_total) + flt(doc.discount_amount);
					if (val > total_before_discount && total_before_discount > 0) {
						frappe.msgprint({
							title: __("Invalid Discount"),
							indicator: "red",
							message: __(
								"Discount amount ({0}) cannot be greater than the total bill ({1}).",
								[
									format_currency(val, currency),
									format_currency(total_before_discount, currency),
								]
							),
						});
						frappe.utils.play_sound("error");
						return;
					}
					me.apply_discount_values(val, "amount");
				}
			};

			$btnApply.on("click", function (e) {
				e.preventDefault();
				doApply();
			});

			$input.on("keydown", function (e) {
				if (e.key === "Enter" || e.keyCode === 13) {
					e.preventDefault();
					doApply();
				} else if (e.key === "Escape" || e.keyCode === 27) {
					e.preventDefault();
					me.hide_discount_control();
				}
			});

			setTimeout(() => {
				$input.focus().select();
			}, 50);
		};

		// Helper to apply discount values cleanly to the POS Invoice model
		ItemCart.prototype.apply_discount_values = function (val, mode) {
			const me = this;
			const frm = me.events.get_frm();
			if (!frm || !frm.doc) return;

			const doc = frm.doc;
			const dt = doc.doctype;
			const dn = doc.name;
			const num_val = flt(val);

			frappe.dom.freeze();

			let promise;

			if (num_val <= 0 || mode === "clear") {
				// Clear discount
				promise = frappe.model
					.set_value(dt, dn, "additional_discount_percentage", 0)
					.then(() => frappe.model.set_value(dt, dn, "discount_amount", 0));
			} else if (mode === "percentage") {
				// Apply Percentage:
				// Ensure apply_discount_on is Grand Total, then set additional_discount_percentage.
				// transaction.js will automatically calculate and set discount_amount = total * pct / 100.
				// Do NOT call set_value("discount_amount", 0) here, or it wipes out the discount!
				promise = frappe.model
					.set_value(dt, dn, "apply_discount_on", "Grand Total")
					.then(() => frappe.model.set_value(dt, dn, "additional_discount_percentage", num_val));
			} else {
				// Apply Fixed Amount:
				// First reset percentage to 0, ensure Grand Total, then set discount_amount.
				promise = frappe.model
					.set_value(dt, dn, "apply_discount_on", "Grand Total")
					.then(() => frappe.model.set_value(dt, dn, "additional_discount_percentage", 0))
					.then(() => frappe.model.set_value(dt, dn, "discount_amount", num_val));
			}

			promise
				.then(() => {
					if (frm.cscript && typeof frm.cscript.calculate_taxes_and_totals === "function") {
						frm.cscript.calculate_taxes_and_totals();
					}
					frm.refresh_fields();
					me.hide_discount_control();
					me.update_totals_section(frm);
					frappe.dom.unfreeze();
				})
				.catch((err) => {
					console.error("Error applying POS discount:", err);
					frappe.dom.unfreeze();
				});
		};

		// Override hide_discount_control to show % or Fixed Amount tag
		ItemCart.prototype.hide_discount_control = function () {
			const frm = this.events.get_frm();
			const doc = frm ? frm.doc : {};
			const percent = flt(doc.additional_discount_percentage);
			const amount = flt(doc.discount_amount);
			const currency = doc.currency || frappe.boot.sysdefaults.currency || "AFN";

			this.discount_field = undefined;

			if (!percent && !amount) {
				this.$add_discount_elem.css({
					border: "1px dashed var(--gray-500, #adb5bd)",
					padding: "var(--padding-sm, 6px) var(--padding-md, 12px)",
					background: "transparent",
				});
				this.$add_discount_elem.html(`${this.get_discount_icon()} ${__("Add Discount")}`);
			} else {
				this.$add_discount_elem.css({
					border: "1px dashed var(--dark-green-500, #28a745)",
					padding: "var(--padding-sm, 6px) var(--padding-md, 12px)",
					background: "transparent",
				});

				let discount_desc = "";
				if (percent > 0) {
					discount_desc = `${__("Additional")}&nbsp;<b style="color: #28a745;">${percent}%</b> (${format_currency(
						amount,
						currency
					)}) ${__("discount applied")}`;
				} else {
					discount_desc = `${__("Additional")}&nbsp;<b style="color: #28a745;">${format_currency(
						amount,
						currency
					)}</b> ${__("discount applied")}`;
				}

				this.$add_discount_elem.html(`
					<div class="edit-discount-btn" style="display: flex; align-items: center; justify-content: space-between; width: 100%; cursor: pointer;">
						<div style="display: flex; align-items: center;">
							${this.get_discount_icon()} ${discount_desc}
						</div>
						<span class="text-muted" style="font-size: 11px; margin-left: auto;">(${__("Edit")})</span>
					</div>
				`);
			}
		};

		// Polish PastOrderSummary if present
		if (erpnext.PointOfSale.PastOrderSummary) {
			erpnext.PointOfSale.PastOrderSummary.prototype.get_discount_html = function (doc) {
				if (doc && doc.discount_amount) {
					const percent = flt(doc.additional_discount_percentage);
					const label =
						percent > 0
							? `${__("Discount")} (${percent} %)`
							: `${__("Discount")} (${__("Fixed")})`;
					return `<div class="summary-row">
						<div>${label}</div>
						<div>${format_currency(doc.discount_amount, doc.currency)}</div>
					</div>`;
				}
				return "";
			};
		}
	}

	initPOSCartCustomizations();

	$(document).on("page-change", function () {
		if (frappe.get_route_str() === "point-of-sale") {
			initPOSCartCustomizations();
		}
	});
})();
