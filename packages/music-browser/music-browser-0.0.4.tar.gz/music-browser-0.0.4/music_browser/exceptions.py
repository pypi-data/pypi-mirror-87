class MusicBrowserException(Exception):
    pass


class RequiredFieldMissing(MusicBrowserException):
    pass


class UnknownField(MusicBrowserException):
    pass
