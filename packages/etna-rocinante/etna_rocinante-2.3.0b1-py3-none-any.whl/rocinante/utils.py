from functools import reduce
import string
from typing import Dict, Mapping

from rocinante.config import Credentials, TokenCredentials, UsernamePasswordCredentials


def sanitize_for_filename(name: str) -> str:
    """
    Sanitize a string so that it can be used as a file name

    :param name:        the string to sanitize
    :return:            the sanitized string
    """
    allowed_chars = string.ascii_lowercase + string.digits
    name = map(lambda x: x if x in allowed_chars else '_', name.lower())
    return reduce(lambda acc, x: (acc + x) if x != '_' or (len(acc) > 0 and acc[-1] != '_') else acc, name, "")


def sanitize_for_environment_name(name: str) -> str:
    """
    Sanitize a string so that it can be used as an environment name

    :param name:        the string to sanitize
    :return:            the sanitized string
    """
    return sanitize_for_filename(name).strip("_")


def make_credentials_context(credentials: Mapping[str, Credentials]) -> Dict[str, str]:
    result = {}
    for name, cred in credentials.items():
        if isinstance(cred, TokenCredentials):
            result[f"{name}_token"] = cred.token
        elif isinstance(cred, UsernamePasswordCredentials):
            result[f"{name}_user"] = cred.username
            result[f"{name}_password"] = cred.password
    return result
