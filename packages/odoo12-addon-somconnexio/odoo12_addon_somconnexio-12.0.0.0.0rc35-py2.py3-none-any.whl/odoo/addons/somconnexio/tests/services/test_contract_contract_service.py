import json
import odoo
from faker import Faker
from odoo.addons.easy_my_coop_api.tests.common import BaseEMCRestCase
from datetime import date, timedelta
from mock import patch
HOST = "127.0.0.1"
PORT = odoo.tools.config["http_port"]


class BaseEMCRestCaseAdmin(BaseEMCRestCase):
    @classmethod
    def setUpClass(cls, *args, **kwargs):
        # Skip parent class in super to avoid recreating api key
        super(BaseEMCRestCase, cls).setUpClass(*args, **kwargs)
        cls.AuthApiKey = cls.env["auth.api.key"]
        admin = cls.env.ref("base.user_admin")
        cls.api_key_test = cls.AuthApiKey.create(
            {"name": "test-key", "key": "api-key", "user_id": admin.id}
        )


@patch('odoo.addons.somconnexio.models.contract.CRMAccountHierarchyFromContractService')
class TestContractController(BaseEMCRestCaseAdmin):

    def setUp(self):
        super().setUp()
        self.router_product = self.env['product.product'].create({
            'name': 'Router',
            'categ_id': self.ref('somconnexio.router_category'),
            'tracking': 'serial'
        })
        partner = self.browse_ref('base.partner_demo')
        self.partner_id = str(partner.id)
        self.iban = partner.bank_ids[0].acc_number
        fake = Faker('es-ES')
        self.service_address = {
            'street': fake.street_address() + " " + fake.secondary_address(),
            'zip_code': fake.postcode(),
            'city': fake.city(),
            'state': self.browse_ref('base.state_es_m').code,
            'country': self.browse_ref('base.es').code,
        }

    def http_public_post(self, url, data, headers=None):
        if url.startswith("/"):
            url = "http://{}:{}{}".format(HOST, PORT, url)
        return self.session.post(url, json=data)

    def test_route_right_create(self, _):
        url = "/public-api/contract"
        data = {
            "partner_id": self.partner_id,
            "service_technology": 'Mobile',
            "service_supplier": "MásMóvil",
            "mobile_contract_service_info": {
                "phone_number": "654321123",
                "icc": "123456",
            },
            "contract_lines": [],
            "iban": self.iban
        }
        response = self.http_public_post(url, data=data)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.reason, "OK")
        content = json.loads(response.content.decode("utf-8"))
        self.assertIn('id', content)
        contract = self.env['contract.contract'].browse(content['id'])
        self.assertEquals(
            contract.name,
            data['mobile_contract_service_info']['phone_number']
        )
        self.assertEquals(
            contract.partner_id,
            self.browse_ref('base.partner_demo')
        )
        self.assertEquals(
            contract.invoice_partner_id,
            self.browse_ref('base.partner_demo')
        )
        self.assertEquals(
            contract.service_technology_id,
            self.browse_ref('somconnexio.service_technology_mobile')
        )
        self.assertEquals(
            contract.service_supplier_id,
            self.browse_ref('somconnexio.service_supplier_masmovil')
        )
        self.assertTrue(
            contract.mobile_contract_service_info_id
        )
        self.assertEquals(
            contract.mobile_contract_service_info_id.icc,
            data['mobile_contract_service_info']['icc']
        )
        self.assertEquals(
            contract.mobile_contract_service_info_id.phone_number,
            data['mobile_contract_service_info']['phone_number']
        )

    @odoo.tools.mute_logger("odoo.addons.base_rest.http")
    def test_route_bad_partner_create(self, _):
        url = "/public-api/contract"
        data = {
            "partner_id": "666",
            "service_technology": 'Mobile',
            "service_supplier": "Másmóvil",
            "mobile_contract_service_info": {
                "phone_number": "654321123",
                "icc": "123456",
            },
            "contract_lines": [],
            "iban": "IBAN"
        }
        response = self.http_public_post(url, data=data)
        self.assertEquals(response.status_code, 400)

    @odoo.tools.mute_logger("odoo.addons.base_rest.http")
    def test_route_bad_tech_create(self, _):
        url = "/public-api/contract"
        data = {
            "partner_id": self.partner_id,
            "service_technology": 'XXXX',
            "service_supplier": "Másmóvil",
            "mobile_contract_service_info": {
                "phone_number": "654321123",
                "icc": "123456",
            },
            "contract_lines": [],
            "iban": self.iban
        }
        response = self.http_public_post(url, data=data)
        self.assertEquals(response.status_code, 400)

    @odoo.tools.mute_logger("odoo.addons.base_rest.http")
    def test_route_bad_supplier_create(self, _):
        url = "/public-api/contract"
        data = {
            "partner_id": self.partner_id,
            "service_technology": 'Mobile',
            "service_supplier": "XXXX",
            "mobile_contract_service_info": {
                "phone_number": "654321123",
                "icc": "123456",
            },
            "contract_lines": [],
            "iban": self.iban
        }
        response = self.http_public_post(url, data=data)
        self.assertEquals(response.status_code, 400)

    @odoo.tools.mute_logger("odoo.addons.base_rest.http")
    def test_route_bad_combination_create(self, _):
        url = "/public-api/contract"
        data = {
            "partner_id": self.partner_id,
            "service_technology": 'Fiber',
            "service_supplier": "Másmóvil",
            "mobile_contract_service_info": {
                "phone_number": "654321123",
                "icc": "123456",
            },
            "contract_lines": [],
            "iban": self.iban
        }
        response = self.http_public_post(url, data=data)
        self.assertEquals(response.status_code, 400)

    def test_route_right_contract_lines(self, _):
        url = "/public-api/contract"
        data = {
            "partner_id": self.partner_id,
            "service_technology": 'Mobile',
            "service_supplier": "MásMóvil",
            "mobile_contract_service_info": {
                "phone_number": "654321123",
                "icc": "123456",
            },
            "contract_lines": [
                {
                    "product_code": (
                        self.browse_ref('somconnexio.150Min1GB').default_code
                    ),
                    "date_start": "2020-01-01 00:00:00"
                },
                {
                    "product_code": (
                        self.browse_ref('somconnexio.EnviamentSIM').default_code
                    ),
                    "date_start": "2020-01-01 00:00:00"
                }
            ],
            "iban": self.iban
        }
        response = self.http_public_post(url, data=data)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.reason,
                          "OK"
                          )
        content = json.loads(response.content.decode("utf-8"))
        self.assertIn('id', content)
        contract = self.env['contract.contract'].browse(content['id'])
        self.assertEquals(
            contract.name,
            data['mobile_contract_service_info']['phone_number']
        )
        self.assertEquals(
            contract.partner_id,
            self.browse_ref('base.partner_demo')
        )
        self.assertEquals(
            contract.invoice_partner_id,
            self.browse_ref('base.partner_demo')
        )
        self.assertEquals(
            contract.service_technology_id,
            self.browse_ref('somconnexio.service_technology_mobile')
        )
        self.assertEquals(
            contract.service_supplier_id,
            self.browse_ref('somconnexio.service_supplier_masmovil')
        )
        self.assertIn(
            self.browse_ref('somconnexio.150Min1GB'), [
                c.product_id
                for c in contract.contract_line_ids
            ]
        )
        self.assertIn(
            self.browse_ref('somconnexio.EnviamentSIM'), [
                c.product_id
                for c in contract.contract_line_ids
            ]
        )
        self.assertEquals(
            contract.current_tariff_contract_line.product_id,
            self.env.ref('somconnexio.150Min1GB')
        )
        self.assertEquals(
            [date(2020, 1, 1), date(2020, 1, 1)],
            contract.contract_line_ids.mapped('date_start'),
        )

        contract.contract_line_ids[0].date_start = date(2020, 1, 2)
        self.assertEquals(contract.date_start, date(2020, 1, 1))

    def test_route_right_contract_line(self, _):
        url = "/public-api/contract"
        data = {
            "partner_id": self.partner_id,
            "service_technology": 'Mobile',
            "service_supplier": "MásMóvil",
            "mobile_contract_service_info": {
                "phone_number": "654321123",
                "icc": "123456",
            },
            "contract_line": {
                "product_code": (
                    self.browse_ref('somconnexio.150Min1GB').default_code
                    ),
                "date_start": "2020-01-01 00:00:00"
                },
            "iban": self.iban
        }
        response = self.http_public_post(url, data=data)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.reason, "OK")
        content = json.loads(response.content.decode("utf-8"))
        self.assertIn('id', content)
        contract = self.env['contract.contract'].browse(content['id'])
        self.assertIn(
            self.browse_ref('somconnexio.150Min1GB'), [
                c.product_id
                for c in contract.contract_line_ids
            ]
        )
        self.assertEquals(
            [date(2020, 1, 1)],
            contract.contract_line_ids.mapped('date_start'),
        )

    def test_route_contract_without_active_tariff(self, _):
        url = "/public-api/contract"
        tomorrow = date.today() + timedelta(days=1)
        data = {
            "partner_id": self.partner_id,
            "service_technology": 'Mobile',
            "service_supplier": "MásMóvil",
            "mobile_contract_service_info": {
                "phone_number": "654321123",
                "icc": "123456",
            },
            "contract_lines": [
                {
                    "product_code": (
                        self.browse_ref('somconnexio.150Min1GB').default_code
                    ),
                    "date_start": tomorrow.strftime("%Y-%m-%d %H:%M:%S"),
                },
                {
                    "product_code": (
                        self.browse_ref('somconnexio.EnviamentSIM').default_code
                    ),
                    "date_start": "2020-01-01 00:00:00"
                }
            ],
            "iban": self.iban
        }
        response = self.http_public_post(url, data=data)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.reason, "OK")
        content = json.loads(response.content.decode("utf-8"))
        contract = self.env['contract.contract'].browse(content['id'])
        self.assertFalse(contract.current_tariff_contract_line)

    @odoo.tools.mute_logger("odoo.addons.base_rest.http")
    def test_route_bad_call_both_contract_lines(self, _):
        url = "/public-api/contract"
        data = {
            "partner_id": self.partner_id,
            "service_technology": 'Mobile',
            "service_supplier": "MásMóvil",
            "mobile_contract_service_info": {
                "phone_number": "654321123",
                "icc": "123456",
            },
            "contract_line": {
                "product_code": (
                    self.browse_ref('somconnexio.150Min1GB').default_code
                    ),
                "date_start": "2020-01-01 00:00:00"
                },
            "contract_lines": [],
            "iban": self.iban
        }
        response = self.http_public_post(url, data=data)
        self.assertEquals(response.status_code, 400)

    @odoo.tools.mute_logger("odoo.addons.base_rest.http")
    def test_route_bad_date_start(self, _):
        url = "/public-api/contract"
        data = {
            "partner_id": self.partner_id,
            "service_technology": 'Mobile',
            "service_supplier": "Másmóvil",
            "mobile_contract_service_info": {
                "phone_number": "654321123",
                "icc": "123456",
            },
            "contract_lines": [
                {
                    "product_code": (
                        self.browse_ref('somconnexio.150Min1GB').default_code
                    ),
                    "date_start": "6666-66-66 66:66:66"
                }
            ],
            "iban": self.iban
        }
        response = self.http_public_post(url, data=data)
        self.assertEquals(response.status_code, 400)

    @odoo.tools.mute_logger("odoo.addons.base_rest.http")
    def test_route_bad_product_id(self, _):
        url = "/public-api/contract"
        data = {
            "partner_id": self.partner_id,
            "service_technology": 'Mobile',
            "service_supplier": "Másmóvil",
            "mobile_contract_service_info": {
                "phone_number": "654321123",
                "icc": "123456",
            },
            "contract_lines": [
                {
                    "product_code": (
                        self.browse_ref('somconnexio.150Min1GB').default_code
                    ),
                    "date_start": "2020-01-01 00:00:00"
                },
                {
                    "product_code": "SC_0",
                    "date_start": "2020-01-01 00:00:00"
                }
            ],
            "iban": self.iban
        }
        response = self.http_public_post(url, data=data)
        self.assertEquals(response.status_code, 400)

    @odoo.tools.mute_logger("odoo.addons.base_rest.http")
    def test_route_bad_format_product(self, _):
        url = "/public-api/contract"
        data = {
            "partner_id": self.partner_id,
            "service_technology": 'Mobile',
            "service_supplier": "Másmóvil",
            "mobile_contract_service_info": {
                "phone_number": "654321123",
                "icc": "123456",
            },
            "contract_lines": [
                {
                    "product_code": (
                        self.browse_ref('somconnexio.150Min1GB').default_code
                    ),
                    "date_start": "2020-01-01 00:00:00"
                },
                {
                    "product_code": 666,
                    "date_start": "2020-01-01 00:00:00"
                }
            ],
            "iban": self.iban
        }
        response = self.http_public_post(url, data=data)
        self.assertEquals(response.status_code, 400)

    @odoo.tools.mute_logger("odoo.addons.base_rest.http")
    def test_route_mobile_missing_icc(self, _):
        url = "/public-api/contract"
        data = {
            "partner_id": self.partner_id,
            "service_technology": 'Mobile',
            "service_supplier": "Másmóvil",
            "mobile_contract_service_info": {
                "phone_number": "654321123",
            },
            "contract_lines": [],
            "iban": self.iban
        }
        response = self.http_public_post(url, data=data)
        self.assertEquals(response.status_code, 400)

    @odoo.tools.mute_logger("odoo.addons.base_rest.http")
    def test_route_mobile_missing_phone_number(self, _):
        url = "/public-api/contract"
        data = {
            "partner_id": self.partner_id,
            "service_technology": 'Mobile',
            "service_supplier": "Másmóvil",
            "mobile_contract_service_info": {
                "icc": "123456",
            },
            "contract_lines": [],
            "iban": self.iban
        }
        response = self.http_public_post(url, data=data)
        self.assertEquals(response.status_code, 400)

    def test_route_right_adsl(self, _):
        url = "/public-api/contract"
        data = {
            "partner_id": self.partner_id,
            "service_address": self.service_address,
            "service_technology": 'ADSL',
            "service_supplier": "Jazztel",
            "adsl_contract_service_info": {
                "phone_number": "654123456",
                'administrative_number': '123',
                'router_product_id': self.router_product.id,
                'router_serial_number': '4637',
                'router_mac_address': 'AA:BB:CC:22:33:11',
                'ppp_user': 'ringo',
                'ppp_password': 'rango',
                'endpoint_user': 'connection',
                'endpoint_password': 'password'
            },
            "contract_lines": [],
            "iban": self.iban
        }
        response = self.http_public_post(url, data=data)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.reason,
                          "OK"
                          )
        content = json.loads(response.content.decode("utf-8"))
        self.assertIn('id', content)
        contract = self.env['contract.contract'].browse(content['id'])
        self.assertEquals(
            contract.name,
            data['adsl_contract_service_info']['phone_number']
        )

        self.assertTrue(contract.adsl_service_contract_info_id)
        contract_service_info = contract.adsl_service_contract_info_id
        self.assertEquals(contract_service_info.phone_number, '654123456')
        self.assertEquals(contract_service_info.administrative_number, '123')
        self.assertEquals(
            contract_service_info.router_lot_id.product_id.id,
            self.router_product.id
        )
        self.assertEquals(
            contract_service_info.router_lot_id.name,
            '4637'
        )
        self.assertEquals(
            contract_service_info.router_lot_id.router_mac_address,
            'AA:BB:CC:22:33:11'
        )
        self.assertEquals(
            contract_service_info.ppp_user,
            'ringo'
        )
        self.assertEquals(
            contract_service_info.ppp_password,
            'rango'
        )
        self.assertEquals(
            contract_service_info.endpoint_user,
            'connection'
        )
        self.assertEquals(
            contract_service_info.endpoint_password,
            'password'
        )
        self.assertEquals(
            contract.service_partner_id.street,
            self.service_address['street']
        )
        self.assertEquals(
            contract.service_partner_id.zip,
            self.service_address['zip_code']
        )
        self.assertEquals(
            contract.service_partner_id.city,
            self.service_address['city']
        )
        self.assertEquals(
            contract.service_partner_id.state_id.code,
            self.service_address['state']
        )

    @odoo.tools.mute_logger("odoo.addons.base_rest.http")
    def test_route_bad_mac_address(self, _):
        url = "/public-api/contract"
        data = {
            "partner_id": self.partner_id,
            "service_address": self.service_address,
            "service_technology": 'ADSL',
            "service_supplier": "Jazztel",
            "adsl_contract_service_info": {
                "phone_number": "654123456",
                'administrative_number': '123',
                'router_product_id': self.router_product.id,
                'router_serial_number': '4637',
                'router_mac_address': 'AA:BB:CC:22:33:XX',
                'ppp_user': 'ringo',
                'ppp_password': 'rango',
                'endpoint_user': 'connection',
                'endpoint_password': 'password'
            },
            "contract_lines": [],
            "iban": self.iban
        }
        response = self.http_public_post(url, data=data)
        self.assertEquals(response.status_code, 400)

    @odoo.tools.mute_logger("odoo.addons.base_rest.http")
    def test_route_bad_router_product_id(self, _):
        url = "/public-api/contract"
        data = {
            "partner_id": self.partner_id,
            "service_address": self.service_address,
            "service_technology": 'ADSL',
            "service_supplier": "Jazztel",
            "adsl_contract_service_info": {
                "phone_number": "654123456",
                'administrative_number': '123',
                'router_product_id': 0,
                'router_serial_number': '4637',
                'router_mac_address': 'AA:BB:CC:22:33:44',
                'ppp_user': 'ringo',
                'ppp_password': 'rango',
                'endpoint_user': 'connection',
                'endpoint_password': 'password'
            },
            "contract_lines": [],
            "iban": self.iban
        }
        response = self.http_public_post(url, data=data)
        self.assertEquals(response.status_code, 400)

    def test_route_right_vodafone_fiber(self, _):
        url = "/public-api/contract"
        data = {
            "partner_id": self.partner_id,
            "service_address": self.service_address,
            "service_technology": 'Fiber',
            "service_supplier": "Vodafone",
            "vodafone_fiber_contract_service_info": {
                "phone_number": "654123456",
                'vodafone_offer_code': 'offer',
                'vodafone_id': "123"
            },
            "contract_lines": [],
            "iban": self.iban
        }
        response = self.http_public_post(url, data=data)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.reason,
                          "OK"
                          )
        content = json.loads(response.content.decode("utf-8"))
        self.assertIn('id', content)
        contract = self.env['contract.contract'].browse(content['id'])
        self.assertEquals(
            contract.name,
            data['vodafone_fiber_contract_service_info']['phone_number']
        )
        self.assertTrue(contract.vodafone_fiber_service_contract_info_id)
        contract_service_info = contract.vodafone_fiber_service_contract_info_id
        self.assertEquals(contract_service_info.phone_number, '654123456')
        self.assertEquals(contract_service_info.vodafone_id, '123')
        self.assertEquals(contract_service_info.vodafone_offer_code, 'offer')
        self.assertEquals(
            contract.service_partner_id.street,
            self.service_address['street']
        )
        self.assertEquals(
            contract.service_partner_id.zip,
            self.service_address['zip_code']
        )
        self.assertEquals(
            contract.service_partner_id.city,
            self.service_address['city']
        )
        self.assertEquals(
            contract.service_partner_id.state_id.code,
            self.service_address['state']
        )

    def test_route_right_mm_fiber(self, _):
        url = "/public-api/contract"
        data = {
            "partner_id": self.partner_id,
            "service_address": self.service_address,
            "service_technology": 'Fiber',
            "service_supplier": "MásMóvil",
            "mm_fiber_contract_service_info": {
                "phone_number": "654123456",
                'mm_id': "123"
            },
            "contract_lines": [],
            "iban": self.iban
        }
        response = self.http_public_post(url, data=data)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.reason,
                          "OK"
                          )
        content = json.loads(response.content.decode("utf-8"))
        self.assertIn('id', content)
        contract = self.env['contract.contract'].browse(content['id'])
        self.assertEquals(
            contract.name,
            data['mm_fiber_contract_service_info']['phone_number']
        )
        self.assertTrue(contract.mm_fiber_service_contract_info_id)
        contract_service_info = contract.mm_fiber_service_contract_info_id
        self.assertEquals(contract_service_info.phone_number, '654123456')
        self.assertEquals(contract_service_info.mm_id, '123')
        self.assertEquals(
            contract.service_partner_id.street,
            self.service_address['street']
        )
        self.assertEquals(
            contract.service_partner_id.zip,
            self.service_address['zip_code']
        )
        self.assertEquals(
            contract.service_partner_id.city,
            self.service_address['city']
        )
        self.assertEquals(
            contract.service_partner_id.state_id.code,
            self.service_address['state']
        )

    @odoo.tools.mute_logger("odoo.addons.base_rest.http")
    def test_route_wrong_missing_service_address(self, _):
        url = "/public-api/contract"
        data = {
            "partner_id": self.ref('base.res_partner_12'),
            "service_technology": 'ADSL',
            "service_supplier": "Jazztel",
            "adsl_contract_service_info": {
                "phone_number": "654123456",
                'administrative_number': '123',
                'router_product_id': self.router_product.id,
                'router_serial_number': '4637',
                'router_mac_address': 'AA:BB:CC:22:33:11',
                'ppp_user': 'ringo',
                'ppp_password': 'rango',
                'endpoint_user': 'connection',
                'endpoint_password': 'password'
            },
            "contract_lines": [],
        }
        response = self.http_public_post(url, data=data)
        self.assertEquals(response.status_code, 400)
