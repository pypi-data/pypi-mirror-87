from otrs_somconnexio.otrs_models.coverage.adsl import ADSLCoverage
from otrs_somconnexio.otrs_models.coverage.mm_fibre import MMFibreCoverage
from otrs_somconnexio.otrs_models.coverage.vdf_fibre import VdfFibreCoverage

from odoo.tests.common import TransactionCase


class TestContractAddressChangeWizard(TransactionCase):

    def setUp(self, *args, **kwargs):
        super().setUp(*args, **kwargs)
        self.env = self.env(context=dict(
            self.env.context,
            test_queue_job_no_delay=True,  # no jobs thanks
        ))
        self.vodafone_fiber_contract_service_info = self.env[
            'vodafone.fiber.service.contract.info'
        ].create({
            'phone_number': '654321123',
            'vodafone_id': '123',
            'vodafone_offer_code': '456',
        })
        self.partner = self.browse_ref('base.partner_demo')
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
        self.contract = self.env['contract.contract'].create(vals_contract)

    def test_wizard_address_change_ok(self):
        wizard = self.env['contract.address.change.wizard'].with_context(
            active_id=self.partner.id
        ).create({
            'partner_bank_id': self.partner.bank_ids.id,
            'service_street': 'Carrer Nou 123',
            'service_street2': 'Principal A',
            'service_zip_code': '00123',
            'service_city': 'Barcelona',
            'service_state_id': self.ref('base.state_es_b'),
            'service_country_id': self.ref('base.es'),
            'service_supplier_id': self.ref('somconnexio.service_supplier_orange'),
            'previous_product_id': self.ref('somconnexio.ADSL20MB100MinFixMobile'),
            'product_id': self.ref('somconnexio.Fibra1Gb'),
            'mm_fiber_coverage': MMFibreCoverage.VALUES[2][0],
            'vdf_fiber_coverage': VdfFibreCoverage.VALUES[3][0],
            'adsl_coverage': ADSLCoverage.VALUES[6][0]
        })
        crm_lead_action = wizard.button_change()
        crm_lead = self.env["crm.lead"].browse(crm_lead_action["res_id"])
        crm_lead_line = crm_lead.lead_line_ids[0]

        self.assertEquals(crm_lead.name, "Change Address process")
        self.assertEquals(crm_lead.partner_id, self.partner)
        self.assertEquals(
            crm_lead.iban,
            self.partner.bank_ids.sanitized_acc_number
        )
        self.assertEquals(
            crm_lead_line.broadband_isp_info.service_street,
            'Carrer Nou 123'
        )
        self.assertEquals(
            crm_lead_line.broadband_isp_info.service_street2,
            'Principal A'
        )
        self.assertEquals(
            crm_lead_line.broadband_isp_info.service_zip_code,
            '00123'
        )
        self.assertEquals(
            crm_lead_line.broadband_isp_info.service_city,
            'Barcelona'
        )
        self.assertEquals(
            crm_lead_line.broadband_isp_info.service_state_id,
            self.browse_ref('base.state_es_b')
        )
        self.assertEquals(
            crm_lead_line.broadband_isp_info.service_country_id,
            self.browse_ref('base.es')
        )
        self.assertEquals(
            crm_lead_line.broadband_isp_info.service_supplier_id,
            self.browse_ref('somconnexio.service_supplier_orange')
        )
        self.assertEquals(
            crm_lead_line.product_id,
            self.browse_ref('somconnexio.Fibra1Gb')
        )
        self.assertEquals(
            crm_lead_line.broadband_isp_info.adsl_coverage,
            ADSLCoverage.VALUES[6][0]
        )
        self.assertEquals(
            crm_lead_line.broadband_isp_info.vdf_fiber_coverage,
            VdfFibreCoverage.VALUES[3][0]
        )
        self.assertEquals(
            crm_lead_line.broadband_isp_info.mm_fiber_coverage,
            MMFibreCoverage.VALUES[2][0]
        )
        self.assertTrue(crm_lead_line.broadband_isp_info.change_address)
