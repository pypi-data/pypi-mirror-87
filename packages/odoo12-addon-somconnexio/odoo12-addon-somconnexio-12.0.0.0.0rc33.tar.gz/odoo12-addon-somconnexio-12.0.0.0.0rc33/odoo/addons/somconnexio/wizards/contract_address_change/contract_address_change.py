from otrs_somconnexio.otrs_models.coverage.adsl import ADSLCoverage
from otrs_somconnexio.otrs_models.coverage.mm_fibre import MMFibreCoverage
from otrs_somconnexio.otrs_models.coverage.vdf_fibre import VdfFibreCoverage

from odoo import api, fields, models


class ContractAddressChangeWizard(models.TransientModel):
    _name = 'contract.address.change.wizard'
    partner_id = fields.Many2one('res.partner')

    partner_bank_id = fields.Many2one(
        'res.partner.bank',
        string='Partner Bank',
        required=True
    )
    service_street = fields.Char(
        string='Service Street',
        required=True
    )
    service_street2 = fields.Char(string='Service Street 2')
    service_zip_code = fields.Char(
        string='Service ZIP',
        required=True
    )
    service_city = fields.Char(
        string='Service City',
        required=True
    )
    service_state_id = fields.Many2one(
        'res.country.state',
        string='Service State',
        required=True
    )
    service_country_id = fields.Many2one(
        'res.country',
        string='Service Country',
        required=True
    )
    service_supplier_id = fields.Many2one(
        'service.supplier',
        'Service Supplier',
        required=True,
    )
    previous_product_id = fields.Many2one(
        'product.product',
        'Previous Product',
        required=True,
    )
    product_id = fields.Many2one(
        'product.product',
        'Product',
        required=True,
    )
    mm_fiber_coverage = fields.Selection(
        MMFibreCoverage.VALUES,
        'MM Fiber Coverage',
    )
    vdf_fiber_coverage = fields.Selection(
        VdfFibreCoverage.VALUES,
        'Vdf Fiber Coverage',
    )
    adsl_coverage = fields.Selection(
        ADSLCoverage.VALUES,
        'ADSL Coverage',
    )

    @api.model
    def default_get(self, fields_list):
        defaults = super().default_get(fields_list)
        defaults['partner_id'] = self.env.context['active_id']
        return defaults

    @api.multi
    def button_change(self):
        self.ensure_one()
        broadband_isp_info = self.env["broadband.isp.info"].create(
            {
                "service_street": self.service_street,
                "service_street2": self.service_street2,
                "service_zip_code": self.service_zip_code,
                "service_city": self.service_city,
                "service_state_id": self.service_state_id.id,
                "service_country_id": self.service_country_id.id,
                "type": "new",
                "service_supplier_id": self.service_supplier_id.id,
                "change_address": True,
                "mm_fiber_coverage": self.mm_fiber_coverage,
                "vdf_fiber_coverage": self.vdf_fiber_coverage,
                "adsl_coverage": self.adsl_coverage,
            }
        )
        line_params = {
            "name": self.product_id.name,
            "product_id": self.product_id.id,
            "product_tmpl_id": self.product_id.product_tmpl_id.id,
            "category_id": self.product_id.categ_id.id,
            "broadband_isp_info": broadband_isp_info.id
        }
        crm_line_ids = [
            self.env["crm.lead.line"].create(line_params).id
        ]
        crm_lead = self.env['crm.lead'].create({
            "name": "Change Address process",
            "partner_id": self.partner_id.id,
            "iban": self.partner_bank_id.sanitized_acc_number,
            "lead_line_ids": [(6, 0, crm_line_ids)]
        })
        action = self.env["ir.actions.act_window"].for_xml_id(
            "crm",
            "crm_lead_all_leads")
        action.update({
            "view_mode": "form",
            "views": False,
            "res_id": crm_lead.id,
        })
        return action
