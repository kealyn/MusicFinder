# start imports
import numpy as np
import os, sys, inspect
import RunParams

cmd_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]))
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)

cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"subfolder")))
if cmd_subfolder not in sys.path:
    sys.path.insert(0, cmd_subfolder)
# end imports


'''
Class that is mainly responsible for recognizing an audio file
'''
class Recognizer(object):

    def initialize_fingerprints_library(self, id_name, id_hash):
        self.song_id_name_mapping = id_name
        self.song_id_hash_mapping = id_hash

    '''
    Unit test function
    '''
    def find_match(self, original_hash_set, new_hash_set):
        
        # Conver the original hash into dictionary
        mapper = {}
        for h, offset in original_hash_set:
            mapper[h] = offset

        return self.find_match_from_mapping(new_hash_set, mapper)

    '''
    Method that counts the number of matchings of the hash values between the 
    new hash set and the mapper library
    '''
    def find_match_from_mapping(self, new_hash_set, mapper):
        
        res = 0

        # Find matches
        for newh, _ in new_hash_set:
            if newh in mapper:
                res += 1

        return res

    '''
    Method that tries to match the provided the hash set with the library
    and returns the name of the song with best match

    Returns:
      - Song name of the best match
      - All candidates that may match the given song. {song_name, matching_count}
    '''
    def find_song_name(self, new_hash_set):

        max_count = 0
        best_song_id = -1
        candidates = {}
        for song_id, original_hash_mapping in self.song_id_hash_mapping.items():
            cur_count = self.find_match_from_mapping(new_hash_set, original_hash_mapping)
            #print (self.song_id_name_mapping[song_id], "matching:", cur_count)
            if cur_count > max_count:
                max_count = cur_count
                best_song_id = song_id
                candidates[self.song_id_name_mapping[best_song_id]] = cur_count
                
        # Post processing to filter out the candidates that are not qualified
        candidates = dict((k, v) for k, v in candidates.items() \
            if v >= max_count * RunParams.Default_Candidate_Threshold_In_Percentage)

        if best_song_id != -1:
            return self.song_id_name_mapping[best_song_id], candidates
        else:
            return "No match.", candidates
