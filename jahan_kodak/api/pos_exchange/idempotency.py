import frappe
from frappe import _
import hashlib
import json

def generate_payload_hash(payload):
    """
    Generates a deterministic hash of the critical transaction components
    to prevent reusing an idempotency key with modified data.
    """
    clean_payload = {
        "original_invoice": payload.get("original_invoice"),
        "return_items": payload.get("return_items", []),
        "new_items": payload.get("new_items", []),
        "payments": payload.get("payments", [])
    }
    payload_str = json.dumps(clean_payload, sort_keys=True)
    return hashlib.sha256(payload_str.encode('utf-8')).hexdigest()

def check_idempotency(payload):
    """
    Checks if an exchange with this idempotency key already exists.
    Returns the POS Exchange name if it exists AND the payload matches.
    Throws an error if the key exists but payload is different.
    """
    idempotency_key = payload.get("idempotency_key")
    if not idempotency_key:
        return None
        
    existing_exchange = frappe.db.get_value(
        "POS Exchange", 
        {"idempotency_key": idempotency_key, "docstatus": 1}, 
        ["name", "payload_hash"],
        as_dict=True
    )
    
    if existing_exchange:
        current_hash = generate_payload_hash(payload)
        if existing_exchange.payload_hash and existing_exchange.payload_hash != current_hash:
            frappe.throw(_("Idempotency conflict: A previous request was completed with this key but different transaction data."))
        return existing_exchange.name
        
    return None
