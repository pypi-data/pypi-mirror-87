from mock import Mock, patch
from odoo.tests import TransactionCase
from ...opencell_services.contract_service import ContractService
from ...opencell_models.crm_account_hierarchy import CRMAccountHierarchyFromContract

from ..factories import ContractFactory


class SubscriptionFake:
    userAccount = 1234


class ContractServiceTests(TransactionCase):

    def setUp(self):
        self.contract = ContractFactory()
        self.subscription = SubscriptionFake()

    @patch('odoo.addons.somconnexio.opencell_services.contract_service.SubscriptionService') # noqa
    @patch("odoo.addons.somconnexio.opencell_services.contract_service.CRMAccountHierarchy") # noqa
    def test_contract_service_update(self, CRMAccountHierarchyMock, MockSubscriptionService):  # noqa
        """ Call to CRMAccountHierarchy when call to update of ContractService """
        MockSubscriptionService.return_value = Mock(spec=['subscription'])
        MockSubscriptionService.return_value.subscription = SubscriptionFake
        crm_account_hierarchy_from_contract = CRMAccountHierarchyFromContract(
            self.contract, self.subscription.userAccount
        )
        ContractService(self.contract).update()
        CRMAccountHierarchyMock.update.assert_called_with(
            **crm_account_hierarchy_from_contract.to_dict()
        )
