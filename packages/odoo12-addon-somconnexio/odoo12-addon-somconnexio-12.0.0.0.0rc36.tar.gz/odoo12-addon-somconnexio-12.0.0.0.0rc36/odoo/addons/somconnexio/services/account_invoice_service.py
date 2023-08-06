import logging
from odoo.addons.component.core import Component
from . import schemas
from werkzeug.exceptions import BadRequest
from odoo.addons.base_rest.http import wrapJsonException
import json

_logger = logging.getLogger(__name__)


class AccountInvoiceService(Component):
    _inherit = "account.invoice.service"

    def create(self, **params):
        params = self._prepare_create(params)
        # tracking_disable=True in context is needed
        # to avoid to send a mail in Account Invoice creation
        invoice = self.env["account.invoice"].with_context(
            tracking_disable=True
        ).create(params)
        return self._to_dict(invoice)

    def _validator_create(self):
        return schemas.S_ACCOUNT_INVOICE_CREATE

    def _validator_return_create(self):
        return schemas.S_ACCOUNT_INVOICE_RETURN_CREATE

    def _prepare_create_line(self, line):
        account = self.env['account.account'].search(
            [('code', '=', line['accountingCode'])]
        )
        if not account:
            raise wrapJsonException(
                BadRequest(
                    'Account code %s not found' % (
                        line['accountingCode']
                    )
                )
            )
        tax = self.env['account.tax'].search(
            [('oc_code', '=', line['taxCode'])]
        )
        if not tax:
            raise wrapJsonException(
                BadRequest(
                    'Tax code %s not found' % (
                        line['taxCode']
                    )
                )
            )
        product_id = self.env['product.product'].search(
            [('default_code', '=', line['invoiceSubCategoryCode'])]
        ).id
        if not product_id:
            raise wrapJsonException(
                BadRequest(
                    'Product with code %s not found' % (
                        line['invoiceSubCategoryCode'],)
                )
            )
        response_line = {
            'name': line['description'],
            'account_id': account.id,
            'oc_amount_taxes': line['amountTax'],
            'oc_amount_untaxed': line['amountWithoutTax'],
            'oc_amount_total': line['amountWithTax'],
            "invoice_line_tax_ids": [(4, tax.id, 0)],
            "product_id": product_id
        }
        return response_line

    def _prepare_create(self, params):
        account_code = params['invoice']['billingAccountCode']
        partner_id = int(account_code[0:account_code.index("_")])
        if not self.env['res.partner'].search(
            [('id', '=', partner_id)]
        ):
            raise wrapJsonException(
                BadRequest(
                    'Partner with id %s not found' % (
                        partner_id,)
                )
            )
        invoice_lines = [
            line
            for category in params['invoice']['categoryInvoiceAgregate']
            for line in category['subCategoryInvoiceAgregateDto']
        ]
        lines = [
            self.env['account.invoice.line'].create(
                self._prepare_create_line(line)
            ).id
            for line in invoice_lines
            if 'amountWithoutTax' in line and line['amountWithoutTax']
        ]
        oc_taxes_parsed = params['invoice']['taxAggregate']
        for oc_tax in oc_taxes_parsed:
            tax = self.env['account.tax'].search([
                ('oc_code', '=', oc_tax['taxCode'])
            ])
            if not tax:
                raise wrapJsonException(
                    BadRequest(
                        'Tax code %s in Tax Aggregate not found' % (
                            oc_tax['taxCode'],)
                    )
                )

        oc_taxes = json.dumps(params['invoice']['taxAggregate'])
        return {
            "partner_id": partner_id,
            "oc_number": params['invoice']['invoiceNumber'],
            "date_invoice": params['invoice']['recordedInvoiceDto']['invoiceDate'],
            "oc_untaxed": params['invoice']['amountWithoutTax'],
            "oc_total": params['invoice']['amountWithTax'],
            "oc_total_taxed": params['invoice']['amountTax'],
            "invoice_line_ids": [(6, 0, lines)],
            "oc_taxes": oc_taxes
        }

    @staticmethod
    def _to_dict(account_invoice):
        return {
            "id": account_invoice.id
        }
