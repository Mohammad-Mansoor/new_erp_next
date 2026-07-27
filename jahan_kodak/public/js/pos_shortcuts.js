frappe.provide("jahan_kodak.pos");

$(document).on("keydown", function (e) {
	// Check if key pressed is Spacebar (key: ' ', keyCode: 32)
	if (e.key === " " || e.keyCode === 32) {
		const activeElem = document.activeElement;
		const isTyping =
			activeElem &&
			(activeElem.tagName === "INPUT" ||
				activeElem.tagName === "TEXTAREA" ||
				activeElem.tagName === "SELECT" ||
				activeElem.isContentEditable);

		// Trigger shortcut ONLY if user is NOT writing/typing in an input field
		if (!isTyping) {
			const checkoutBtn = $(".checkout-btn:visible");
			const submitOrderBtn = $(".submit-order-btn:visible");

			if (checkoutBtn.length) {
				e.preventDefault();
				checkoutBtn.click();
			} else if (submitOrderBtn.length) {
				e.preventDefault();
				submitOrderBtn.click();
			}
		}
	}
});

// Remove automatic focus on cash input when Checkout is clicked
$(document).on("click", ".checkout-btn", function () {
	setTimeout(function () {
		if (document.activeElement) {
			document.activeElement.blur();
		}
		$(".mode-of-payment-control input").blur();
	}, 250);
});
