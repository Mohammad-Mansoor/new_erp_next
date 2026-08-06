import frappe


POS_RECEIPT_HTML = r"""
{# ---------------------------------------------------------
   Calculate a safe initial page height.

   JavaScript below will measure the exact rendered height
   before printing. This Jinja calculation is the fallback
   for PDF engines that do not execute JavaScript.
---------------------------------------------------------- #}

{% set calculation = namespace(items_height=0) %}

{% set item_count = doc.items | length %}
{% set tax_count = doc.taxes | length if doc.taxes else 0 %}
{% set payment_count = doc.payments | length if doc.payments else 0 %}

{% for item in doc.items %}
    {% set item_label = item.item_name or item.item_code or '' %}
    {% set name_length = item_label | length %}

    {#
       Approximately 22 characters fit on one item-name line.
       Longer names receive additional page height.
    #}
    {% set wrapped_lines = ((name_length + 21) // 22) %}

    {% if wrapped_lines < 1 %}
        {% set wrapped_lines = 1 %}
    {% endif %}

    {#
       5mm for rate/padding
       4.5mm for every wrapped item-name line
    #}
    {% set calculation.items_height =
        calculation.items_height + 5 + (wrapped_lines * 4.5)
    %}
{% endfor %}

{#
   135mm includes:
   - Header
   - Invoice information
   - Table heading
   - Totals
   - Payments
   - Thank-you message
   - QR code
   - Cutter safety space
#}
{% set estimated_page_height =
    135
    + calculation.items_height
    + (tax_count * 5)
    + (payment_count * 5)
%}

{% if estimated_page_height < 150 %}
    {% set estimated_page_height = 150 %}
{% endif %}


<div class="pos-receipt" id="pos-receipt">

    <!-- =====================================================
         HEADER
    ====================================================== -->

    <div class="receipt-header">
        <div class="company-name">
            {{ doc.company }}




















            
        </div>

        <div class="receipt-title">
            SALES RECEIPT
        </div>

        <div class="receipt-meta">
            <div>
                Invoice:
                <strong>{{ doc.name }}</strong>
            </div>

            <div>
                Date:

                {% if doc.posting_date and doc.posting_time %}
                    {{ frappe.utils.format_datetime(
                        doc.posting_date ~ ' ' ~ doc.posting_time,
                        "dd-MM-yyyy hh:mm a"
                    ) }}
                {% else %}
                    {{ frappe.utils.formatdate(doc.posting_date) }}
                {% endif %}
            </div>
        </div>
    </div>


    <div class="divider divider-dashed"></div>


    <!-- =====================================================
         ITEMS
    ====================================================== -->

    <table class="items-table">

        <thead>
            <tr>
                <th class="text-left item-column">
                    Item
                </th>

                <th class="text-center qty-column">
                    Qty
                </th>

                <th class="text-right amount-column">
                    Amount
                </th>
            </tr>
        </thead>

        <tbody>
            {% for item in doc.items %}
                <tr class="item-row">

                    <td class="text-left">
                        <div class="item-name">
                            {{ item.item_name or item.item_code }}
                        </div>

                        {% if item.item_code and item.item_name != item.item_code %}
                            <div class="item-code">
                                {{ item.item_code }}
                            </div>
                        {% endif %}

                        <div class="item-rate">
                            @
                            {{ frappe.utils.fmt_money(
                                item.rate,
                                currency=doc.currency
                            ) }}
                        </div>
                    </td>

                    <td class="text-center value-cell">
                        {% if item.qty == item.qty | int %}
                            {{ item.qty | int }}
                        {% else %}
                            {{ item.qty }}
                        {% endif %}
                    </td>

                    <td class="text-right value-cell">
                        {{ frappe.utils.fmt_money(
                            item.amount,
                            currency=doc.currency
                        ) }}
                    </td>

                </tr>
            {% endfor %}
        </tbody>

    </table>


    <div class="divider divider-dashed"></div>


    <!-- =====================================================
         TOTALS
    ====================================================== -->

    <div class="totals-wrapper">

        <div class="total-row">
            <span>Subtotal</span>
            <span>{{ doc.get_formatted("net_total") }}</span>
        </div>


        {% if doc.discount_amount %}
            <div class="total-row">
                <span>Discount</span>

                <span>
                    - {{ doc.get_formatted("discount_amount") }}
                </span>
            </div>
        {% endif %}


        {% if doc.taxes %}
            {% for tax in doc.taxes %}
                {% if tax.tax_amount %}
                    <div class="total-row">
                        <span>
                            {{ tax.description or "Tax" }}
                        </span>

                        <span>
                            {{ tax.get_formatted("tax_amount") }}
                        </span>
                    </div>
                {% endif %}
            {% endfor %}
        {% endif %}


        <div class="divider divider-solid"></div>


        <div class="total-row grand-total-row">
            <span>TOTAL</span>
            <span>{{ doc.get_formatted("grand_total") }}</span>
        </div>


        <div class="divider divider-solid"></div>


        <!-- ================================================
             PAYMENTS
        ================================================= -->

        {% if doc.payments %}
            {% for payment in doc.payments %}
                {% if payment.amount %}
                    <div class="total-row payment-row">
                        <span>
                            {{ payment.mode_of_payment }}
                        </span>

                        <span>
                            {{ payment.get_formatted("amount") }}
                        </span>
                    </div>
                {% endif %}
            {% endfor %}
        {% endif %}


        {% if doc.change_amount %}
            <div class="total-row">
                <span>Change</span>

                <span>
                    {{ doc.get_formatted("change_amount") }}
                </span>
            </div>
        {% endif %}

    </div>


    <div class="divider divider-dashed"></div>


    <!-- =====================================================
         FOOTER
    ====================================================== -->

    <div class="receipt-footer">

        <div class="footer-message">
            Thank you for shopping with us!
        </div>

        <div class="powered-by">
            Jahan Kodak
        </div>

        <img
            id="receipt-qr-code"
            class="qr-code"
            src="https://quickchart.io/qr?text={{ doc.name }}&size=200&margin=1&format=png"
            width="96"
            height="96"
            alt="Receipt QR Code"
        >


        # <div class="cutter-space">------------------------------------------</div>
        # <div class="cutter-space">------------------------------------------</div>
        # <div class="cutter-space">------------------------------------------</div>

    </div>

</div>


{# Initial page height generated by Jinja #}
<style id="receipt-page-size">
    @page {
        size:
            80mm
            {{ estimated_page_height | round(0, "ceil") | int }}mm;
        margin: 0;
    }
</style>


<style>

    /* =====================================================
       GLOBAL PRINT RESET
    ====================================================== */

    html,
    body {
        width: 80mm !important;
        min-width: 80mm !important;
        max-width: 80mm !important;

        height: auto !important;
        min-height: 0 !important;

        margin: 0 !important;
        padding: 0 !important;

        overflow: visible !important;

        background: #ffffff !important;
        color: #000000 !important;

        font-family:
            "Courier New",
            Courier,
            monospace !important;

        font-size: 12px !important;
        line-height: 1.25 !important;
    }


    /*
     * Override Frappe's normal A4 print container.
     */
    .print-format-gutter,
    .print-format {
        width: 80mm !important;
        min-width: 80mm !important;
        max-width: 80mm !important;

        height: auto !important;
        min-height: 0 !important;

        margin: 0 !important;
        padding: 0 !important;

        overflow: visible !important;

        background: #ffffff !important;
        box-shadow: none !important;
    }


    /* =====================================================
       RECEIPT CONTAINER
    ====================================================== */

    .pos-receipt {
        display: block !important;

        /*
         * Most 80mm printers have approximately
         * 72mm printable width.
         */
        width: 72mm !important;

        height: auto !important;
        min-height: 0 !important;

        margin: 0 auto !important;
        padding: 3mm 1mm 4mm 1mm !important;

        box-sizing: border-box !important;
        overflow: visible !important;

        page-break-before: avoid !important;
        page-break-after: avoid !important;
        page-break-inside: avoid !important;

        break-before: avoid-page !important;
        break-after: avoid-page !important;
        break-inside: avoid-page !important;
    }


    /* =====================================================
       HEADER
    ====================================================== */

    .receipt-header {
        display: block;
        width: 100%;
        text-align: center;
    }


    .company-name {
        margin: 0 0 2px 0 !important;
        padding: 0 !important;

        font-size: 17px !important;
        line-height: 1.15 !important;
        font-weight: 800 !important;

        text-transform: uppercase;
        letter-spacing: 0.3px;

        overflow-wrap: anywhere;
        word-break: break-word;
    }


    .receipt-title {
        margin: 0 !important;
        padding: 0 !important;

        font-size: 12px !important;
        line-height: 1.15 !important;
        font-weight: 700 !important;

        text-decoration: underline;
    }


    .receipt-meta {
        margin-top: 4px;

        font-size: 10.5px;
        line-height: 1.25;

        text-align: center;
    }


    /* =====================================================
       DIVIDERS
    ====================================================== */

    .divider {
        display: block;

        width: 100%;
        height: 0;

        box-sizing: border-box;
    }


    .divider-dashed {
        margin: 6px 0;
        border-top: 1px dashed #000000;
    }


    .divider-solid {
        margin: 5px 0;
        border-top: 1.5px solid #000000;
    }


    /* =====================================================
       ITEMS TABLE
    ====================================================== */

    .items-table {
        width: 100% !important;
        max-width: 100% !important;

        margin: 0 !important;
        padding: 0 !important;

        border: 0 !important;
        border-spacing: 0 !important;
        border-collapse: collapse !important;

        table-layout: fixed !important;
    }


    .items-table thead {
        display: table-header-group;
    }


    .items-table tbody {
        display: table-row-group;
    }


    .items-table tr {
        page-break-inside: avoid !important;
        break-inside: avoid-page !important;
    }


    .items-table th {
        margin: 0 !important;
        padding: 0 0 3px 0 !important;

        border: 0 !important;
        border-bottom: 1px solid #000000 !important;

        font-size: 10.5px !important;
        line-height: 1.2 !important;
        font-weight: 700 !important;
    }


    .items-table td {
        margin: 0 !important;
        padding: 4px 0 !important;

        border: 0 !important;

        vertical-align: top !important;

        font-size: 10.5px !important;
        line-height: 1.2 !important;

        overflow-wrap: anywhere !important;
        word-wrap: break-word !important;
        word-break: break-word !important;
    }


    .item-column {
        width: 52%;
    }


    .qty-column {
        width: 13%;
    }


    .amount-column {
        width: 35%;
    }


    .item-name {
        display: block;

        font-weight: 700;

        white-space: normal !important;
        overflow-wrap: anywhere !important;
        word-break: break-word !important;
    }


    .item-code {
        display: block;

        margin-top: 1px;

        font-size: 9px;
        line-height: 1.15;
    }


    .item-rate {
        display: block;

        margin-top: 1px;

        font-size: 9.5px;
        line-height: 1.15;
    }


    .value-cell {
        vertical-align: middle !important;
        white-space: nowrap !important;
    }


    /* =====================================================
       ALIGNMENT
    ====================================================== */

    .text-left {
        text-align: left !important;
    }


    .text-center {
        text-align: center !important;
    }


    .text-right {
        text-align: right !important;
    }


    /* =====================================================
       TOTALS
    ====================================================== */

    .totals-wrapper {
        display: block !important;
        width: 100% !important;

        margin: 0 !important;
        padding: 0 !important;
    }


    .total-row {
        display: flex !important;

        width: 100% !important;

        justify-content: space-between !important;
        align-items: baseline !important;

        gap: 6px !important;

        margin: 0 0 3px 0 !important;
        padding: 0 !important;

        font-size: 10.5px !important;
        line-height: 1.2 !important;

        page-break-inside: avoid !important;
        break-inside: avoid-page !important;
    }


    .total-row span:first-child {
        min-width: 0;
        overflow-wrap: anywhere;
    }


    .total-row span:last-child {
        flex-shrink: 0;

        text-align: right;
        white-space: nowrap;
    }


    .grand-total-row {
        margin: 0 !important;
        padding: 1px 0 !important;

        font-size: 14px !important;
        line-height: 1.2 !important;
        font-weight: 800 !important;
    }


    /* =====================================================
       FOOTER AND QR
    ====================================================== */

    .receipt-footer {
        display: block !important;

        width: 100% !important;

        margin: 6px 0 0 0 !important;
        padding: 0 !important;

        text-align: center !important;

        page-break-inside: avoid !important;
        break-inside: avoid-page !important;
    }


    .footer-message {
        font-size: 11px;
        line-height: 1.2;
        font-weight: 700;
    }


    .powered-by {
        margin-top: 2px;
        margin-bottom: 4px;

        font-size: 9px;
        line-height: 1.2;
    }


    .qr-code {
        display: block !important;

        width: 24mm !important;
        height: 24mm !important;

        min-width: 24mm !important;
        min-height: 24mm !important;

        max-width: 24mm !important;
        max-height: 24mm !important;

        margin: 3px auto 0 auto !important;
        padding: 0 !important;

        border: 0 !important;

        object-fit: contain !important;

        page-break-before: avoid !important;
        page-break-after: avoid !important;
        page-break-inside: avoid !important;

        break-before: avoid-page !important;
        break-after: avoid-page !important;
        break-inside: avoid-page !important;
    }


    /*
     * Small space for the printer cutter.
     * Do not use 100px or 100mm here.
     */
    .cutter-space {
        display: block;
        width: 100%;
        height: 4mm;
        # padding-bottom: 40px;
        # margin-bottom: 100px
    }


    /* =====================================================
       PRINT MODE
    ====================================================== */

    @media print {

        html,
        body,
        .print-format-gutter,
        .print-format {
            width: 80mm !important;
            min-width: 80mm !important;
            max-width: 80mm !important;

            height: auto !important;
            min-height: 0 !important;

            margin: 0 !important;
            padding: 0 !important;

            overflow: visible !important;
        }


        .pos-receipt {
            page-break-before: avoid !important;
            page-break-after: avoid !important;
            page-break-inside: avoid !important;

            break-before: avoid-page !important;
            break-after: avoid-page !important;
            break-inside: avoid-page !important;
        }


        .items-table tr,
        .total-row,
        .receipt-footer,
        .qr-code {
            page-break-inside: avoid !important;
            break-inside: avoid-page !important;
        }
    }

</style>


<script>
(function () {
    "use strict";

    function setExactReceiptPageHeight() {
        var receipt = document.getElementById("pos-receipt");
        var pageStyle = document.getElementById("receipt-page-size");

        if (!receipt || !pageStyle) {
            return;
        }

        /*
         * Browsers normally calculate CSS pixels at 96 DPI.
         *
         * Convert the actual receipt height from pixels to mm
         * and add 4mm for the thermal-printer cutter.
         */
        var receiptHeightPixels = Math.ceil(
            Math.max(
                receipt.scrollHeight,
                receipt.offsetHeight,
                receipt.getBoundingClientRect().height
            )
        );

        var receiptHeightMillimetres = Math.ceil(
            (receiptHeightPixels * 25.4 / 96) + 4
        );

        /*
         * Minimum height for a very small receipt.
         */
        if (receiptHeightMillimetres < 150) {
            receiptHeightMillimetres = 150;
        }

        pageStyle.textContent =
            "@page {" +
                "size: 80mm " + receiptHeightMillimetres + "mm;" +
                "margin: 0;" +
            "}";
    }


    /*
     * Measure the receipt during all important print stages.
     */
    document.addEventListener(
        "DOMContentLoaded",
        setExactReceiptPageHeight
    );

    window.addEventListener(
        "load",
        setExactReceiptPageHeight
    );

    window.addEventListener(
        "beforeprint",
        setExactReceiptPageHeight
    );


    /*
     * The QR image may finish loading after the HTML.
     */
    var qrCode = document.getElementById("receipt-qr-code");

    if (qrCode) {
        qrCode.addEventListener(
            "load",
            setExactReceiptPageHeight
        );

        qrCode.addEventListener(
            "error",
            setExactReceiptPageHeight
        );
    }


    /*
     * Additional measurements for slower browsers.
     */
    setTimeout(setExactReceiptPageHeight, 100);
    setTimeout(setExactReceiptPageHeight, 300);
    setTimeout(setExactReceiptPageHeight, 700);

})();
</script>
"""


