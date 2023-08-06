from typing import Any

from .source_connection import SourceConnection


class AuthSourceConnection(SourceConnection):
    '''Auth-based source connection.

    :param credentials: user or system credentials used for the authentication
    :type credentials: Any
    '''
    _credentials: Any

    def __init__(self: 'AuthSourceConnection', credentials: Any) -> None:
        '''Please refer to this class documentation.'''
        self._credentials = credentials
