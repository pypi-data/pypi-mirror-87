from rest_framework import exceptions


class APIError(exceptions.APIException):
    status_code = 500
    detail = None
    code = None

    def __init__(self, detail=None, code=None):
        if detail:
            self.detail = detail
        if code:
            self.code = code


class UserExistsError(APIError):
    status_code = 400
    detail = 'user is exists'
    code = 'user_exists'


class UserNotFoundError(APIError):
    status_code = 404
    detail = 'user not found'
    code = 'user_not_found'


class InvalidCodeError(APIError):
    status_code = 400
    detail = 'this code is invalid'
    code = 'invalid_code'


class JWTDecodeError(APIError):
    status_code = 400
    detail = 'jwt decode error'
    code = 'invalid_jwt'


class APIKeyError(APIError):
    status_code = 403
    detail = 'api key not valid'
    code = 'api_key_error'


class SerializerError(APIError):
    status_code = 403
    detail = 'serializer not valid'
    code = 'serializer_error'


class RegisterDecodeTypeError(APIError):
    status_code = 403
    detail = 'token typ not valid'
    code = 'register_decode_type_error'
