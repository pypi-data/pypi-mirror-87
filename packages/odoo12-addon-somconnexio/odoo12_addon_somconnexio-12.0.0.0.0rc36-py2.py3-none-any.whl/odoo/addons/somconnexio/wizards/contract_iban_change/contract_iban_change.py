from odoo import api, fields, models


class ContractIbanChangeWizard(models.TransientModel):
    _name = 'contract.iban.change.wizard'
    partner_id = fields.Many2one('res.partner')
    contract_ids = fields.Many2many('contract.contract', string='Contracts')
    res_partner_bank_id = fields.Many2one(
        'res.partner.bank', 'IBAN',
    )

    @api.model
    def default_get(self, fields_list):
        defaults = super().default_get(fields_list)
        defaults['partner_id'] = self.env.context['active_id']
        return defaults

    @api.multi
    def button_change(self):
        self.ensure_one()
        self.contract_ids.write({'bank_id': self.res_partner_bank_id.id})
        return True