def create_or_update_print_format(doctype: str) -> None:
    print_format_name = f"Modern POS Receipt - {doctype}"

    existing_name = frappe.db.exists(
        "Print Format",
        print_format_name,
    )

    if existing_name:
        print_format = frappe.get_doc(
            "Print Format",
            existing_name,
        )

        print_format.doc_type = doctype
        print_format.module = "Accounts"
        print_format.custom_format = 1
        print_format.print_format_type = "Jinja"
        print_format.raw_printing = 0
        print_format.html = POS_RECEIPT_HTML
        print_format.disabled = 0

        print_format.save(ignore_permissions=True)

    else:
        print_format = frappe.get_doc(
            {
                "doctype": "Print Format",
                "name": print_format_name,
                "doc_type": doctype,
                "module": "Accounts",
                "custom_format": 1,
                "print_format_type": "Jinja",
                "raw_printing": 0,
                "disabled": 0,
                "html": POS_RECEIPT_HTML,
            }
        )

        print_format.insert(ignore_permissions=True)


def setup() -> None:
    doctypes = [
        "POS Invoice",
        "Sales Invoice",
    ]

    for doctype in doctypes:
        create_or_update_print_format(doctype)

    frappe.db.commit()

    print(
        "Modern POS Receipt print formats "
        "created or updated successfully."
    )