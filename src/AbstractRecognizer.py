# start imports
import os, sys, inspect
from abc import ABC, abstractmethod
# end imports


'''
Base class of recognizer
'''
class AbstractRecognizer(ABC):

    '''
    Method that tries to match the provided the hash set with the library
    and returns the name of the song with best match

    Returns:
      - Song name of the best match
      - All candidates that may match the given song. {song_name, matching_count}
    '''
    @abstractmethod
    def find_song_name(self, new_hash_list):
        pass

