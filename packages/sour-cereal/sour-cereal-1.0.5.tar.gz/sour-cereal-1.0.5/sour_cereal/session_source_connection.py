from abc import abstractmethod

from .auth_source_connection import AuthSourceConnection


class SessionSourceConnection(AuthSourceConnection):
    '''A connection to a session-based data source.

    A session will not be opened at the moment of instantiation, but using the
    `open` method instead.
    '''

    @abstractmethod
    def open(self: 'SessionSourceConnection') -> bool:
        '''Opens a session attached to this connection.'''
        return True

    @abstractmethod
    def close(self: 'SessionSourceConnection') -> bool:
        '''Closes the attached session'''
        return True
