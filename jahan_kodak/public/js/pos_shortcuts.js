frappe.provide("jahan_kodak.pos");

document.addEventListener("keydown", function (e) {
	// Check if key pressed is Spacebar (key: ' ', keyCode: 32)
	if (e.key === " " || e.keyCode === 32) {
		const checkoutBtn = $(".checkout-btn:visible");
		const submitOrderBtn = $(".submit-order-btn:visible");

		// 1. Payment View: Pressing Space submits & completes order
		if (submitOrderBtn.length) {
			e.preventDefault();
			e.stopPropagation();
			submitOrderBtn.click();
			return;
		}

		// 2. Cart View: Pressing Space triggers Checkout if not typing text
		if (checkoutBtn.length) {
			const activeElem = document.activeElement;
			let isActivelyTyping = false;

			if (activeElem && (activeElem.tagName === "INPUT" || activeElem.tagName === "TEXTAREA")) {
				// If the input has text typed by user, allow typing space
				if (activeElem.value && activeElem.value.trim().length > 0) {
					isActivelyTyping = true;
				}
			}

			// If search box is empty or no text is being typed, proceed to Checkout
			if (!isActivelyTyping) {
				e.preventDefault();
				e.stopPropagation();
				checkoutBtn.click();
			}
		}
	}
}, true); // Event capture phase

// Remove automatic focus on cash input when Checkout is clicked
$(document).on("click", ".checkout-btn", function () {
	const blurInputs = function () {
		if (document.activeElement) {
			document.activeElement.blur();
		}
		$(".mode-of-payment-control input, .payment-modes input, .fields-numpad-container input").blur();
	};

	setTimeout(blurInputs, 100);
	setTimeout(blurInputs, 350);
});
