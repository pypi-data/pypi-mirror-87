from odoo import models, fields, api
from odoo.exceptions import ValidationError


class BaseISPInfo(models.AbstractModel):
    _name = 'base.isp.info'
    phone_number = fields.Char(string='Phone Number')

    delivery_full_street = fields.Char(
        compute='_get_delivery_full_street',
        store=True
    )

    delivery_street = fields.Char(string='Delivery Street')
    delivery_street2 = fields.Char(string='Delivery Street 2')
    delivery_zip_code = fields.Char(string='Delivery ZIP')
    delivery_city = fields.Char(string='Delivery City')
    delivery_state_id = fields.Many2one(
        'res.country.state',
        string='Delivery State')
    delivery_country_id = fields.Many2one(
        'res.country',
        string='Delivery Country')

    type = fields.Selection([('portability', 'Portability'), ('new', 'New')],
                            default='new',
                            string='Type')
    previous_provider = fields.Many2one('previous.provider',
                                        string='Previous Provider')
    previous_owner_vat_number = fields.Char(string='Previous Owner VatNumber')
    previous_owner_first_name = fields.Char(string='Previous Owner First Name')
    previous_owner_name = fields.Char(string='Previous Owner Name')

    def name_get(self):
        res = []
        for item in self:
            if item.type == 'new':
                res.append((item.id, 'New'))
            else:
                res.append((item.id, item.phone_number))
        return res

    @api.depends('delivery_street', 'delivery_street2')
    def _get_delivery_full_street(self):
        for record in self:
            if record.delivery_street2:
                record.delivery_full_street = "{} {}".format(
                    record.delivery_street,
                    record.delivery_street2)
            else:
                record.delivery_full_street = record.delivery_street

    @api.one
    @api.constrains(
        'type', 'previous_provider', 'previous_owner_vat_number',
        'previous_owner_name', 'previous_owner_first_name', 'phone_number')
    def _check_protability_info(self):
        if self.type == 'new':
            return True
        if not self.previous_provider:
            raise ValidationError(
                'Previous provider is required in a portability'
            )
        if not self.phone_number:
            raise ValidationError(
                'Phone number is required in a portability'
            )
        if (not self.previous_owner_vat_number or not self.previous_owner_first_name or
                not self.previous_owner_name):
            raise ValidationError(
                'Previous owner info is required in a portability'
            )
