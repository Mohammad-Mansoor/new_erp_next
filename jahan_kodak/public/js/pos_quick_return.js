frappe.provide("jahan_kodak.pos");

$(document).ready(function () {
	// Periodically check if POS page wrapper is loaded
	const checkPOSLoaded = setInterval(function () {
		if (window.location.hash.includes("point-of-sale") && window.cur_pos) {
			initQuickReturnInput();
		}
	}, 1000);

	// Also listen on hash changes
	$(window).on("hashchange", function () {
		if (window.location.hash.includes("point-of-sale")) {
			setTimeout(initQuickReturnInput, 800);
		}
	});
});

function initQuickReturnInput() {
	if ($("#pos-quick-return-wrapper").length > 0) return;

	const $pageActions = $(".page-head:visible .page-actions");
	if (!$pageActions.length) return;

	const $returnContainer = $(`
		<div id="pos-quick-return-wrapper" style="display: inline-flex; align-items: center; margin-right: 12px;">
			<input type="text" 
				id="pos-quick-return-input" 
				class="form-control input-sm" 
				placeholder="📷 Scan / Type Receipt # for Return..." 
				style="width: 260px; height: 30px; font-size: 12px; border: 1.5px solid #ffa000; border-radius: 6px; padding: 0 10px; background-color: #fff9c4; color: #333;" />
			<button id="btn-quick-return-submit" class="btn btn-xs btn-warning ml-1" style="height: 30px; font-weight: bold; padding: 0 12px; border-radius: 6px;">
				Return ↵
			</button>
		</div>
	`);

	$pageActions.prepend($returnContainer);

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
						message: __("Invoice <b>{0}</b> was not found in the system.", [invoiceId]),
					});
					return;
				}

				if (doc.docstatus !== 1) {
					frappe.msgprint({
						title: __("Cannot Return Invoice"),
						indicator: "orange",
						message: __("Invoice <b>{0}</b> is not submitted.", [invoiceId]),
					});
					return;
				}

				if (doc.is_return) {
					frappe.msgprint({
						title: __("Already a Return"),
						indicator: "orange",
						message: __("Invoice <b>{0}</b> is already a return document.", [invoiceId]),
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
					message: __("Loaded return for Receipt <b>{0}</b>. Click Checkout to complete.", [invoiceId]),
					indicator: "green",
				});
			})
			.catch((err) => {
				frappe.dom.unfreeze();
				frappe.msgprint({
					title: __("Error Loading Invoice"),
					indicator: "red",
					message: __("Could not fetch Invoice <b>{0}</b>. Please check the Receipt ID.", [invoiceId]),
				});
			});
	};

	$("#pos-quick-return-input").on("keypress", function (e) {
		if (e.which === 13) {
			e.preventDefault();
			executeReturn();
		}
	});

	$("#btn-quick-return-submit").on("click", function () {
		executeReturn();
	});
}
