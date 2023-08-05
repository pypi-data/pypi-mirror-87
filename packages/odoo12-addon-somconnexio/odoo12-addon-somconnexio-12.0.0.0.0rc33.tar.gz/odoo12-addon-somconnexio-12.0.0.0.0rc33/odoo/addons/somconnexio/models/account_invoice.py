from odoo import models, fields, api
import json


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'
    oc_number = fields.Char()
    oc_taxes = fields.Char()
    oc_total = fields.Float()
    oc_untaxed = fields.Float()
    oc_total_taxed = fields.Float()

    @api.one
    @api.depends('invoice_line_ids.price_subtotal', 'tax_line_ids.amount',
                 'tax_line_ids.amount_rounding',
                 'currency_id', 'company_id', 'date_invoice', 'type', 'date')
    def _compute_amount(self):
        round_curr = self.currency_id.round
        if self.oc_untaxed:
            self.amount_untaxed = self.oc_untaxed
        else:
            self.amount_untaxed = sum(
                line.price_subtotal for line in self.invoice_line_ids
            )
        if self.oc_total_taxed:
            self.amount_tax = self.oc_total_taxed
        else:
            self.amount_tax = sum(
                round_curr(line.amount_total) for line in self.tax_line_ids
            )
        if self.oc_total:
            self.amount_total = self.oc_total
        else:
            self.amount_total = self.amount_untaxed + self.amount_tax
        amount_total_company_signed = self.amount_total
        amount_untaxed_signed = self.amount_untaxed
        if (
            self.currency_id and self.company_id and
            self.currency_id != self.company_id.currency_id
        ):
            currency_id = self.currency_id
            rate_date = self._get_currency_rate_date() or fields.Date.today()
            amount_total_company_signed = currency_id._convert(
                self.amount_total, self.company_id.currency_id,
                self.company_id, rate_date
            )
            amount_untaxed_signed = currency_id._convert(
                self.amount_untaxed, self.company_id.currency_id,
                self.company_id, rate_date
            )
        sign = self.type in ['in_refund', 'out_refund'] and -1 or 1
        self.amount_total_company_signed = amount_total_company_signed * sign
        self.amount_total_signed = self.amount_total * sign
        self.amount_untaxed_signed = amount_untaxed_signed * sign

    @api.multi
    def compute_taxes(self):
        for invoice in self:
            oc_invoice = any([
                line.oc_amount_total
                for line in invoice.invoice_line_ids
            ])
            if not oc_invoice:
                super().compute_taxes()
                continue
            oc_taxes_parsed = json.loads(self.oc_taxes)
            for oc_tax in oc_taxes_parsed:
                taxes_amount = oc_tax['amountTax']
                base = oc_tax['amountWithoutTax']
                tax = self.env['account.tax'].search([
                    ('oc_code', '=', oc_tax['taxCode'])
                ])
                vals = {
                    'invoice_id': invoice.id,
                    'name': tax.name,
                    'tax_id': tax.id,
                    'amount': taxes_amount,
                    'base': base,
                    'manual': False,
                    'account_id': tax.account_id.id
                }
                self.env['account.invoice.tax'].create(vals)


class AccountInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'
    oc_amount_untaxed = fields.Float()
    oc_amount_total = fields.Float()
    oc_amount_taxes = fields.Float()
    price_unit = fields.Float(required=False)
    quantity = fields.Float(required=False)

    @api.one
    @api.depends('price_unit', 'discount', 'invoice_line_tax_ids', 'quantity',
                 'product_id', 'invoice_id.partner_id', 'invoice_id.currency_id',
                 'invoice_id.company_id', 'invoice_id.date_invoice', 'invoice_id.date')
    def _compute_price(self):
        currency = self.invoice_id and self.invoice_id.currency_id or None
        price = self.price_unit * (1 - (self.discount or 0.0) / 100.0)
        taxes = False
        if self.invoice_line_tax_ids:
            taxes = self.invoice_line_tax_ids.compute_all(
                price, currency, self.quantity,
                product=self.product_id, partner=self.invoice_id.partner_id
            )
        if self.oc_amount_untaxed:
            self.price_subtotal = price_subtotal_signed = self.oc_amount_untaxed
        else:
            self.price_subtotal = price_subtotal_signed = (
                taxes['total_excluded'] if taxes else self.quantity * price
            )
        if self.oc_amount_total:
            self.price_total = self.oc_amount_total
        else:
            self.price_total = taxes['total_included'] if taxes else self.price_subtotal
        if (
            self.invoice_id.currency_id and
            self.invoice_id.currency_id != self.invoice_id.company_id.currency_id
        ):
            currency = self.invoice_id.currency_id
            date = self.invoice_id._get_currency_rate_date()
            price_subtotal_signed = currency._convert(
                price_subtotal_signed, self.invoice_id.company_id.currency_id,
                self.company_id or self.env.user.company_id, date or fields.Date.today()
            )
        sign = self.invoice_id.type in ['in_refund', 'out_refund'] and -1 or 1
        self.price_subtotal_signed = price_subtotal_signed * sign

    def _get_price_tax(self):
        for line in self:
            line.price_tax = (
                line.oc_amount_taxes
                if line.oc_amount_taxes
                else line.price_total - line.price_subtotal
            )
