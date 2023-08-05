from ..sc_test_case import SCTestCase
from odoo.exceptions import ValidationError


class MobileISPInfoTest(SCTestCase):
    def setUp(self, *args, **kwargs):
        super().setUp(*args, **kwargs)
        self.mobile_isp_info_args = {
            'delivery_address': self.ref(
                'easy_my_coop.res_partner_cooperator_2_demo'
            ),
            'type': 'new',
            'previous_contract_type': 'contract',
            'previous_provider': self.ref(
                'somconnexio.service_supplier_masmovil'
            ),
            'previous_owner_vat_number': '1234G',
            'previous_owner_name': 'Ford',
            'previous_owner_first_name': 'Windom',
        }

    def test_new_creation_ok(self):
        mobile_isp_info_args_copy = self.mobile_isp_info_args.copy()
        mobile_isp_info = self.env['mobile.isp.info'].create(
            mobile_isp_info_args_copy
        )
        self.assertTrue(mobile_isp_info.id)

    def test_portability_creation_ok(self):
        mobile_isp_info_args_copy = self.mobile_isp_info_args.copy()

        mobile_isp_info_args_copy.update({
            'type': 'portability',
            'icc_donor': '1234',
            'phone_number': '666666666',
            'previous_contract_type': 'contract',
            'previous_provider': self.ref(
                'somconnexio.service_supplier_masmovil'
            ),
            'previous_owner_vat_number': '1234G',
            'previous_owner_name': 'Ford',
            'previous_owner_first_name': 'Windom',
        })

        mobile_isp_info = self.env['mobile.isp.info'].create(
            mobile_isp_info_args_copy
        )
        self.assertTrue(mobile_isp_info.id)

    def test_portability_without_previous_provider(self):
        mobile_isp_info_args_copy = self.mobile_isp_info_args.copy()

        mobile_isp_info_args_copy.update({
            'type': 'portability',
            'icc_donor': '1234',
            'phone_number': '666666666',
            'previous_contract_type': 'contract',
            'previous_provider': None,
            'previous_owner_vat_number': '1234G',
            'previous_owner_name': 'Ford',
            'previous_owner_first_name': 'Windom',
        })

        self.assertRaises(
            ValidationError,
            self.env['mobile.isp.info'].create,
            [mobile_isp_info_args_copy]
        )

    def test_portability_without_previous_contract_type(self):
        mobile_isp_info_args_copy = self.mobile_isp_info_args.copy()

        mobile_isp_info_args_copy.update({
            'type': 'portability',
            'icc_donor': '1234',
            'phone_number': '666666666',
            'previous_contract_type': None,
            'previous_provider': self.ref(
                'somconnexio.service_supplier_masmovil'
            ),
            'previous_owner_vat_number': '1234G',
            'previous_owner_name': 'Ford',
            'previous_owner_first_name': 'Windom',
        })

        self.assertRaises(
            ValidationError,
            self.env['mobile.isp.info'].create,
            [mobile_isp_info_args_copy]
        )

    def test_portability_without_previous_owner_vat_number(self):
        mobile_isp_info_args_copy = self.mobile_isp_info_args.copy()

        mobile_isp_info_args_copy.update({
            'type': 'portability',
            'icc_donor': '1234',
            'phone_number': '666666666',
            'previous_contract_type': 'contract',
            'previous_provider': self.ref(
                'somconnexio.service_supplier_masmovil'
            ),
            'previous_owner_vat_number': '',
            'previous_owner_name': 'Ford',
            'previous_owner_first_name': 'Windom',
        })

        self.assertRaises(
            ValidationError,
            self.env['mobile.isp.info'].create,
            [mobile_isp_info_args_copy]
        )

    def test_portability_without_previous_owner_name(self):
        mobile_isp_info_args_copy = self.mobile_isp_info_args.copy()

        mobile_isp_info_args_copy.update({
            'type': 'portability',
            'icc_donor': '1234',
            'phone_number': '666666666',
            'previous_contract_type': 'contract',
            'previous_provider': self.ref(
                'somconnexio.service_supplier_masmovil'
            ),
            'previous_owner_vat_number': '1234G',
            'previous_owner_name': '',
            'previous_owner_first_name': 'Windom',
        })

        self.assertRaises(
            ValidationError,
            self.env['mobile.isp.info'].create,
            [mobile_isp_info_args_copy]
        )

    def test_portability_without_previous_owner_first_name(self):
        mobile_isp_info_args_copy = self.mobile_isp_info_args.copy()

        mobile_isp_info_args_copy.update({
            'type': 'portability',
            'icc_donor': '1234',
            'phone_number': '666666666',
            'previous_contract_type': 'contract',
            'previous_provider': self.ref(
                'somconnexio.service_supplier_masmovil'
            ),
            'previous_owner_vat_number': '1234g',
            'previous_owner_name': 'ford',
            'previous_owner_first_name': '',
        })

        self.assertRaises(
            ValidationError,
            self.env['mobile.isp.info'].create,
            [mobile_isp_info_args_copy]
        )

    def test_portability_without_phone_number(self):
        mobile_isp_info_args_copy = self.mobile_isp_info_args.copy()

        mobile_isp_info_args_copy.update({
            'type': 'portability',
            'icc_donor': '1234',
            'phone_number': '',
            'previous_contract_type': 'contract',
            'previous_provider': self.ref(
                'somconnexio.service_supplier_masmovil'
            ),
            'previous_owner_vat_number': '1234g',
            'previous_owner_name': 'ford',
            'previous_owner_first_name': '',
        })

        self.assertRaises(
            ValidationError,
            self.env['mobile.isp.info'].create,
            [mobile_isp_info_args_copy]
        )

    def test_portability_without_icc_donor(self):
        mobile_isp_info_args_copy = self.mobile_isp_info_args.copy()

        mobile_isp_info_args_copy.update({
            'type': 'portability',
            'icc_donor': '',
            'phone_number': '666666666',
            'previous_contract_type': 'contract',
            'previous_provider': self.ref(
                'somconnexio.service_supplier_masmovil'
            ),
            'previous_owner_vat_number': '1234g',
            'previous_owner_name': 'ford',
            'previous_owner_first_name': '',
        })

        self.assertRaises(
            ValidationError,
            self.env['mobile.isp.info'].create,
            [mobile_isp_info_args_copy]
        )
