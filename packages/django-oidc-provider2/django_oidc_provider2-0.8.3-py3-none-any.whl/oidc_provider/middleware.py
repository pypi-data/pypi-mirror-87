from django.http import HttpRequest, HttpResponse

from oidc_provider import settings
from oidc_provider.lib.utils.common import get_browser_state_or_default


class SessionManagementMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    """
    Maintain a `op_browser_state` cookie along with the `sessionid` cookie that
    represents the End-User's login state at the OP. If the user is not logged
    in then use the value of settings.OIDC_UNAUTHENTICATED_SESSION_MANAGEMENT_KEY.
    """

    def __call__(self, request: HttpRequest):
        response: HttpResponse = self.get_response(request)

        if settings.get('OIDC_SESSION_MANAGEMENT_ENABLE'):
            response.set_cookie('op_browser_state', get_browser_state_or_default(request))

        return response
