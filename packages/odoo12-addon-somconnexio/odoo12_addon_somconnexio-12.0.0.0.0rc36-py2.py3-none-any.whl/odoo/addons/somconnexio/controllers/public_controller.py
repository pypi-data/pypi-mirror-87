import logging
try:
    from cerberus import Validator
except ImportError:
    _logger = logging.getLogger(__name__)
    _logger.debug("Can not import cerberus")
from odoo import http
from odoo.http import Root
from odoo.http import request
from odoo.addons.base_rest.http import HttpRestRequest
from odoo.addons.somconnexio.services import contract_contract_service
from odoo.addons.base_rest.controllers.main import RestController
from odoo.exceptions import UserError
_logger = logging.getLogger(__name__)

emc_process_method = RestController._process_method


def _process_method(self, service_name, method_name, id=None, params=None):
    _logger.debug("params: {}".format(params))
    return emc_process_method(self, service_name, method_name, id, params)


RestController._process_method = _process_method


class UserPublicController(http.Controller):

    @http.route(['/public-api/contract'], auth='public',
                methods=['POST'], csrf=False)
    def create_contract(self, **kwargs):
        service = contract_contract_service.ContractService(request.env)
        service.v = Validator()
        data = request.params
        _logger.info("contract create body: {}".format(data))
        if not service.v.validate(data, service.validator_create()):
            raise UserError('BadRequest {}'.format(service.v.errors))
        response = service.create(**data)
        if not service.v.validate(response, service.validator_return_create()):
            raise SystemError('Invalid Response {}'.format(service.v.errors))
        return request.make_json_response(response)


ori_get_request = Root.get_request


def get_request(self, httprequest):
    if httprequest.path.startswith('/public-api/contract'):
        return HttpRestRequest(httprequest)
    return ori_get_request(self, httprequest)


Root.get_request = get_request
