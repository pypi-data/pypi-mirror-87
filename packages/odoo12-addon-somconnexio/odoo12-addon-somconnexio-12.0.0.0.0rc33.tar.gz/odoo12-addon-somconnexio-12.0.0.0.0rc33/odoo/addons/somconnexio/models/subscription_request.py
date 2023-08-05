from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError
import logging
_logger = logging.getLogger(__name__)
try:
    from stdnum.es.nie import is_valid as valid_nie
except (ImportError, IOError) as err:
    _logger.debug(err)


class SubscriptionRequest(models.Model):
    _inherit = 'subscription.request'

    iban = fields.Char(required=True)

    type = fields.Selection(
        selection_add=[(
            'sponsorship_coop_agreement',
            'Sponsorship Coop Agreement'
        )])

    coop_agreement_id = fields.Many2one(
        'coop.agreement',
        string='Coop Agreement'
    )
    nationality = fields.Many2one('res.country', 'Nationality')

    payment_type = fields.Selection([
        ('single', 'One single payment'),
        ('split', 'Ten payments')
    ])

    state_id = fields.Many2one('res.country.state', 'Province')

    def get_journal(self):
        # Redefine the get_journal of EMC to get the SUBJ journal:
        # https://github.com/coopiteasy/vertical-cooperative/blob/12.0/easy_my_coop/models/coop.py#L522  # noqa
        return self.env.ref('somconnexio.subscription_journal')

    def get_partner_company_vals(self):
        values = super().get_partner_company_vals()
        values['coop_agreement_id'] = self.coop_agreement_id and \
            self.coop_agreement_id.id
        values["vat"] = self.vat
        values["state_id"] = self.state_id.id
        return values

    def get_partner_vals(self):
        values = super().get_partner_vals()
        values['coop_agreement_id'] = self.coop_agreement_id and \
            self.coop_agreement_id.id
        values["vat"] = self.vat
        values["nationality"] = self.nationality.id
        values["state_id"] = self.state_id.id
        return values

    @api.one
    def vinculate_partner_in_lead(self):
        leads = self.env['crm.lead'].search([
            ('subscription_request_id', '=', self.id)
        ])
        for lead in leads:
            lead.partner_id = self.partner_id

    @api.one
    def validate_subscription_request(self):
        try:
            invoice = super().validate_subscription_request()
        except UserError:
            if self.ordered_parts == 0 and self.type == 'sponsorship_coop_agreement':
                pass
            else:
                raise
        else:
            self.vinculate_partner_in_lead()
            return invoice

        self.partner_obj = self.env['res.partner']

        self._check_already_cooperator()

        if not self.partner:
            self.partner = self.create_coop_partner()
        else:
            self.partner = self.partner[0]

        self.partner_id = self.partner
        self.partner.nationality = self.nationality
        self.partner.state_id = self.state_id

        self.partner.cooperator = True

        self._create_company_contact()

        self.write({'state': 'done'})
        self.vinculate_partner_in_lead()
        return True

    @api.one
    @api.constrains('coop_agreement_id', 'type')
    def _check_coop_agreement_id(self):
        if self.type == 'sponsorship_coop_agreement' and not self.coop_agreement_id:
            raise ValidationError(
                "If it's a Coop Agreement sponsorship the Coop Agreement must be set."
            )

    @api.one
    @api.constrains('vat', 'nationality')
    def _check_nie_nationality(self):
        if valid_nie(self.vat) and not self.nationality:
            raise ValidationError('If a NIE is provided, nationality is mandatory.')
