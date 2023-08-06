from .auth_source_connection import AuthSourceConnection


class SessionSourceConnection(AuthSourceConnection):
    '''A connection to a session-based data source.

    A session will not be opened at the moment of instantiation, but using the
    `open` method instead.
    '''

    def open(self: 'SessionSourceConnection') -> bool:
        '''Opens a session attached to this connection.'''
        return True

    def close(self: 'SessionSourceConnection') -> bool:
        '''Closes the attached session'''
        return True
