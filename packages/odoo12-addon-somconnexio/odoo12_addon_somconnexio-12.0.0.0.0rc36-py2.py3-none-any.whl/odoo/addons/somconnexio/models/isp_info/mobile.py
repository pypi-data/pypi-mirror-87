from odoo import models, fields, api
from odoo.exceptions import ValidationError


class MobileISPInfo(models.Model):
    _inherit = 'base.isp.info'

    _name = 'mobile.isp.info'
    _description = "Mobile ISP Info"
    icc = fields.Char(string='ICC')
    icc_donor = fields.Char(string='ICC Donor')
    previous_contract_type = fields.Selection([
                                              ('contract', 'Contract'),
                                              ('prepaid', 'Prepaid')],
                                              string='Previous Contract Type')

    @api.one
    @api.constrains('type', 'icc_donor', 'previous_contract_type')
    def _check_mobile_protability_info(self):
        if self.type == 'new':
            return True
        if not self.previous_contract_type:
            raise ValidationError(
                'Previous contract type is required in a portability'
            )
        if not self.icc_donor:
            raise ValidationError(
                'ICC donor is required in a portability'
            )
