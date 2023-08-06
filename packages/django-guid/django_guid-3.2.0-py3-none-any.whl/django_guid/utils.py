import logging
import uuid
from typing import Optional, Union

from django.http import HttpRequest, HttpResponse

from django_guid.config import settings

logger = logging.getLogger('django_guid')


def get_correlation_id_from_header(request: HttpRequest) -> str:
    """
    Returns either the provided GUID or a new one depending on if the provided GUID is valid or not.
    :param request: HttpRequest object
    :return: GUID
    """
    given_guid = str(request.headers.get(settings.guid_header_name))
    if not settings.validate_guid:
        logger.debug('Returning ID from header without validating it as a GUID')
        return given_guid
    elif validate_guid(given_guid):
        logger.debug('%s is a valid GUID', given_guid)
        return given_guid
    else:
        new_guid = generate_guid()
        logger.warning('%s is not a valid GUID. New GUID is %s', given_guid, new_guid)
        return new_guid


def get_id_from_header(request: HttpRequest) -> str:
    """
    Checks if the request contains the header specified in the Django settings.
    If it does, we fetch the header and attempt to validate the contents as GUID.
    If no header is found, we generate a GUID to be injected instead.
    :param request: HttpRequest object
    :return: GUID
    """
    header: str = request.headers.get(settings.guid_header_name)  # Case insensitive headers.get added in Django2.2
    if header:
        logger.info('%s found in the header: %s', settings.guid_header_name, header)
        request.correlation_id = get_correlation_id_from_header(request)
    else:
        request.correlation_id = generate_guid()
        logger.info(
            'Header `%s` was not found in the incoming request. Generated new GUID: %s',
            settings.guid_header_name,
            request.correlation_id,
        )
    return request.correlation_id


def ignored_url(request: Union[HttpRequest, HttpResponse]) -> bool:
    """
    Checks if the current URL is defined in the `IGNORE_URLS` setting.

    :return: Boolean
    """
    return request.get_full_path().strip('/') in settings.ignore_urls


def generate_guid(uuid_length: Optional[int] = None) -> str:
    """
    Generates an UUIDv4/GUID as a string.

    :return: GUID
    """
    if uuid_length is None:
        return uuid.uuid4().hex[: settings.uuid_length]
    return uuid.uuid4().hex[:uuid_length]


def validate_guid(original_guid: str) -> bool:
    """
    Validates a GUID.

    :param original_guid: string to validate
    :return: bool
    """
    try:
        return bool(uuid.UUID(original_guid, version=4).hex)
    except ValueError:
        logger.warning('Failed to validate GUID %s', original_guid)
        return False
