from ..sc_test_case import SCTestCase
from odoo.exceptions import ValidationError


class TestContract(SCTestCase):

    def setUp(self, *args, **kwargs):
        super().setUp(*args, **kwargs)
        self.env = self.env(context=dict(
            self.env.context,
            test_queue_job_no_delay=True,  # no jobs thanks
        ))
        self.Contract = self.env['contract.contract']
        self.product_1 = self.env.ref('product.product_product_1')
        self.router_product = self.env['product.product'].create({
            'name': 'Router',
            'categ_id': self.ref('somconnexio.router_category'),
            'tracking': 'serial'
        })
        self.router_lot = self.env['stock.production.lot'].create({
            'product_id': self.router_product.id,
            'name': '123',
            'router_mac_address': '12:BB:CC:DD:EE:90'
        })
        self.mobile_contract_service_info = self.env[
            'mobile.service.contract.info'
        ].create({
            'phone_number': '654987654',
            'icc': '123'
        })
        self.adsl_contract_service_info = self.env[
            'adsl.service.contract.info'
        ].create({
            'phone_number': '654987654',
            'administrative_number': '123',
            'router_product_id': self.router_product.id,
            'router_lot_id': self.router_lot.id,
            'ppp_user': 'ringo',
            'ppp_password': 'rango',
            'endpoint_user': 'user',
            'endpoint_password': 'password'
        })
        self.vodafone_fiber_contract_service_info = self.env[
            'vodafone.fiber.service.contract.info'
        ].create({
            'phone_number': '654321123',
            'vodafone_id': '123',
            'vodafone_offer_code': '456',
        })
        self.partner = self.browse_ref('base.partner_demo')

    def test_more_than_one_invoice_contact_same_parent(self):
        invoice_partner_1_args = {
            'name': 'Partner for invoice 1',
            'type': 'invoice'
        }
        invoice_partner_2_args = {
            'name': 'Partner for invoice 2',
            'type': 'invoice'
        }
        self.assertRaises(
            ValidationError,
            self.partner.write,
            {
                'child_ids': [
                    (0, False, invoice_partner_1_args),
                    (0, False, invoice_partner_2_args)
                ]
            }
        )

    def test_one_invoice_contact_per_partner(self):
        invoice_partner_args = {
            'name': 'Partner for invoice 1',
            'type': 'invoice'
        }
        self.assertTrue(
            self.partner.write({
                'child_ids': [
                    (0, False, invoice_partner_args),
                ]
            })
        )

    def test_service_contact_wrong_type(self):
        partner_id = self.partner.id
        service_partner = self.env['res.partner'].create({
            'parent_id': partner_id,
            'name': 'Partner not service'
        })
        vals_contract = {
            'name': 'Test Contract Broadband',
            'partner_id': partner_id,
            'service_partner_id': service_partner.id,
            'invoice_partner_id': partner_id,
            'service_technology_id': self.ref(
                "somconnexio.service_technology_adsl"
            ),
            "service_supplier_id": self.ref(
                "somconnexio.service_supplier_orange"
            ),
            'adsl_service_contract_info_id': (
                self.adsl_contract_service_info.id
            ),
            'bank_id': self.partner.bank_ids.id
        }
        self.assertRaises(
            ValidationError,
            self.env['contract.contract'].create,
            (vals_contract,)
        )

    def test_service_contact_right_type(self):
        partner_id = self.partner.id
        service_partner = self.env['res.partner'].create({
            'parent_id': partner_id,
            'name': 'Partner service OK',
            'type': 'service'
        })
        vals_contract = {
            'name': 'Test Contract Broadband',
            'partner_id': partner_id,
            'service_partner_id': service_partner.id,
            'invoice_partner_id': partner_id,
            'service_technology_id': self.ref(
                "somconnexio.service_technology_fiber"
            ),
            'service_supplier_id': self.ref(
                "somconnexio.service_supplier_vodafone"
            ),
            'vodafone_fiber_service_contract_info_id': (
                self.vodafone_fiber_contract_service_info.id
            ),
            'bank_id': self.partner.bank_ids.id
        }
        self.assertTrue(self.env['contract.contract'].create(vals_contract))

    def test_service_contact_wrong_parent(self):
        partner_id = self.partner.id
        service_partner = self.env['res.partner'].create({
            'parent_id': self.ref('easy_my_coop.res_partner_cooperator_3_demo'),
            'name': 'Partner wrong parent',
            'type': 'service'
        })
        vals_contract = {
            'name': 'Test Contract Broadband',
            'partner_id': partner_id,
            'service_partner_id': service_partner.id,
            'invoice_partner_id': partner_id,
            'service_technology_id': self.ref(
                "somconnexio.service_technology_adsl"
            ),
            'adsl_service_contract_info_id': (
                self.adsl_contract_service_info.id
            ),
            'service_supplier_id': self.ref(
                'somconnexio.service_supplier_orange'
            ),
            'bank_id': self.partner.bank_ids.id
        }
        self.assertRaises(
            ValidationError,
            self.env['contract.contract'].create,
            (vals_contract,)
        )

    def test_service_contact_wrong_parent_not_broadband(self):
        partner_id = self.partner.id
        service_partner = self.env['res.partner'].create({
            'parent_id': self.ref('easy_my_coop.res_partner_cooperator_3_demo'),
            'name': 'Partner wrong parent',
            'type': 'service'
        })
        vals_contract = {
            'name': 'Test Contract Mobile',
            'partner_id': partner_id,
            'service_partner_id': service_partner.id,
            'invoice_partner_id': partner_id,
            'service_technology_id': self.ref("somconnexio.service_technology_mobile"),
            'service_supplier_id': self.ref("somconnexio.service_supplier_masmovil"),
            'mobile_contract_service_info_id': self.mobile_contract_service_info.id,
            'bank_id': self.partner.bank_ids.id
        }
        self.assertTrue(self.env['contract.contract'].create(vals_contract))

    def test_service_contact_wrong_type_not_broadband(self):
        partner_id = self.partner.id
        service_partner = self.env['res.partner'].create({
            'parent_id': partner_id,
            'name': 'Partner not service'
        })
        vals_contract = {
            'name': 'Test Contract Mobile',
            'partner_id': partner_id,
            'service_partner_id': service_partner.id,
            'invoice_partner_id': partner_id,
            'service_technology_id': self.ref("somconnexio.service_technology_mobile"),
            'service_supplier_id': self.ref("somconnexio.service_supplier_masmovil"),
            'mobile_contract_service_info_id': self.mobile_contract_service_info.id,
            'bank_id': self.partner.bank_ids.id
        }
        self.assertTrue(self.env['contract.contract'].create(vals_contract))

    def test_email_not_partner_not_child_wrong_type(self):
        partner_id = self.partner.id
        wrong_email = self.env['res.partner'].create({
            'name': 'Bad email',
            'email': 'hello@example.com'
        })
        vals_contract = {
            'name': 'Test Contract Mobile',
            'partner_id': partner_id,
            'invoice_partner_id': partner_id,
            'service_technology_id': self.ref("somconnexio.service_technology_mobile"),
            'service_supplier_id': self.ref("somconnexio.service_supplier_masmovil"),
            'mobile_contract_service_info_id': self.mobile_contract_service_info.id,
            'bank_id': self.partner.bank_ids.id,
            'email_ids': [(6, 0, [wrong_email.id])]
        }
        self.assertRaises(
            ValidationError,
            self.env['contract.contract'].create,
            (vals_contract,)
        )

    def test_email_not_partner_not_child_right_type(self):
        partner_id = self.partner.id
        wrong_email = self.env['res.partner'].create({
            'name': 'Bad email',
            'email': 'hello@example.com',
            'type': 'contract-email',
        })
        vals_contract = {
            'name': 'Test Contract Mobile',
            'partner_id': partner_id,
            'invoice_partner_id': partner_id,
            'service_technology_id': self.ref("somconnexio.service_technology_mobile"),
            'service_supplier_id': self.ref("somconnexio.service_supplier_masmovil"),
            'mobile_contract_service_info_id': self.mobile_contract_service_info.id,
            'bank_id': self.partner.bank_ids.id,
            'email_ids': [(6, 0, [wrong_email.id])]
        }
        self.assertRaises(
            ValidationError,
            self.env['contract.contract'].create,
            (vals_contract,)
        )

    def test_email_same_partner_not_contract_email_type(self):
        partner_id = self.partner.id
        vals_contract = {
            'name': 'Test Contract Mobile',
            'partner_id': partner_id,
            'invoice_partner_id': partner_id,
            'service_technology_id': self.ref("somconnexio.service_technology_mobile"),
            'service_supplier_id': self.ref("somconnexio.service_supplier_masmovil"),
            'mobile_contract_service_info_id': self.mobile_contract_service_info.id,
            'bank_id': self.partner.bank_ids.id,
            'email_ids': [(6, 0, [partner_id])]
        }
        self.assertTrue(self.env['contract.contract'].create(vals_contract))

    def test_email_child_partner_wrong_type(self):
        partner_id = self.partner.id
        child_email = self.env['res.partner'].create({
            'name': 'Bad email',
            'email': 'hello@example.com',
            'parent_id': partner_id,
        })
        vals_contract = {
            'name': 'Test Contract Mobile',
            'partner_id': partner_id,
            'invoice_partner_id': partner_id,
            'service_technology_id': self.ref("somconnexio.service_technology_mobile"),
            'service_supplier_id': self.ref("somconnexio.service_supplier_masmovil"),
            'mobile_contract_service_info_id': self.mobile_contract_service_info.id,
            'bank_id': self.partner.bank_ids.id,
            'email_ids': [(6, 0, [child_email.id])]
        }
        self.assertRaises(
            ValidationError,
            self.env['contract.contract'].create,
            (vals_contract,)
        )

    def test_email_child_partner_right_type(self):
        partner_id = self.partner.id
        child_email = self.env['res.partner'].create({
            'name': 'Right email',
            'email': 'hello@example.com',
            'parent_id': partner_id,
            'type': 'contract-email'
        })
        vals_contract = {
            'name': 'Test Contract Mobile',
            'partner_id': partner_id,
            'invoice_partner_id': partner_id,
            'service_technology_id': self.ref("somconnexio.service_technology_mobile"),
            'service_supplier_id': self.ref("somconnexio.service_supplier_masmovil"),
            'mobile_contract_service_info_id': self.mobile_contract_service_info.id,
            'bank_id': self.partner.bank_ids.id,
            'email_ids': [(6, 0, [child_email.id])]
        }
        self.assertTrue(self.env['contract.contract'].create(vals_contract))
