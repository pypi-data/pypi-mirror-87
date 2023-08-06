from odoo.http import route

from odoo.addons.base_rest.controllers import main


class NotifyController(main.RestController):
    _root_path = "/api/"
    _collection_name = "emc.services"
    _default_auth = "api_key"

    @route(
        _root_path + "<string:_service_name>/notify_new",
        methods=["POST"],
    )
    def notify_new(self, _service_name, **params):
        return self._process_method(
            _service_name, "notify_new", None, params
        )
