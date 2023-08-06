from odoo.tests.common import SavepointCase


class SCTestCase(SavepointCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # disable tracking test suite wise
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
