class HttpException(Exception):
    name = ""
    status_code = None
    response = None

    def __init__(self, status_code=None, response=None):
        if status_code:
            self.status_code = status_code
        self.response = response

    def __repr__(self):
        return "HTTP {} {}".format(self.status_code, self.name)

    def __str__(self):
        return repr(self)

    def __unicode__(self):
        return repr(self)


class BadRequest(HttpException):
    name = "Bad Request"
    status_code = 400


class Unauthorized(HttpException):
    name = "Unauthorized"
    status_code = 401


class Forbidden(HttpException):
    name = "Forbidden"
    status_code = 403


class NotFound(HttpException):
    name = "Not Found"
    status_code = 404


class MethodNotAllowed(HttpException):
    name = "Method Not Allowed"
    status_code = 405


class TooManyRequests(HttpException):
    name = "Too Many Requests"
    status_code = 429


class InternalServerError(HttpException):
    name = "Internal Server Error"
    status_code = 500


class BadGateway(HttpException):
    name = "Bad Gateway"
    status_code = 502


class ServiceUnavailable(HttpException):
    name = "Service Unavailable"
    status_code = 503


class ConnectionTimeout(HttpException):
    name = "Connection Timeout"
    status_code = 522


class NotLoggedIn(Exception):
    def __repr__(self):
        return "You are not logged into topdesk! You need to call .login_person() or .login_operator() before using the API."

    def __str__(self):
        return repr(self)

    def __unicode__(self):
        return repr(self)



exceptions = [
]

def _find_exceptions():
    for name, obj in globals().items():
        try:
            is_http_exception = issubclass(obj, HttpException)
        except TypeError:
            is_http_exception = False
        if not is_http_exception or obj.status_code is None:
            continue
        exceptions.append(obj)

_find_exceptions()
del _find_exceptions


def get_exception(status_code, response):
    for cls in exceptions:
        if cls.status_code == status_code:
            return cls(response=response)
    return HttpException(status_code=status_code, response=response)
