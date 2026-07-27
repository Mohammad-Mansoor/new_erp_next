frappe.provide("jahan_kodak.pos");

function isTextInput(elem) {
	if (!elem) return false;
	const tag = elem.tagName;
	if (tag === "TEXTAREA" || elem.isContentEditable) return true;
	if (tag === "INPUT") {
		const type = (elem.type || "text").toLowerCase();
		if (["button", "submit", "checkbox", "radio", "hidden"].includes(type)) return false;

		// Inputs inside the payment section (like Cash amount) are NOT treated as text typing
		if ($(elem).closest(".payment-container, .payment-modes, .mode-of-payment-control").length) {
			return false;
		}
		return true;
	}
	return false;
}

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
	setTimeout(doBlur, 600);
}

$(document).on("keydown", function (e) {
	// Check if key pressed is Spacebar (key: ' ', keyCode: 32)
	if (e.key === " " || e.keyCode === 32) {
		const activeElem = document.activeElement;

		// Trigger shortcut ONLY if user is NOT typing in search or customer text fields
		if (!isTextInput(activeElem)) {
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
