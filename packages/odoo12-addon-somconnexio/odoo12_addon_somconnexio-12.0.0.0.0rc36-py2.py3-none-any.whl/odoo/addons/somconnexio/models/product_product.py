from odoo import models


class Product(models.Model):
    _inherit = 'product.product'
    _sql_constraints = [
        ('default_code_uniq', 'unique (default_code)',
         'The product code must be unique !'
         ),
    ]
