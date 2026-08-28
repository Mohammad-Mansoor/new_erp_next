import frappe

class POSExchangeError(frappe.ValidationError):
    pass

class OriginalInvoiceNotFoundError(POSExchangeError):
    pass

class InvalidInvoiceStateError(POSExchangeError):
    pass

class InvalidReturnQuantityError(POSExchangeError):
    pass

class ItemNotReturnableError(POSExchangeError):
    pass

class IdempotencyConflictError(POSExchangeError):
    pass

class ConcurrencyConflictError(POSExchangeError):
    pass

class PaymentMismatchError(POSExchangeError):
    pass
