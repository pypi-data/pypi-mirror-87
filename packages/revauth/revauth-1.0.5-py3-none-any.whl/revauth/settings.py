from django.conf import settings
from django.utils.module_loading import import_string


DEFAULTS = {
    # Base API policies
    'DEBUG': True,
    'AUTH_VERSION': 'v3',
    'DEFAULT_IDENTITY': 'email',
    'DEFAULT_PROFILE_CLASS': 'revauth.models.UserProfile',
    'DEFAULT_BASE_PATH': 'auth',
    'DEFAULT_HANDLER_CLASS': 'revauth.handlers.DefaultHandler',
    'DEFAULT_REGISTER_SERIALIZER': 'revauth.serializers.RegisterSerializer',
    'DEFAULT_VALIDATION_ISSUER': 'register',
    'GOOGLE_CLIENT_ID': '782455260604-925fnvgriavsgqs89edlecqcgfee8d49.apps.googleusercontent.com',
    'APPLE_CLIENT_ID': 'fake',
}
# List of settings that may be in string import notation.
IMPORT_STRINGS = [
    'DEFAULT_PROFILE_CLASS', 'DEFAULT_HANDLER_CLASS', 'DEFAULT_REGISTER_SERIALIZER'
]


def perform_import(val, setting_name):
    """
    If the given setting is a string import notation,
    then perform the necessary import or imports.
    """
    if val is None:
        return None
    elif isinstance(val, str):
        return import_from_string(val, setting_name)
    elif isinstance(val, (list, tuple)):
        return [import_from_string(item, setting_name) for item in val]
    return val


def import_from_string(val, setting_name):
    """
    Attempt to import a class from a string representation.
    """
    try:
        return import_string(val)
    except ImportError as e:
        msg = "Could not import '%s' for API setting '%s'. %s: %s." % (val, setting_name, e.__class__.__name__, e)
        raise ImportError(msg)


class APISettings:
    def __init__(self, defaults=None, import_strings=None):
        self.defaults = defaults or DEFAULTS
        self.import_strings = import_strings or IMPORT_STRINGS

    @ property
    def user_settings(self):
        return getattr(settings, 'REVAUTH', {})

    def __getattr__(self, attr):
        try:
            # Check if present in user settings
            val = self.user_settings[attr]
        except KeyError:
            # Fall back to defaults
            val = self.defaults[attr]

        # Coerce import strings into classes
        if attr in self.import_strings:
            val = perform_import(val, attr)

        # Cache the result
        setattr(self, attr, val)
        return val


api_settings = APISettings(DEFAULTS, IMPORT_STRINGS)
