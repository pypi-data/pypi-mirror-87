'''Defines abstraction for any data source.'''
from abc import ABC, abstractmethod
from typing import Any


class SourceConnectionInterface(ABC):
    '''Interface for any kind of data source, comprising it's minimal set of
    methods.
    '''

    def prepare_extraction(
        self: 'SourceConnectionInterface',
        parameters: Any = None,
    ) -> dict:
        '''Prepare an extraction and return a fingerprint for further queries.

        This method shall raise an IOError if it does not succeed.

        :param parameters: a dictionary with the extraction parameters
        :type parameters: dict, optional
        :raises IOError: raised when the method does not succeed.
        :return: the extraction's fingerprint, used to getting status, execu-
        ting and cleaning
        :rtype: Any
        '''
        return parameters

    def get_status_of_extraction(
        self: 'SourceConnectionInterface',
        extraction_fingerprint: Any = None,
    ) -> Any:
        '''Return the current status of a prepared extraction using its finger-
        print.

        This method shall raise an IOError if it does not succeed.

        :param extraction_fingerprint: the ethe extraction's identifier
        :type extraction_fingerprint: Any, optional
        :raises IOError: raised when the method does not succeed.
        :return: the description of the current status of an extraction
        :rtype: Any
        '''
        return None

    def check_availability_of_extraction(
        self: 'SourceConnectionInterface',
        status: Any,
    ) -> bool:
        '''Indicate whether an extraction is ready or not according to a speci-
        fic status.

        :param status: a specific status of the extraction
        :type status: Any, optional
        :return: `True` if it's ready and `False` otherwise
        :rtype: bool
        '''
        return True

    @abstractmethod
    def execute_extraction(
        self: 'SourceConnectionInterface',
        extraction_fingerprint: Any = None,
    ) -> Any:
        '''Execute an extraction and returns a result.

        This method shall raise an IOError if it does not succeed.

        :param extraction_fingerprint: the ethe extraction's identifier
        :type extraction_fingerprint: Any, optional
        :raises IOError: raised when the method does not succeed.
        :return: the result of the extraction. It may be a list of filenames to
        which data was writing, the data itself, etc.
        :rtype: Any
        '''
        pass

    def clean_resources_of_extraction(
        self: 'SourceConnectionInterface',
        extraction_fingerprint: Any = None,
    ) -> bool:
        '''Attempt to clean resources that might have been allocated for an ex-
        traction and return this operation's success (or failure).

        This method shall raise an IOError if it does not succeed.

        :param extraction_fingerprint: the ethe extraction's identifier
        :type extraction_fingerprint: Any, optional
        :raises IOError: raised when the method does not succeed.
        :return: `True` if the resources got cleaned and `False` otherwise
        :rtype: bool
        '''
        return True
