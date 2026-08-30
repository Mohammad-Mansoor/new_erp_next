import frappe

POS_RECEIPT_HTML = """<div class="pos-receipt">
    <!-- Header -->
    <div class="receipt-header">
        <h2 class="company-name" dir="rtl" style="font-family: Tahoma, Arial, sans-serif;">جهان کودک</h2>
        {% if letter_head %}
            <div class="letterhead-wrapper">{{ letter_head }}</div>
        {% endif %}
        <div class="receipt-title">SALES RECEIPT</div>
        <div class="meta-row" style="text-align: center;">
            <img src="https://quickchart.io/barcode?type=code128&text={{ doc.name }}&height=20&width=120" alt="Barcode" style="margin: 4px auto; display: block;">
            <span>Date: {{ frappe.utils.format_datetime(doc.posting_date ~ ' ' ~ doc.posting_time, "dd-MM-yyyy hh:mm a") if doc.posting_date and doc.posting_time else frappe.utils.formatdate(doc.posting_date) }}</span>
        </div>
    </div>

    <div class="divider-dashed"></div>

    <!-- Items Table -->
    <table class="items-table" dir="rtl">
        <thead>
            <tr>
                <th class="text-right" style="width: 50%; font-family: Tahoma, Arial, sans-serif;">کالا (Item)</th>
                <th class="text-center" style="width: 15%; font-family: Tahoma, Arial, sans-serif;">تعداد (Qty)</th>
                <th class="text-left" style="width: 35%; font-family: Tahoma, Arial, sans-serif;">مبلغ (Amount)</th>
            </tr>
        </thead>
        <tbody>
            {% for item in doc.items %}
            <tr>
                <td class="text-right">
                    <div class="item-name">{{ item.item_name }}</div>
                    <div class="item-meta">@ {{ frappe.utils.fmt_money(item.rate, currency=doc.currency) }}</div>
                </td>
                <td class="text-center val-align">{{ item.qty | int if item.qty == item.qty | int else item.qty }}</td>
                <td class="text-left val-align">{{ frappe.utils.fmt_money(item.amount, currency=doc.currency) }}</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>

    <div class="divider-dashed"></div>

    <!-- Totals Section -->
    <div class="totals-wrapper">
        <div class="total-row">
            <span>Subtotal</span>
            <span>{{ doc.get_formatted('net_total') }}</span>
        </div>
        
        {% if doc.discount_amount %}
        <div class="total-row discount-row">
            <span>Discount</span>
            <span>- {{ doc.get_formatted('discount_amount') }}</span>
        </div>
        {% endif %}

        {% for tax in doc.taxes %}
        {% if tax.tax_amount %}
        <div class="total-row">
            <span>{{ tax.description or 'Tax' }}</span>
            <span>{{ frappe.utils.fmt_money(tax.tax_amount, currency=doc.currency) }}</span>
        </div>
        {% endif %}
        {% endfor %}

        <div class="divider-solid"></div>

        <div class="total-row grand-total-row">
            <span>TOTAL</span>
            <span>{{ doc.get_formatted('grand_total') }}</span>
        </div>

        <div class="divider-solid"></div>

        <!-- Payments Section -->
        {% if doc.payments %}
            {% for p in doc.payments %}
                {% if p.amount %}
                <div class="total-row payment-row">
                    <span>{{ p.mode_of_payment }}</span>
                    <span>{{ frappe.utils.fmt_money(p.amount, currency=doc.currency) }}</span>
                </div>
                {% endif %}
            {% endfor %}
        {% endif %}

        {% if doc.change_amount %}
        <div class="total-row change-row">
            <span>Change</span>
            <span>{{ doc.get_formatted('change_amount') }}</span>
        </div>
        {% endif %}
    </div>

    <div class="divider-dashed"></div>

    <!-- Footer QR & Thank You -->
    <div class="receipt-footer">
        <div class="footer-msg" dir="rtl" style="font-family: Tahoma, Arial, sans-serif; font-size: 10px;">در منزل سوم صرف لباس وكفش قابل تعويض ويا مسترد كردن ميباشدا</div>
    </div>
</div>

<style>
    @page {
        size: 78mm auto;
        margin: 0;
    }
    body, html {
        margin: 0;
        padding: 0;
        background: #ffffff !important;
        color: #000000 !important;
        font-family: 'Courier New', Courier, monospace, Arial, sans-serif;
        font-size: 12px;
        line-height: 1.3;
    }
    .pos-receipt {
        width: 76mm;
        margin: 0 auto;
        padding: 4mm 2mm;
        box-sizing: border-box;
    }
    .receipt-header {
        text-align: center;
    }
    .company-name {
        font-size: 16px;
        font-weight: 800;
        margin: 0 0 4px 0;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .receipt-title {
        font-size: 12px;
        font-weight: 700;
        margin-top: 4px;
        text-decoration: underline;
    }
    .meta-row {
        margin-top: 6px;
        font-size: 11px;
        display: flex;
        flex-direction: column;
        gap: 2px;
    }
    .divider-dashed {
        border-top: 1px dashed #000000;
        margin: 8px 0;
    }
    .divider-solid {
        border-top: 1.5px solid #000000;
        margin: 6px 0;
    }
    .items-table {
        width: 100%;
        border-collapse: collapse;
    }
    .items-table th {
        font-size: 11px;
        font-weight: 700;
        border-bottom: 1px solid #000000;
        padding-bottom: 3px;
    }
    .items-table td {
        padding: 4px 0;
        vertical-align: top;
        font-size: 11px;
    }
    .item-name {
        font-weight: 600;
        word-break: break-word;
    }
    .item-meta {
        font-size: 10px;
        color: #333333;
    }
    .text-left { text-align: left; }
    .text-center { text-align: center; }
    .text-right { text-align: right; }
    .val-align { vertical-align: middle; }
    
    .totals-wrapper {
        display: flex;
        flex-direction: column;
        gap: 3px;
    }
    .total-row {
        display: flex;
        justify-content: space-between;
        font-size: 11px;
    }
    .grand-total-row {
        font-size: 14px;
        font-weight: 800;
        padding: 2px 0;
    }
    .receipt-footer {
        text-align: center;
        margin-top: 8px;
    }
    .qr-code {
        width: 28mm;
        height: 28mm;
        display: block;
        margin: 0 auto 6px auto;
    }
    .footer-msg {
        font-size: 11px;
        font-weight: 700;
    }
    .powered-by {
        font-size: 9px;
        margin-top: 2px;
        color: #555555;
    }
</style>
"""

def update():
    pf_name = "POS Invoice"
    if frappe.db.exists("Print Format", pf_name):
        frappe.db.set_value("Print Format", pf_name, {
            "custom_format": 1,
            "print_format_type": "Jinja",
            "html": POS_RECEIPT_HTML
        })
    else:
        doc = frappe.get_doc({
            "doctype": "Print Format",
            "name": pf_name,
            "doc_type": "POS Invoice",
            "module": "Stock",
            "custom_format": 1,
            "print_format_type": "Jinja",
            "html": POS_RECEIPT_HTML
        })
        doc.insert(ignore_permissions=True)
    
    pos_profiles = frappe.get_all("POS Profile", fields=["name"])
    for p in pos_profiles:
        frappe.db.set_value("POS Profile", p.name, "print_format", "POS Invoice")

    frappe.db.commit()
    print("Standard POS Invoice Print Format updated in DB successfully!")
