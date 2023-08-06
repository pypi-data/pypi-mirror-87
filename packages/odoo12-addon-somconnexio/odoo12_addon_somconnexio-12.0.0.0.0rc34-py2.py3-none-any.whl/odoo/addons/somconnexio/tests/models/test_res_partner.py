from ..sc_test_case import SCTestCase


class TestResPartner(SCTestCase):

    def setUp(self, *args, **kwargs):
        super().setUp(*args, **kwargs)

    def test_contract_email_create(self):
        parent_partner = self.env['res.partner'].create({
            'name': 'test',
        })
        partner = self.env['res.partner'].create({
            'parent_id': parent_partner.id,
            'name': 'test',
            'street': 'test',
            'street2': 'test',
            'city': 'city',
            'state_id': self.ref('base.state_es_b'),
            'country_id': self.ref('base.es'),
            'customer': True,
            'email': 'test@example.com',
            'type': 'contract-email'
        })
        self.assertFalse(partner.name)
        self.assertFalse(partner.street)
        self.assertFalse(partner.street2)
        self.assertFalse(partner.city)
        self.assertFalse(partner.state_id)
        self.assertFalse(partner.country_id)
        self.assertFalse(partner.customer)
        self.assertFalse(partner.supplier)
        self.assertEqual(partner.email, 'test@example.com')
        self.assertEqual(partner.type, 'contract-email')
        self.assertEqual(partner.parent_id, parent_partner)

    def test_contract_email_write_set_before(self):
        parent_partner = self.env['res.partner'].create({
            'name': 'test',
        })
        partner = self.env['res.partner'].create({
            'parent_id': parent_partner.id,
            'name': 'test',
            'street': 'test',
            'street2': 'test',
            'city': 'city',
            'state_id': self.ref('base.state_es_b'),
            'country_id': self.ref('base.es'),
            'customer': True,
            'email': 'test@example.com',
        })
        partner.write({
            'type': 'contract-email'
        })
        self.assertFalse(partner.name)
        self.assertFalse(partner.street)
        self.assertFalse(partner.street2)
        self.assertFalse(partner.city)
        self.assertFalse(partner.state_id)
        self.assertFalse(partner.country_id)
        self.assertFalse(partner.customer)
        self.assertFalse(partner.supplier)
        self.assertEqual(partner.email, 'test@example.com')
        self.assertEqual(partner.type, 'contract-email')
        self.assertEqual(partner.parent_id, parent_partner)

    def test_contract_email_write_set_in(self):
        parent_partner = self.env['res.partner'].create({
            'name': 'test',
        })
        partner = self.env['res.partner'].create({})
        partner.write({
            'type': 'contract-email',
            'parent_id': parent_partner.id,
            'name': 'test',
            'street': 'test',
            'street2': 'test',
            'city': 'city',
            'state_id': self.ref('base.state_es_b'),
            'country_id': self.ref('base.es'),
            'customer': True,
            'email': 'test@example.com',
        })
        self.assertFalse(partner.name)
        self.assertFalse(partner.street)
        self.assertFalse(partner.street2)
        self.assertFalse(partner.city)
        self.assertFalse(partner.state_id)
        self.assertFalse(partner.country_id)
        self.assertFalse(partner.customer)
        self.assertFalse(partner.supplier)
        self.assertEqual(partner.email, 'test@example.com')
        self.assertEqual(partner.type, 'contract-email')
        self.assertEqual(partner.parent_id, parent_partner)

    def test_not_contract_email_create(self):
        parent_partner = self.env['res.partner'].create({
            'name': 'test',
        })
        partner = self.env['res.partner'].create({
            'parent_id': parent_partner.id,
            'name': 'test',
            'street': 'test',
            'street2': 'test2',
            'city': 'test',
            'state_id': self.ref('base.state_es_b'),
            'country_id': self.ref('base.es'),
            'customer': True,
            'email': 'test@example.com',
            'type': 'contact'
        })
        self.assertEqual(partner.name, 'test')
        self.assertEqual(partner.street, 'test')
        self.assertEqual(partner.street2, 'test2')
        self.assertEqual(partner.full_street, 'test test2')
        self.assertEqual(partner.city, 'test')
        self.assertEqual(partner.state_id, self.browse_ref('base.state_es_b'))
        self.assertEqual(partner.country_id, self.browse_ref('base.es'))
        self.assertEqual(partner.customer, True)
        self.assertEqual(partner.supplier, False)
        self.assertEqual(partner.email, 'test@example.com')
        self.assertEqual(partner.type, 'contact')
        self.assertEqual(partner.parent_id, parent_partner)

    def test_not_contract_email_write_set_before(self):
        parent_partner = self.env['res.partner'].create({
            'name': 'test',
        })
        partner = self.env['res.partner'].create({
            'parent_id': parent_partner.id,
            'name': 'test',
            'street': 'test',
            'street2': 'test2',
            'city': 'test',
            'state_id': self.ref('base.state_es_b'),
            'country_id': self.ref('base.es'),
            'customer': True,
            'email': 'test@example.com',
        })
        partner.write({
            'type': 'contact'
        })
        self.assertEqual(partner.name, 'test')
        self.assertEqual(partner.street, 'test')
        self.assertEqual(partner.street2, 'test2')
        self.assertEqual(partner.full_street, 'test test2')
        self.assertEqual(partner.city, 'test')
        self.assertEqual(partner.state_id, self.browse_ref('base.state_es_b'))
        self.assertEqual(partner.country_id, self.browse_ref('base.es'))
        self.assertEqual(partner.customer, True)
        self.assertEqual(partner.supplier, False)
        self.assertEqual(partner.email, 'test@example.com')
        self.assertEqual(partner.type, 'contact')
        self.assertEqual(partner.parent_id, parent_partner)

    def test_not_contract_email_write_set_in(self):
        parent_partner = self.env['res.partner'].create({
            'name': 'test',
        })
        partner = self.env['res.partner'].create({})
        partner.write({
            'type': 'contact',
            'parent_id': parent_partner.id,
            'name': 'test',
            'street': 'test',
            'street2': 'test2',
            'city': 'test',
            'state_id': self.ref('base.state_es_b'),
            'country_id': self.ref('base.es'),
            'customer': True,
            'email': 'test@example.com',
        })
        self.assertEqual(partner.name, 'test')
        self.assertEqual(partner.street, 'test')
        self.assertEqual(partner.street2, 'test2')
        self.assertEqual(partner.full_street, 'test test2')
        self.assertEqual(partner.city, 'test')
        self.assertEqual(partner.state_id, self.browse_ref('base.state_es_b'))
        self.assertEqual(partner.country_id, self.browse_ref('base.es'))
        self.assertEqual(partner.customer, True)
        self.assertEqual(partner.supplier, False)
        self.assertEqual(partner.email, 'test@example.com')
        self.assertEqual(partner.type, 'contact')
        self.assertEqual(partner.parent_id, parent_partner)
