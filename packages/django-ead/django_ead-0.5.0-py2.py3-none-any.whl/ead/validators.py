import re

from django.core.exceptions import ValidationError


NAME_START_CHAR = ''.join(r'''
  :
  A-Z
  a-z
  _
  \u00C0-\u00D6
  \u00D8-\u00F6
  \u00F8-\u02FF
  \u0370-\u037D
  \u037F-\u1FFF
  \u200C-\u200D
  \u2070-\u218F
  \u2C00-\u2FEF
  \u3001-\uD7FF
  \uF900-\uFDCF
  \uFDF0-\uFFFD
  \u10000-\uEFFFF
'''.split())
NAME_CHAR = ''.join(r'''
  {}
  \-
  \.
  0-9
  \u00B7
  \u0300-\u036F
  \u203F-\u2040
'''.format(NAME_START_CHAR).split())

DATE_TIME_PATTERN = re.compile(
    r'\d{4}(-\d{2}(-\d{2}(T\d{2}:\d{2}:\d{2}(Z|([+-]\d{2}:\d{2}))?)?)?)?')
ID_PATTERN = re.compile(
    r'[{}]([{}])*'.format(NAME_START_CHAR, NAME_CHAR))
NM_TOKEN_PATTERN = re.compile(r'[{}]+'.format(NAME_CHAR))


def validate_date_time(value):
    """Raise ValidationError if `value` does not constitute an ISO 8601
    pattern.

    The valid patterns are:

    * YYYY-MM-DD
    * YYYY-MM
    * YYYY
    * YYYY-MM-DDThh:mm:ss
    * YYYY-MM-DDThh:mm:ss[+|-]hh:mm
    * YYYY-MM-DDThh:mm:ssZ

    """
    if DATE_TIME_PATTERN.fullmatch(value) is None:
        raise ValidationError('"{}" is not a valid date-time'.format(value))


def validate_id(value):
    """Raise ValidationError if `value` does not consitute an ID.

    An ID must begin with an alpha, not numeric, character, either
    upper or lowercase, and may contain a . (period), - (hyphen), or _
    (underscore), but not a blank space.

    """
    if ID_PATTERN.fullmatch(value) is None:
        raise ValidationError('"{}" is not a valid ID'.format(value))


def validate_nmtoken(value):
    """Raise ValidationError if `value` does not constitute a name token.

    A name token can consists of any alpha or numeric character, as
    well as a . (period), : (colon), - (hyphen), or _ (underscore),
    but not a blank space.

    """
    if NM_TOKEN_PATTERN.fullmatch(value) is None:
        raise ValidationError('"{}" is not a valid name'.format(value))


def validate_token(value):
    """Raise ValidationError if `value` does not constitute a token.

    A token is a type of string that may not contain carriage return,
    line feed or tab characters, leading or trailing spaces, nor any
    internal sequence of two or more spaces.

    """
    if value.strip() != value or '\r' in value or '\n' in value or \
       '\t' in value or '  ' in value:
        raise ValidationError('"{}" is not a valid token'.format(value))
