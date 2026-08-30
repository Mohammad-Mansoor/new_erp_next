/**
 * Single SPACE Key POS Cashier Workflow
 * Jahan Kodak Customization
 * 
 * This script intercepts the Spacebar key to provide an extremely fast, 
 * single-key checkout flow for cashiers, while preserving 100% of ERPNext's
 * native validations, payment rendering, and printing mechanisms.
 */

frappe.provide("erpnext.PointOfSale");

// Internal lock to prevent duplicate submissions from rapid key presses
window.__pos_single_key_lock = false;

/**
 * Safely triggers the ERPNext submit button and securely tracks the lifecycle
 * of the submission (including server delays) to unlock the workflow only when finished.
 */
function trigger_submit_with_lifecycle_lock() {
    let savesubmit_called = false;
    let unfreeze_hooked = false;
    let confirm_restored = false;
    
    const original_savesubmit = cur_pos.frm.savesubmit;
    const original_unfreeze = frappe.dom.unfreeze;
    const original_confirm = frappe.confirm;

    const restore_confirm = () => {
        if (!confirm_restored) {
            frappe.confirm = original_confirm;
            confirm_restored = true;
        }
    };

    const restore_unfreeze = () => {
        if (unfreeze_hooked) {
            frappe.dom.unfreeze = original_unfreeze;
            unfreeze_hooked = false;
        }
    };

    // 1. Intercept the confirmation dialog securely
    frappe.confirm = function(message, confirm_action, reject_action) {
        if (message && message.includes("Permanently Submit") && cur_pos && cur_pos.frm && message.includes(cur_pos.frm.docname)) {
            restore_confirm();
            if (confirm_action) confirm_action();
            return;
        }
        restore_confirm();
        original_confirm.apply(this, arguments);
    };

    // 2. Intercept savesubmit to know if validation passed and submission started
    cur_pos.frm.savesubmit = function() {
        savesubmit_called = true;
        
        // Hook unfreeze just for this submission to know exactly when the server response completes
        unfreeze_hooked = true;
        frappe.dom.unfreeze = function() {
            restore_unfreeze();
            window.__pos_single_key_lock = false; // RELEASE LOCK ON COMPLETION/ERROR
            return original_unfreeze.apply(this, arguments);
        };

        return original_savesubmit.apply(this, arguments);
    };

    try {
        // Re-trigger the exact ERPNext submit button which holds the validation logic.
        cur_pos.payment.$component.find(".submit-order-btn").click();
    } finally {
        cur_pos.frm.savesubmit = original_savesubmit;
        restore_confirm();
        
        // If validation failed, savesubmit never ran, so unfreeze was never hooked.
        // We must release the lock immediately because Frappe halted.
        if (!savesubmit_called) {
            window.__pos_single_key_lock = false; // RELEASE LOCK ON VALIDATION FAIL
        }
    }
}

