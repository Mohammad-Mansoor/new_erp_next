frappe.provide("jahan_kodak.pos");

function removePaymentFocus() {
	const doBlur = () => {
		const activeElem = document.activeElement;
		if (activeElem && $(activeElem).closest(".payment-container, .payment-modes").length) {
			activeElem.blur();
		}
		$(".payment-container input, .mode-of-payment-control input").blur();
	};

	setTimeout(doBlur, 50);
	setTimeout(doBlur, 150);
	setTimeout(doBlur, 300);
}

$(document).on("keydown", function (e) {
	// Check if key pressed is Enter (keyCode 13) or Spacebar (keyCode 32)
	const isEnterKey = e.key === "Enter" || e.keyCode === 13;
	const isSpaceKey = e.key === " " || e.keyCode === 32;

	if (isEnterKey || isSpaceKey) {
		const activeElem = document.activeElement;

		// Only bypass if user is actively typing in the main Item/Customer search bar
		const isSearchInput = activeElem && $(activeElem).closest(".search-field, .item-search-field, .customer-field").length > 0;

		if (!isSearchInput) {
			const checkoutBtn = $(".checkout-btn:visible");
			const submitOrderBtn = $(".submit-order-btn:visible");

			if (checkoutBtn.length) {
				e.preventDefault();
				checkoutBtn.click();
				removePaymentFocus();
			} else if (submitOrderBtn.length) {
				e.preventDefault();
				submitOrderBtn.click();
			}
		}
	}
});

// Remove automatic focus on cash input when Checkout button is clicked
$(document).on("click", ".checkout-btn", function () {
	removePaymentFocus();
});
