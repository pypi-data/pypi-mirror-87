import logging
from odoo.addons.component.core import Component
from . import schemas
from werkzeug.exceptions import BadRequest
from odoo.addons.base_rest.http import wrapJsonException


_logger = logging.getLogger(__name__)


class SubscriptionRequestService(Component):
    _inherit = "subscription.request.services"

    def _prepare_create(self, params):
        params["ordered_parts"] = 1
        if params["type"] == "new":
            params["share_product"] = self.env.ref(
                "somconnexio.cooperator_share_product").id
        sr_create_values = super()._prepare_create(params)
        sr_create_values["iban"] = params["iban"]
        sr_create_values["vat"] = params["vat"]
        sr_create_values["voluntary_contribution"] = params.get(
            "voluntary_contribution", False
        )
        payment_type = params["payment_type"]
        if payment_type not in [
            pm[0]
            for pm
            in self.env['subscription.request']._fields['payment_type'].selection
        ]:
            raise wrapJsonException(
                BadRequest(
                    'Payment method %s not valid' % (params['payment_type'],)
                )
            )
        sr_create_values["payment_type"] = params["payment_type"]
        if "coop_agreement" in params:
            coop_agreement_id = self.env['coop.agreement'].search([
                ('code', '=', params['coop_agreement'])
            ]).id
            if not coop_agreement_id:
                raise wrapJsonException(
                    BadRequest(
                        'Coop Agreement %s not found' % (params['coop_agreement'],)
                    )
                )
            sr_create_values['coop_agreement_id'] = coop_agreement_id
        if "nationality" in params:
            nationality_id = self.env['res.country'].search([
                ('code', '=', params['nationality'])
            ]).id
            if not nationality_id:
                raise wrapJsonException(
                    BadRequest(
                        'Nationality %s not found' % (params['nationality'],)
                    )
                )
            sr_create_values['nationality'] = nationality_id
        if "state" in params['address']:
            country = self.env['res.country'].browse(
                sr_create_values['country_id']
            )
            state_id = self.env['res.country.state'].search([
                ('code', '=', params['address']['state']),
                ('country_id', '=', country.id),
            ]).id
            if not state_id:
                raise wrapJsonException(
                    BadRequest(
                        'State %s not found' % (params['address']['state'],)
                    )
                )
            sr_create_values['state_id'] = state_id
        return sr_create_values

    def _validator_create(self):
        create_schema = super()._validator_create()
        create_schema.update(schemas.S_SUBSCRIPTION_REQUEST_CREATE_SC_FIELDS)
        return create_schema
