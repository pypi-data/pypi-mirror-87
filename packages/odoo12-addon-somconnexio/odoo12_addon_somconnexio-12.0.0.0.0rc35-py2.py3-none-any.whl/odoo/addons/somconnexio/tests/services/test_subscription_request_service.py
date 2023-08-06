import json
from ..common_service import BaseEMCRestCaseAdmin
from datetime import datetime, timedelta
import odoo


class SubscriptionRequestServiceRestCase(BaseEMCRestCaseAdmin):

    def setUp(self):
        super().setUp()
        self.demo_request_1 = self.browse_ref(
            "easy_my_coop.subscription_request_1_demo"
        )
        self.demo_share_product = (
            self.demo_request_1.share_product_id.product_tmpl_id
        )

        CoopAgreement = self.env['coop.agreement']
        vals_coop_agreement = {
            'partner_id': self.ref("easy_my_coop.res_partner_cooperator_1_demo"),
            'products': False,
            'code': 'CODE',
        }
        self.coop_agreement = CoopAgreement.create(vals_coop_agreement)

        self.vals_subscription = {
            'already_cooperator': False,
            'name': 'Manuel Dublues Test',
            'email': 'manuel@demo-test.net',
            'ordered_parts': 1,
            'address': {
                "street": "Fuenlabarada",
                "zip_code": "28943",
                "city": "Madrid",
                "country": "ES",
                "state": self.browse_ref('base.state_es_m').code,
            },
            'city': 'Brussels',
            'zip_code': '1111',
            'country_id': self.ref('base.es'),
            'date': (datetime.now() - timedelta(days=12)).strftime("%Y-%m-%d"),
            'company_id': 1,
            'source': 'manual',
            'share_product_id': False,
            'lang': 'en_US',
            'sponsor_id': False,
            'iban': 'ES6020808687312159493841',
            "type": "new",
            "vat": "49013933J",
            "coop_agreement": self.coop_agreement.code,
            "voluntary_contribution": 1.33,
            "nationality": "ES",
            "payment_type": "single",
        }

    def test_route_create(self):
        url = "/api/subscription-request"
        response = self.http_post(
            url, data=self.vals_subscription
        )
        self.assertEquals(response.status_code, 200)
        content = json.loads(response.content.decode("utf-8"))
        self.assertIn('id', content)
        sr = self.env['subscription.request'].search([
            ('_api_external_id', '=', content['id']),
            ('name', '=', self.vals_subscription['name'])
        ])
        self.assertEquals(sr.iban, self.vals_subscription['iban'])
        self.assertEquals(sr.vat, self.vals_subscription['vat'])
        self.assertEquals(
            sr.coop_agreement_id.code,
            self.vals_subscription['coop_agreement']
        )
        self.assertEquals(
            sr.voluntary_contribution,
            self.vals_subscription['voluntary_contribution']
        )
        self.assertEquals(
            sr.payment_type,
            self.vals_subscription['payment_type']
        )
        self.assertEquals(
            sr.state_id.code,
            self.vals_subscription['address']["state"]
        )
        self.assertEquals(
            sr.share_product_id.product_tmpl_id.id,
            self.ref("somconnexio.cooperator_share_product")
        )
        self.assertEquals(
            sr.ordered_parts,
            1
        )
        sr.validate_subscription_request()
        partner_id = sr.partner_id
        self.assertEquals(
            partner_id.state_id.code,
            self.vals_subscription['address']["state"]
        )
        self.assertEquals(
            partner_id.country_id.code,
            self.vals_subscription['address']['country']
        )
        self.assertEquals(
            partner_id.vat,
            self.vals_subscription['vat']
        )
        self.assertEquals(
            partner_id.bank_ids.acc_number.replace(" ", ""),
            self.vals_subscription['iban']
        )
        self.assertEquals(
            partner_id.nationality.code,
            self.vals_subscription['nationality']
        )

    @odoo.tools.mute_logger("odoo.addons.base_rest.http")
    def test_route_create_bad_coop_agreement(self):
        url = "/api/subscription-request"
        self.vals_subscription['coop_agreement'] = "XXX"
        response = self.http_post(
            url, data=self.vals_subscription
        )
        self.assertEquals(response.status_code, 400)

    @odoo.tools.mute_logger("odoo.addons.base_rest.http")
    def test_route_create_bad_voluntary_contribution(self):
        url = "/api/subscription-request"
        self.vals_subscription['voluntary_contribution'] = "XXX"
        response = self.http_post(
            url, data=self.vals_subscription
        )
        self.assertEquals(response.status_code, 400)

    @odoo.tools.mute_logger("odoo.addons.base_rest.http")
    def test_route_create_bad_payment_type(self):
        url = "/api/subscription-request"
        self.vals_subscription['payment_type'] = "XXX"
        response = self.http_post(
            url, data=self.vals_subscription
        )
        self.assertEquals(response.status_code, 400)

    @odoo.tools.mute_logger("odoo.addons.base_rest.http")
    def test_route_create_bad_nationality(self):
        url = "/api/subscription-request"
        self.vals_subscription['nationality'] = "XXX"
        response = self.http_post(
            url, data=self.vals_subscription
        )
        self.assertEquals(response.status_code, 400)

    @odoo.tools.mute_logger("odoo.addons.base_rest.http")
    def test_route_create_bad_state(self):
        url = "/api/subscription-request"
        self.vals_subscription['address']['state'] = "XXX"
        response = self.http_post(
            url, data=self.vals_subscription
        )
        self.assertEquals(response.status_code, 400)

    @odoo.tools.mute_logger("odoo.addons.base_rest.http")
    def test_route_create_wo_voluntary_contribution(self):
        url = "/api/subscription-request"
        del self.vals_subscription['voluntary_contribution']
        response = self.http_post(
            url, data=self.vals_subscription
        )
        self.assertEquals(response.status_code, 200)
