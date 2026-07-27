frappe.provide("jahan_kodak.pos");

$(document).ready(function () {
	// Register Frappe native keyboard shortcut for Spacebar
	frappe.ui.keys.add_shortcut({
		shortcut: "space",
		description: __("POS Checkout / Complete Order"),
		ignore_inputs: true,
		condition: () => {
			const checkoutBtn = $(".checkout-btn:visible");
			const submitOrderBtn = $(".submit-order-btn:visible");

			// Only run if either Checkout or Complete Order button is visible in POS
			if (!checkoutBtn.length && !submitOrderBtn.length) {
				return false;
			}

			const $focused = $(document.activeElement);
			// If user is inside an input/textarea, only trigger if input is empty
			if ($focused.is("input, select, textarea, [contenteditable=true]")) {
				const val = $focused.val();
				if (val && val.trim().length > 0) {
					return false; // User is typing text, do not trigger shortcut
				}
			}

			return true;
		},
		action: (e) => {
			const checkoutBtn = $(".checkout-btn:visible");
			const submitOrderBtn = $(".submit-order-btn:visible");

			if (submitOrderBtn.length) {
				submitOrderBtn.click();
				return true;
			}

			if (checkoutBtn.length) {
				checkoutBtn.click();
				return true;
			}
		},
	});
});

// Remove automatic focus on cash input when Checkout is clicked
$(document).on("click", ".checkout-btn", function () {
	const removeFocus = function () {
		if (document.activeElement) {
			document.activeElement.blur();
		}
		$(".mode-of-payment-control input, .payment-modes input, .fields-numpad-container input").blur();
	};

	setTimeout(removeFocus, 100);
	setTimeout(removeFocus, 300);
});
