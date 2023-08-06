import logging

from werkzeug.exceptions import BadRequest
from odoo.addons.base_rest.http import wrapJsonException
from . import schemas

_logger = logging.getLogger(__name__)


class ContractService:
    _description = """
        Contract creation
    """

    def __init__(self, env=False):
        self.env = env

    @staticmethod
    def validator_create():
        return schemas.S_CONTRACT_CREATE

    @staticmethod
    def validator_return_create():
        return schemas.S_CONTRACT_RETURN_CREATE

    def create(self, **params):
        _logger.info("Create contract received with body: {}".format(params))
        params = self._prepare_create(params)
        cc = self.env["contract.contract"].sudo().create(params)
        return self._to_dict(cc)

    @staticmethod
    def _to_dict(contract):
        return {
            "id": contract.id
        }

    def _prepare_create_line(self, line):
        product = self.env["product.product"].sudo().search(
            [('default_code', '=', line['product_code'])]
        )
        if not product:
            raise wrapJsonException(
                BadRequest(
                    'Product with code %s not found' % (
                        line['product_code'],
                    )
                )
            )
        response_line = {
            "name": product.name,
            "product_id": product.id,
            "date_start": line['date_start']
        }
        return response_line

    def _check_service_combination(self, technology_id, supplier_id):
        if not self.env['service.technology.service.supplier'].sudo().search(
            [
                ('service_technology_id', '=', technology_id),
                ('service_supplier_id', '=', supplier_id)
            ]
        ):
            return False
        else:
            return True

    def _create_mobile_contract_service_info(self, params):
        if not params:
            return False
        return self.env['mobile.service.contract.info'].sudo().create({
            'phone_number': params['phone_number'],
            'icc': params['icc']
        })

    def _create_adsl_contract_service_info(self, params):
        if not params:
            return False
        router_product = self._get_router_product_id(params['router_product_id'])
        router_lot_id = self._create_router_lot_id(
            params['router_serial_number'],
            params['router_mac_address'],
            router_product,
        )
        return self.env['adsl.service.contract.info'].sudo().create({
            'phone_number': params['phone_number'],
            'administrative_number': params['administrative_number'],
            'router_product_id': router_product.id,
            'router_mac_address': params['router_mac_address'],
            'ppp_user': params['ppp_user'],
            'ppp_password': params['ppp_password'],
            'endpoint_user': params['endpoint_user'],
            'endpoint_password': params['endpoint_password'],
            'router_lot_id': router_lot_id.id,
        })

    def _create_vodafone_fiber_contract_service_info(self, params):
        if not params:
            return False
        return self.env['vodafone.fiber.service.contract.info'].sudo().create({
            'phone_number': params['phone_number'],
            'vodafone_id': params['vodafone_id'],
            'vodafone_offer_code': params['vodafone_offer_code']
        })

    def _create_mm_fiber_contract_service_info(self, params):
        if not params:
            return False
        return self.env['mm.fiber.service.contract.info'].sudo().create({
            'phone_number': params['phone_number'],
            'mm_id': params['mm_id'],
        })

    def _prepare_service_partner_id(self, params):
        service_address = params['service_address']
        service_address_obj = self.env['res.partner'].sudo().search([
            ('parent_id', '=', params['partner_id']),
            ('street', '=', service_address['street']),
            ('zip', '=', service_address['zip_code']),
            ('city', '=', service_address['city']),
            ('state_id.code', '=', service_address['state']),
            ('type', '=', 'service'),
        ])
        if not service_address_obj:
            state = self.env['res.country.state'].sudo().search([
                ('country_id', '=', self.env.ref('base.es').id),
                ('code', '=', service_address['state'])
            ])
            service_address_obj = self.env['res.partner'].sudo().create({
                'parent_id': params['partner_id'],
                'street': service_address['street'],
                'zip':  service_address['zip_code'],
                'city': service_address['city'],
                'state_id': state.id,
                'type': 'service',
            })
        return service_address_obj.id

    def _prepare_create(self, params):
        partner_id = int(params['partner_id'])

        if not self.env['res.partner'].sudo().browse(partner_id):
            raise wrapJsonException(
                BadRequest(
                    'Partner id %s not found' % (partner_id, )
                )
            )

        contract_lines = []
        if params.get('contract_line'):
            contract_lines.append(
                self._prepare_create_line(params['contract_line'])
            )
        else:
            contract_lines.extend(
                self._prepare_create_line(line)
                for line in params['contract_lines']
            )
        mobile_contract_service_info = self._create_mobile_contract_service_info(
            params.get('mobile_contract_service_info')
        )
        adsl_contract_service_info = (
            self._create_adsl_contract_service_info(
                params.get('adsl_contract_service_info')
            )
        )
        vodafone_fiber_contract_service_info = (
            self._create_vodafone_fiber_contract_service_info(
                params.get('vodafone_fiber_contract_service_info')
            )
        )
        mm_fiber_contract_service_info = (
            self._create_mm_fiber_contract_service_info(
                params.get('mm_fiber_contract_service_info')
            )
        )
        if mobile_contract_service_info:
            name = mobile_contract_service_info.phone_number
        elif adsl_contract_service_info:
            name = adsl_contract_service_info.phone_number
        elif vodafone_fiber_contract_service_info:
            name = vodafone_fiber_contract_service_info.phone_number
        elif mm_fiber_contract_service_info:
            name = mm_fiber_contract_service_info.phone_number
        if 'service_partner_id' in params:
            service_partner_id = params['service_partner_id']
        elif 'service_address' in params:
            service_partner_id = self._prepare_service_partner_id(params)
        else:
            service_partner_id = False
        response = {
            'name': name,
            'partner_id': partner_id,
            'service_partner_id': service_partner_id,
            'mobile_contract_service_info_id': (
                mobile_contract_service_info and mobile_contract_service_info.id
            ),
            'adsl_service_contract_info_id': (
                adsl_contract_service_info and
                adsl_contract_service_info.id
            ),
            'vodafone_fiber_service_contract_info_id': (
                vodafone_fiber_contract_service_info and
                vodafone_fiber_contract_service_info.id
            ),
            'mm_fiber_service_contract_info_id': (
                mm_fiber_contract_service_info and
                mm_fiber_contract_service_info.id
            ),
            'invoice_partner_id': partner_id,
            'service_technology_id': self._get_service_tech(
                params['service_technology']
            ).id,
            'service_supplier_id': self._get_service_supplier(
                params['service_supplier']
            ).id,
            'bank_id': self.env.get('res.partner.bank').sudo().search(
                [
                    ("partner_id", "=", partner_id),
                    ("acc_number", "=", params['iban']),
                ]
            ).id
        }
        if not self._check_service_combination(
            response['service_technology_id'],
            response['service_supplier_id']
        ):
            raise wrapJsonException(
                BadRequest(
                    'Bad combination {} and {}'.format(
                        params['service_technology'],
                        params['service_supplier']
                    )
                )
            )
        if contract_lines:
            response.update({
                'contract_line_ids': [
                    (0, False, contract_line)
                    for contract_line in contract_lines
                ],
            })
        return response

    def _get_service_tech(self, name):
        service_tech = self.env['service.technology'].sudo().search(
            [('name', '=', name)]
        )
        if service_tech:
            return service_tech
        else:
            raise wrapJsonException(
                BadRequest('No service technology for name %s' % name)
            )

    def _get_service_supplier(self, name):
        service_supplier = self.env['service.supplier'].sudo().search(
            [('name', '=', name)]
        )
        if service_supplier:
            return service_supplier
        else:
            raise wrapJsonException(
                BadRequest('No service supplier for name %s' % name)
            )

    def _get_router_product_id(self, product_id):
        router_product = self.env['product.product'].sudo().search(
            [
                ('id', '=', product_id),
                ('categ_id', '=', self.env.ref('somconnexio.router_category').id),
                ('tracking', '=', 'serial')
            ]
        )
        if router_product:
            return router_product
        else:
            raise wrapJsonException(
                BadRequest('No router product id for %d' % product_id)
            )

    def _create_router_lot_id(self, serial_number, mac_address, product):
        return self.env['stock.production.lot'].sudo().create({
            'product_id': product.id,
            'router_mac_address': mac_address,
            'name': serial_number,
        })
