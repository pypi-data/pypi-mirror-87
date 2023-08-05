from ..sc_test_case import SCTestCase

from odoo.addons.somconnexio.otrs_factories.customer_data_from_res_partner \
    import CustomerDataFromResPartner


class CustomerDataFromResPartnerTest(SCTestCase):
    def test_build(self):
        partner = self.env.ref('somconnexio.res_partner_1_demo')

        customer_data = CustomerDataFromResPartner(partner).build()

        self.assertEqual(customer_data.id, partner.id)
        self.assertEqual(customer_data.vat_number, partner.vat)
        self.assertEqual(customer_data.email, partner.email)
        self.assertEqual(customer_data.phone, partner.mobile)
        self.assertEqual(customer_data.first_name, partner.name)
        self.assertEqual(customer_data.name, partner.name)
        self.assertEqual(customer_data.street, partner.full_street)
        self.assertEqual(customer_data.zip, partner.zip)
        self.assertEqual(customer_data.city, partner.city)
        self.assertEqual(customer_data.subdivision, "ES-GI")
