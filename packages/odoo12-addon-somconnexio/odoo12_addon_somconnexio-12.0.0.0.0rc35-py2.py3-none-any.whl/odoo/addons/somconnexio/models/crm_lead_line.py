from odoo import models, fields, api
from odoo.addons.queue_job.job import job
from odoo.exceptions import ValidationError

from otrs_somconnexio.otrs_models.ticket_factory import TicketFactory

from odoo.addons.somconnexio.otrs_factories.customer_data_from_res_partner \
    import CustomerDataFromResPartner
from odoo.addons.somconnexio.otrs_factories.service_data_from_crm_lead_line \
    import ServiceDataFromCRMLeadLine


class CRMLeadLine(models.Model):
    _inherit = 'crm.lead.line'

    broadband_isp_info = fields.Many2one(
        'broadband.isp.info',
        string='Broadband ISP Info'
    )
    mobile_isp_info = fields.Many2one(
        'mobile.isp.info',
        string='Mobile ISP Info'
    )

    is_mobile = fields.Boolean(
        compute='_get_is_mobile',
    )
    is_adsl = fields.Boolean(
        compute='_get_is_adsl',
    )
    is_fiber = fields.Boolean(
        compute='_get_is_fiber',
    )
    ticket_number = fields.Char(string='Ticket Number')

    @api.depends('product_id')
    def _get_is_mobile(self):
        mobile = self.env.ref('somconnexio.mobile_service')
        for record in self:
            record.is_mobile = (
                mobile.id == record.product_id.product_tmpl_id.categ_id.id
            )

    @api.depends('product_id')
    def _get_is_adsl(self):
        adsl = self.env.ref('somconnexio.broadband_adsl_service')
        for record in self:
            record.is_adsl = (
                adsl.id == record.product_id.product_tmpl_id.categ_id.id
            )

    @api.depends('product_id')
    def _get_is_fiber(self):
        fiber = self.env.ref('somconnexio.broadband_fiber_service')
        for record in self:
            record.is_fiber = (
                fiber.id == record.product_id.product_tmpl_id.categ_id.id
            )

    @api.constrains('is_mobile', 'broadband_isp_info', 'mobile_isp_info')
    def _check_isp_info(self):
        for record in self:
            if record.is_mobile:
                if not record.mobile_isp_info:
                    raise ValidationError(
                        'A mobile lead line needs a Mobile ISP Info instance related.'
                    )
            else:
                if not record.broadband_isp_info:
                    raise ValidationError(
                        'A broadband lead line needs a Broadband '
                        + 'ISP Info instance related.'
                    )

    @job
    def create_ticket(self, id):
        crm_lead_line = self.browse(id)
        ticket = TicketFactory(
            ServiceDataFromCRMLeadLine(crm_lead_line).build(),
            CustomerDataFromResPartner(crm_lead_line.lead_id.partner_id).build()
        ).build()
        ticket.create()
        crm_lead_line.write({'ticket_number': ticket.number})
