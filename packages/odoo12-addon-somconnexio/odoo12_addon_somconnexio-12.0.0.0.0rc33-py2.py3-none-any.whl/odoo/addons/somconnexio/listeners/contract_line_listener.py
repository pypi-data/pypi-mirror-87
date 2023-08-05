from odoo.addons.component.core import Component


class ContractLineListener(Component):
    _name = 'contract.line.listener'
    _inherit = 'base.event.listener'
    _apply_on = ['contract.line']

    def on_record_create(self, record, fields=None):

        one_shot_products_categ_id_list = [
            self.env.ref('somconnexio.mobile_oneshot_service').id,
            self.env.ref('somconnexio.broadband_oneshot_service').id,
        ]

        if record.product_id.categ_id.id in one_shot_products_categ_id_list:
            self.env['contract.contract'].with_delay().add_one_shot_contract_line(
                record.id, record.product_id)
