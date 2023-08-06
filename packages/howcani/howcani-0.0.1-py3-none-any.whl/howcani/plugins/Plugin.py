'''
Contains Abstract Class to create Plugins.
'''

from abc import ABC, abstractmethod
from functools import lru_cache

from howcani.cache import cache_results

class Plugin(ABC):

    @cache_results
    def get_results(self, query, n=1):
        """
        docstring
        """
        return self._get_results(query=query, n=n)


    def _get_results(self, query:str, n=1) -> list:
        '''
        '''
        pass