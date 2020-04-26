from enum import Enum

from ...account.error_codes import AccountErrorCode

SAFESENS_ERROR_CODE_ENUMS = [
    AccountErrorCode,
]

safesens_error_codes = []
for enum in SAFESENS_ERROR_CODE_ENUMS:
    safesens_error_codes.extend([code.value for code in enum])


def get_error_code_from_error(error) -> str:
    """
    Return valid error code from ValidationError.

    It unifies default Django error codes and checks
    if error code is valid.
    """
    code = error.code
    if code in ["required", "blank", "null"]:
        return "required"
    if code in ["unique", "unique_for_date"]:
        return "unique"
    if isinstance(code, Enum):
        code = code.value
    if code not in safesens_error_codes:
        return "invalid"
    return code