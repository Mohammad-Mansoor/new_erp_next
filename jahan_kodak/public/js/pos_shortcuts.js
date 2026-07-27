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

function isTextInput(elem) {
	if (!elem) return false;
	const tag = elem.tagName;
	if (tag === "TEXTAREA" || elem.isContentEditable) return true;
	if (tag === "INPUT") {
		const type = (elem.type || "text").toLowerCase();
		if (["button", "submit", "checkbox", "radio", "hidden"].includes(type)) return false;
		if ($(elem).closest(".payment-container, .payment-modes, .mode-of-payment-control").length) {
			return false;
		}
		return true;
	}
	return false;
}

$(document).on("keydown", function (e) {
	const isSpaceKey = e.key === " " || e.keyCode === 32;
	
	// Alt + Space: ALWAYS triggers globally (no matter where cursor is)
	// Standalone Space: triggers when not typing in text search box
	const isAltSpace = e.altKey && isSpaceKey;
	const isStandaloneSpace = isSpaceKey && !e.altKey && !e.ctrlKey && !e.shiftKey && !isTextInput(document.activeElement);

	if (isAltSpace || isStandaloneSpace) {
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
});

// Remove automatic focus on cash input when Checkout button is clicked
$(document).on("click", ".checkout-btn", function () {
	removePaymentFocus();
});
