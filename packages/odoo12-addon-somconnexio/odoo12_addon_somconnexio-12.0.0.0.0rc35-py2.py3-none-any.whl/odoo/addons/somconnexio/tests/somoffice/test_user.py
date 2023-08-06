import os
import json
from mock import patch

from ..sc_test_case import SCTestCase
from ...somoffice.user import SomOfficeUser


class SomOfficeUserTestCase(SCTestCase):
    @patch.dict(os.environ, {
        'SOMOFFICE_URL': 'https://somoffice.coopdevs.org/',
        'SOMOFFICE_USER': 'user',
        'SOMOFFICE_PASSWORD': 'password'
    })
    @patch('odoo.addons.somconnexio.somoffice.user.requests', spec=['post'])
    def test_create(self, mock_requests):
        SomOfficeUser(123, 'something321@example.com', '1234G').create()
        mock_requests.post.assert_called_with(
            'https://somoffice.coopdevs.org/api/admin/import_user/',
            headers={'Content-Type': 'application/json'},
            auth=('user', 'password'),
            data=json.dumps({
                "customerCode": 123,
                "customerEmail": "something321@example.com",
                "customerUsername": "1234G",
                "sendEmailNotification": True
            })
        )