// Attach a global event listener in the CAPTURE phase to intercept SPACE 
// before it is consumed by input fields (especially the natively focused payment input).
window.addEventListener("keydown", function(e) {
    // Only care about Space. Also ignore held-down repeat keys to prevent duplicate fires.
    if (e.code !== "Space" || e.repeat) {
        return;
    }

    // 1. EDITABLE INPUT PROTECTION (With Empty Exemption)
    const activeNode = document.activeElement ? document.activeElement.nodeName.toLowerCase() : "";
    if (activeNode === 'input' || activeNode === 'textarea') {
        const val = (document.activeElement.value || "").toString();
        if (val.length > 0) {
            return; // The input has text, allow native typing of space
        }
        // If the input is empty, we ignore the input and treat Space as the shortcut!
    }

    // 2. EXCHANGE OVERLAY PRIORITY
    const $exchange = $('.pos-exchange-overlay:visible');
    if ($exchange.length > 0) {
        e.preventDefault();
        e.stopPropagation();
        
        // A. SUCCESS STATE: Close button exists
        const $close_btn = $exchange.find('.btn-close-success');
        if ($close_btn.length > 0 && $close_btn.is(':visible')) {
            $close_btn.click();
            return;
        }

        // B. EDITABLE STATE: Submit button exists
        const $submit_btn = $exchange.find('#btn-submit-exchange');
        if ($submit_btn.length > 0 && $submit_btn.is(':visible')) {
            if (!$submit_btn.prop('disabled')) {
                $submit_btn.click();
            }
            return;
        }
        
        // C. SUBMITTING STATE: Button is disabled
        // Do nothing, lock is held naturally by button state.
        
        return; // Terminate early so normal POS doesn't fire
    }

    // 3. NORMAL MODAL PROTECTION
    // If any blocking modal is open, let Space act normally. DO NOT submit underlying POS.
    if ($('.modal:visible').length > 0) {
        return;
    }

    // Ensure we are inside the POS page and the controller is actually initialized
    if (typeof cur_pos === 'undefined' || !cur_pos || !cur_pos.frm || !cur_pos.wrapper.is(':visible')) {
        return;
    }

    // ==========================================
    // STATE MACHINE
    // ==========================================
    
    // ------------------------------------------
    // STATE: COMPLETED / ORDER SUMMARY
    // ------------------------------------------
    if (cur_pos.order_summary && cur_pos.order_summary.$component.is(':visible')) {
        e.preventDefault();
        e.stopPropagation();
        
        if (!window.__pos_single_key_lock) {
            window.__pos_single_key_lock = true;
            // Trigger New Order via the native button which clears the DOM safely
            cur_pos.order_summary.$summary_container.find('.new-btn').click();
            
            // Release lock after a short delay since new order transitions the DOM immediately
            setTimeout(() => { window.__pos_single_key_lock = false; }, 500);
        }
        return;
    }

    // ------------------------------------------
    // STATE: PAYMENT_READY
    // ------------------------------------------
    // If we are already on the payment screen (e.g., cashier manually intervened to enter exact change)
    if (cur_pos.payment && cur_pos.payment.$component.is(':visible')) {
        e.preventDefault();
        e.stopPropagation();
        
        if (!window.__pos_single_key_lock) {
            window.__pos_single_key_lock = true;
            trigger_submit_with_lifecycle_lock();
        }
        return;
    }

    // ------------------------------------------
    // STATE: IDLE_CART / CHECKOUT_IN_PROGRESS
    // ------------------------------------------
    if (cur_pos.cart && cur_pos.cart.$component.is(':visible')) {
        
        // EDGE CASE 1: Search Field
        // If the search field is currently focused, allow typing a space UNLESS it is empty.
        // This ensures they can type "Apple Juice", but can still hit Space to checkout if empty.
        const search_input = cur_pos.item_selector && cur_pos.item_selector.search_field ? cur_pos.item_selector.search_field.$input.get(0) : null;
        if (document.activeElement === search_input) {
            if (search_input && search_input.value.length > 0) {
                // Allow the user to type the space character natively
                return;
            }
        }

        // Consume the space key for checkout workflow
        e.preventDefault();
        e.stopPropagation();

        if (window.__pos_single_key_lock) return;

        // EDGE CASE 2: Empty Cart
        const items = cur_pos.frm.doc.items;
        if (!items || items.length === 0) {
            frappe.show_alert({ message: __("You cannot checkout an empty order."), indicator: "orange" });
            return;
        }

        window.__pos_single_key_lock = true;

        // Trigger ERPNext Checkout logic natively.
        // save_and_checkout() saves the invoice asynchronously and then renders the payment screen.
        cur_pos.save_and_checkout().then(() => {
            
            // Wait for the payment component to actually become visible in the DOM
            let fallback_timer;
            const check_payment_ready = setInterval(() => {
                if (cur_pos.payment && cur_pos.payment.$component.is(':visible')) {
                    clearInterval(check_payment_ready);
                    clearTimeout(fallback_timer);
                    
                    // Allow the UI a small frame to settle and focus_on_default_mop() to populate Cash
                    requestAnimationFrame(() => {
                        trigger_submit_with_lifecycle_lock();
                    });
                }
            }, 50); // poll every 50ms safely

            // Fallback unlock if payment screen never shows (e.g. unexpected error preventing render)
            fallback_timer = setTimeout(() => { 
                clearInterval(check_payment_ready);
                window.__pos_single_key_lock = false; 
            }, 5000);

        }).catch(() => {
            window.__pos_single_key_lock = false;
        });

        return;
    }
}, true); // Use capture phase to beat Mousetrap and Input handlers
