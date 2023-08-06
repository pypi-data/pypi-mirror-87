from odoo import models, fields


class DiscoveryChannel(models.Model):
    _name = 'discovery.channel'
    description = fields.Char('Description')
