from ..sc_test_case import SCTestCase
from ...opencell_models.crm_account_hierarchy import \
    CRMAccountHierarchyFromContract

from faker import Faker


class OpenCellConfigurationFake:
    seller_code = 'SC'
    customer_category_code = 'CLIENT'


class CRMAccountHierarchyTests(SCTestCase):

    def setUp(self):
        super().setUp()
        fake = Faker('es-ES')
        self.res_partner_bank = {
            'bank_id': self.ref('base.bank_ing'),
            'acc_number': "ES7921000813610123456789",
        }
        self.partner = self.env['res.partner'].create({
            'name': fake.first_name(),
            'firstname': fake.first_name(),
            'lastname': fake.last_name(),
            'street': fake.street_address(),
            'street2': fake.secondary_address(),
            'zip': fake.postcode(),
            'city': fake.city(),
            'state_id': self.ref('base.state_es_m'),
            'country_id': self.ref('base.es'),
            'vat': fake.nif(),
            'mobile': fake.phone_number(),
            'email': fake.email(),
            'lang': "ca_ES",
            'bank_ids': [(0, 0, self.res_partner_bank)]
        })
        child_email = self.env['res.partner'].create({
            'name': 'Partner email',
            'email': 'hello@example.com',
            'parent_id': self.partner.id,
            'type': 'contract-email'
        })
        self.contract_line = {
            "name": "Hola",
            "product_id": self.browse_ref('somconnexio.150Min1GB').id,
            "date_start": '2020-01-01'
        }
        service_tech = self.browse_ref('somconnexio.service_technology_mobile')
        service_supplier = self.browse_ref('somconnexio.service_supplier_masmovil')
        self.mobile_contract_service_info = self.env[
            'mobile.service.contract.info'
        ].create({
            'phone_number': '654987654',
            'icc': '123'
        })
        self.contract = self.env['contract.contract'].create({
            "name": "Test Contract",
            "partner_id": self.partner.id,
            "invoice_partner_id": self.partner.id,
            "service_technology_id": service_tech.id,
            "service_supplier_id": service_supplier.id,
            "mobile_contract_service_info_id": self.mobile_contract_service_info.id,
            "contract_line_ids": [(0, 0, self.contract_line)],
            "email_ids": [(6, 0, [child_email.id])],
            "bank_id": self.partner.bank_ids.id,
        })
        self.opencell_configuration = OpenCellConfigurationFake()

    def test_email(self):
        crm_account_hierarchy = CRMAccountHierarchyFromContract(
            self.contract, "Code"
        )

        self.assertEqual(
            self.contract.invoice_partner_id.email,
            crm_account_hierarchy.email)

    def test_code(self):
        crm_account_hierarchy = CRMAccountHierarchyFromContract(
            self.contract, "Code"
        )

        self.assertEqual(
            "Code",
            crm_account_hierarchy.code)

    def test_crmAccountType(self):
        crm_account_hierarchy = CRMAccountHierarchyFromContract(
            self.contract, "Code"
        )

        self.assertEqual(
            "CA_UA",
            crm_account_hierarchy.crmAccountType)

    def test_phone(self):
        crm_account_hierarchy = CRMAccountHierarchyFromContract(
            self.contract, "Code"
        )

        self.assertEqual(
            self.contract.partner_id.mobile,
            crm_account_hierarchy.phone)

    def test_crmParentCode(self):
        crm_account_hierarchy = CRMAccountHierarchyFromContract(
            self.contract, "Code"
        )

        self.assertEqual(
            self.contract.partner_id.id,
            crm_account_hierarchy.crmParentCode)

    def test_language(self):
        crm_account_hierarchy = CRMAccountHierarchyFromContract(
            self.contract, "Code"
        )

        self.assertEqual(
            "CAT",
            crm_account_hierarchy.language)

    def test_customerCategory(self):
        crm_account_hierarchy = CRMAccountHierarchyFromContract(
            self.contract, "Code"
        )

        self.assertEqual(
            "CLIENT",
            crm_account_hierarchy.customerCategory)

    def test_currency(self):
        crm_account_hierarchy = CRMAccountHierarchyFromContract(
            self.contract, "Code"
        )

        self.assertEqual(
            "EUR",
            crm_account_hierarchy.currency)

    def test_billingCycle(self):
        crm_account_hierarchy = CRMAccountHierarchyFromContract(
            self.contract, "Code"
        )

        self.assertEqual(
            "BC_SC_MONTHLY_1ST",
            crm_account_hierarchy.billingCycle)

    def test_country(self):
        crm_account_hierarchy = CRMAccountHierarchyFromContract(
            self.contract, "Code"
        )

        self.assertEqual(
            "SP",
            crm_account_hierarchy.country)

    def test_electronicBilling(self):
        crm_account_hierarchy = CRMAccountHierarchyFromContract(
            self.contract, "Code"
        )

        self.assertTrue(crm_account_hierarchy.electronicBilling)

    def test_mailingType(self):
        crm_account_hierarchy = CRMAccountHierarchyFromContract(
            self.contract, "Code"
        )

        self.assertEqual(
            "Manual",
            crm_account_hierarchy.mailingType)

    def test_emailTemplate(self):
        crm_account_hierarchy = CRMAccountHierarchyFromContract(
            self.contract, "Code"
        )

        self.assertEqual(
            "EMAIL_TEMPLATE_TEST",
            crm_account_hierarchy.emailTemplate)

    def test_methodOfPayment(self):
        crm_account_hierarchy = CRMAccountHierarchyFromContract(
            self.contract, "Code"
        )

        bank_coordinates = crm_account_hierarchy.methodOfPayment[0].get(
            'bankCoordinates')

        self.assertEqual(
            self.contract.bank_id.id,
            crm_account_hierarchy.methodOfPayment[0].get('mandateIdentification'))
        self.assertEqual(
            self.contract.bank_id.sanitized_acc_number,
            bank_coordinates.get('iban'))
        self.assertEqual(
            self.contract.bank_id.bank_id.bic,
            bank_coordinates.get('bic'))
        self.assertEqual(
            self.contract.bank_id.bank_id.name,
            bank_coordinates.get('bankName'))
        self.assertEqual(
            "{} {}".format(self.partner.firstname, self.partner.lastname),
            bank_coordinates.get('accountOwner'))
