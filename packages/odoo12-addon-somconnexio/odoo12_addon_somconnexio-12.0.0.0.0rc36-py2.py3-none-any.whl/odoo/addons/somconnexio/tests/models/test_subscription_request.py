from ..sc_test_case import SCTestCase
from odoo.exceptions import ValidationError, UserError
from datetime import datetime, timedelta


class TestSubscription(SCTestCase):

    def setUp(self, *args, **kwargs):
        result = super().setUp(*args, **kwargs)
        self.SubscriptionRequest = self.env['subscription.request']
        crm_lead_pool = self.env['crm.lead']
        vals_lead_a = {
            'name': 'Test Lead a'
        }
        vals_lead_b = {
            'name': 'Test Lead b'
        }
        self.crm_lead_a = crm_lead_pool.create(vals_lead_a)
        self.crm_lead_b = crm_lead_pool.create(vals_lead_b)
        self.vals_subscription = {
            'already_cooperator': False,
            'name': 'Manuel Dublues Test',
            'email': 'manuel@demo-test.net',
            'ordered_parts': 1,
            'address': 'schaerbeekstraat',
            'city': 'Brussels',
            'zip_code': '1111',
            'country_id': self.ref('base.es'),
            'date': datetime.now() - timedelta(days=12),
            'company_id': 1,
            'source': 'manual',
            'share_product_id': False,
            'lang': 'en_US',
            'sponsor_id': False,
            'iban': 'ES6020808687312159493841'
        }
        CoopAgreement = self.env['coop.agreement']
        vals_coop_agreement = {
            'partner_id': self.ref("easy_my_coop.res_partner_cooperator_1_demo"),
            'products': False,
            'code': 'CODE',
        }
        self.coop_agreement = CoopAgreement.create(vals_coop_agreement)
        if not self.env.ref('easy_my_coop.sequence_subscription_journal', False):
            journal_sequence = self.env['ir.sequence'].create({
                "name": "Account Default Subscription Journal",
                "padding": 3,
                "prefix": "SUBJ/%(year)s/",
                "use_date_range": True
            })
            self.env['ir.model.data'].create({
                'module': 'easy_my_coop',
                'name': 'sequence_subscription_journal',
                'model': 'ir.sequence',
                'res_id': journal_sequence.id,
                'noupdate': True
            })
        if not self.env.ref('easy_my_coop.subscription_journal', False):
            journal = self.env['account.journal'].create({
                "name": "Subscription Journal",
                "code": "SUBJ",
                "type": "sale",
                "sequence_id": self.ref("easy_my_coop.sequence_subscription_journal")
            })
            self.env['ir.model.data'].create({
                'module': 'easy_my_coop',
                'name': 'subscription_journal',
                'model': 'account.journal',
                'res_id': journal.id,
                'noupdate': True
            })
        if not self.env.ref("easy_my_coop.account_cooperator_demo", False):
            account = self.env['account.account'].create({
                "code": "416101",
                "name": "Cooperators",
                "user_type_id": self.ref("account.data_account_type_receivable"),
                "reconcile": True
            })
            self.env['ir.model.data'].create({
                'module': 'easy_my_coop',
                'name': 'account_cooperator_demo',
                'model': 'account.account',
                'res_id': account.id,
                'noupdate': True
            })
            self.browse_ref('base.main_company').property_cooperator_account = (
                self.browse_ref('easy_my_coop.account_cooperator_demo')
            )
        return result

    def test_create_subscription_coop_agreement_sponsorship(self):
        vals_subscription_sponsorship = self.vals_subscription.copy()
        vals_subscription_sponsorship.update({
            'share_product_id': False,
            'ordered_parts': False,
            'type': 'sponsorship_coop_agreement',
            'coop_agreement_id': self.coop_agreement.id,
        })
        subscription = self.SubscriptionRequest.create(vals_subscription_sponsorship)
        self.assertEqual(subscription.subscription_amount, 0.0)

    def test_create_subscription_coop_agreement_sponsorship_without_coop_agreement_raise_validation_error(self):  # noqa
        vals_subscription_sponsorship = self.vals_subscription.copy()
        vals_subscription_sponsorship.update({
            'share_product_id': False,
            'ordered_parts': False,
            'type': 'sponsorship_coop_agreement',
            'coop_agreement_id': False,
        })

        self.assertRaises(
            ValidationError,
            self.SubscriptionRequest.create,
            vals_subscription_sponsorship
        )

    def test_validate_subscription_coop_agreement_sponsorship(self):
        vals_subscription_sponsorship = self.vals_subscription.copy()
        vals_subscription_sponsorship.update({
            'share_product_id': False,
            'ordered_parts': False,
            'type': 'sponsorship_coop_agreement',
            'coop_agreement_id': self.coop_agreement.id,
        })
        subscription = self.SubscriptionRequest.create(vals_subscription_sponsorship)
        subscription.validate_subscription_request()

        partner = subscription.partner_id
        self.assertEqual(partner.coop_agreement_id.id, self.coop_agreement.id)

        self.assertFalse(partner.coop_candidate)
        self.assertFalse(partner.coop_sponsee)
        self.assertTrue(partner.coop_agreement)

    def test_validate_subscription_nie_wo_nacionality(self):
        vals_subscription_sponsorship = self.vals_subscription.copy()
        vals_subscription_sponsorship.update({
            'share_product_id': False,
            'ordered_parts': False,
            'type': 'sponsorship_coop_agreement',
            'coop_agreement_id': self.coop_agreement.id,
        })
        vals_subscription_sponsorship.update({
            'vat': 'Z1234567R',
            'nationality': False,
        })
        self.assertRaises(
            ValidationError,
            self.SubscriptionRequest.create,
            vals_subscription_sponsorship
        )

    def test_validate_subscription_nacionality_in_partner(self):
        vals_subscription_sponsorship = self.vals_subscription.copy()
        vals_subscription_sponsorship.update({
            'share_product_id': False,
            'ordered_parts': False,
            'type': 'sponsorship_coop_agreement',
            'coop_agreement_id': self.coop_agreement.id,
        })
        vals_subscription_sponsorship.update({
            'vat': 'Z1234567R',
            'nationality': self.ref('base.es'),
        })
        subscription = self.SubscriptionRequest.create(
            vals_subscription_sponsorship
        )
        subscription.validate_subscription_request()
        partner = subscription.partner_id
        self.assertEquals(partner.nationality, self.browse_ref('base.es'))

    def test_validate_regular_subscription_bind_partner(self):
        vals_regular_subscription = self.vals_subscription.copy()
        subscription = self.SubscriptionRequest.create(
            vals_regular_subscription
        )
        subscription.update({
            "share_product_id": self.browse_ref(
                "easy_my_coop.product_template_share_type_2_demo"
            ).product_variant_id.id,
        })
        self.crm_lead_a.subscription_request_id = subscription
        subscription.validate_subscription_request()
        partner = self.crm_lead_a.partner_id
        self.assertEquals(partner, subscription.partner_id)

    def test_validate_sponsor_subscription_bind_partner(self):
        vals_sponsor_subscription = self.vals_subscription.copy()
        sponsor_id = self.ref("easy_my_coop.res_partner_cooperator_1_demo")
        vals_sponsor_subscription.update({
            'share_product_id': False,
            'ordered_parts': False,
            'type': 'sponsorship',
            'sponsor_id': sponsor_id,
        })
        subscription = self.SubscriptionRequest.create(
            vals_sponsor_subscription
        )
        self.crm_lead_a.subscription_request_id = subscription
        subscription.validate_subscription_request()
        partner = self.crm_lead_a.partner_id
        self.assertEquals(partner, subscription.partner_id)

    def test_validate_coop_agreement_subscription_bind_partner(self):
        vals_coop_agreement_subscription = self.vals_subscription.copy()
        vals_coop_agreement_subscription.update({
            'share_product_id': False,
            'ordered_parts': False,
            'type': 'sponsorship_coop_agreement',
            'coop_agreement_id': self.coop_agreement.id,
        })
        vals_coop_agreement_subscription.update({
            'vat': 'Z1234567R',
            'nationality': self.ref('base.es'),
        })
        subscription = self.SubscriptionRequest.create(
            vals_coop_agreement_subscription
        )
        self.crm_lead_a.subscription_request_id = subscription
        subscription.validate_subscription_request()
        partner = self.crm_lead_a.partner_id
        self.assertEquals(partner, subscription.partner_id)

    def test_validate_different_crm_leads_bind_partner(self):
        vals_regular_subscription = self.vals_subscription.copy()
        vals_different_subscription = self.vals_subscription.copy()
        vals_different_subscription.update({
            "share_product_id": self.browse_ref(
                "easy_my_coop.product_template_share_type_2_demo"
            ).product_variant_id.id,
        })
        vals_regular_subscription.update({
            "share_product_id": self.browse_ref(
                "easy_my_coop.product_template_share_type_2_demo"
            ).product_variant_id.id,
        })
        regular_subscription = self.SubscriptionRequest.create(
            vals_regular_subscription
        )
        different_subscription = self.SubscriptionRequest.create(
            vals_different_subscription
        )
        self.crm_lead_a.subscription_request_id = regular_subscription
        self.crm_lead_b.subscription_request_id = different_subscription
        regular_subscription.validate_subscription_request()
        partner = self.crm_lead_a.partner_id
        self.assertEquals(partner, regular_subscription.partner_id)
        self.assertFalse(self.crm_lead_b.partner_id)

    def test_validate_many_crm_leads_same_bind_partner(self):
        vals_regular_subscription = self.vals_subscription.copy()
        vals_regular_subscription.update({
            "share_product_id": self.browse_ref(
                "easy_my_coop.product_template_share_type_2_demo"
            ).product_variant_id.id,
        })
        regular_subscription = self.SubscriptionRequest.create(
            vals_regular_subscription
        )
        self.crm_lead_a.subscription_request_id = regular_subscription
        self.crm_lead_b.subscription_request_id = regular_subscription
        regular_subscription.validate_subscription_request()
        partner_a = self.crm_lead_a.partner_id
        partner_b = self.crm_lead_b.partner_id
        self.assertEquals(partner_a, regular_subscription.partner_id)
        self.assertEquals(partner_b, regular_subscription.partner_id)

    def test_validate_subscription_error_not_bind(self):
        vals_subscription = self.vals_subscription.copy()
        vals_subscription.update({
            'share_product_id': self.browse_ref(
                "easy_my_coop.product_template_share_type_2_demo"
            ).product_variant_id.id,
            'ordered_parts': False,
        })
        subscription = self.SubscriptionRequest.create(
            vals_subscription
        )
        self.crm_lead_a = subscription
        self.assertRaises(
            UserError,
            subscription.validate_subscription_request,
        )
        self.assertFalse(self.crm_lead_a.partner_id)
