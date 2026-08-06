frappe.provide("jahan_kodak.pos");

(function() {
	function renderQuickReturn() {
		const route = frappe.get_route_str();
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

			frappe.dom.freeze(__("Fetching Invoice for Return..."));

			frappe.db
				.get_doc("POS Invoice", invoiceId)
				.then((doc) => {
					frappe.dom.unfreeze();

					if (!doc || !doc.name) {
						frappe.msgprint({
							title: __("Invoice Not Found"),
							indicator: "red",
							message: __("Invoice <b>{0}</b> was not found in the system.", [frappe.utils.escape_html(invoiceId)]),
						});
						return;
					}

					if (doc.docstatus !== 1) {
						frappe.msgprint({
							title: __("Cannot Return Invoice"),
							indicator: "orange",
							message: __("Invoice <b>{0}</b> is not submitted (DocStatus = {1}).", [frappe.utils.escape_html(invoiceId), doc.docstatus]),
						});
						return;
					}

					if (doc.is_return) {
						frappe.msgprint({
							title: __("Already a Return"),
							indicator: "orange",
							message: __("Invoice <b>{0}</b> is already a return document.", [frappe.utils.escape_html(invoiceId)]),
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

	setInterval(renderQuickReturn, 1000);

	$(document).on("page-change route", function () {
		setTimeout(renderQuickReturn, 500);
	});
})();
