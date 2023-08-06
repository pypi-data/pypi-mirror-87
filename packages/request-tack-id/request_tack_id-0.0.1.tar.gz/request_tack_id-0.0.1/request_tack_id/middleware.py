import logging
import uuid

from django.utils.deprecation import MiddlewareMixin
from django.conf import settings

from request_tack_id import *

logger = logging.getLogger(__name__)


class RequestIDMiddleware(MiddlewareMixin):

    def process_request(self, request):
        request_id = self._general_request_id(request)
        local.request_id = request_id
        request.id = request_id

    def get_log_message(self, request, response):
        user = getattr(request, 'user', None)
        user_attribute = getattr(settings, LOG_USER_ATTRIBUTE_SETTING, False)
        if user_attribute:
            user_id = getattr(user, user_attribute, None)
        else:
            user_id = getattr(user, 'pk', None) or getattr(user, 'id', None)
        message = 'method=%s path=%s status=%s' % (request.method, request.path, response.status_code)
        if user_id:
            message += ' user=' + str(user_id)
        return message

    def process_response(self, request, response):
        if getattr(settings, REQUEST_ID_RESPONSE_HEADER_SETTING, False) and getattr(request, 'id', None):
            response[getattr(settings, REQUEST_ID_RESPONSE_HEADER_SETTING)] = request.id

        if not getattr(settings, LOG_REQUESTS_SETTING, False):
            return response

        if 'favicon' in request.path:
            return response

        logger.info(self.get_log_message(request, response))

        try:
            del local.request_id
        except AttributeError:
            pass

        return response

    def _general_request_id(self, request):
        request_id_header = getattr(settings, REQUEST_ID_HEADER_SETTING, None)
        generate_request_if_not_in_header = getattr(settings, GENERATE_REQUEST_ID_IF_NOT_IN_HEADER_SETTING, False)

        if request_id_header:
            default_request_id = getattr(settings, LOG_REQUESTS_NO_SETTING, DEFAULT_NO_REQUEST_ID)
            if generate_request_if_not_in_header:
                default_request_id = self._generate_id()
            return request.META.get(request_id_header, default_request_id)
        return self._generate_id()

    def _generate_id(self):
        return uuid.uuid4().hex
