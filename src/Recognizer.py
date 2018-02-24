# start imports
import numpy as np
import os, sys, inspect

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
    Test function
    '''
    def find_match(self, original_hash, new_hash):
        
        # Conver the original hash into dictionary
        mapper = {}
        for h, offset in original_hash:
            mapper[h] = offset

        return self.find_match_from_mapping(new_hash, mapper)


    def find_match_from_mapping(self, new_hash, mapper):
        
        res = 0

        # Find matches
        for newh, _ in new_hash:
            if newh in mapper:
                res += 1

        return res

    def find_song_name(self, new_hash):

        max_count = 0
        best_song_id = -1
        for song_id, original_hash_mapping in self.song_id_hash_mapping.items():
            cur_count = self.find_match_from_mapping(new_hash, original_hash_mapping)
            print (self.song_id_name_mapping[song_id], "matching:", cur_count)
            if cur_count > max_count:
                max_count = cur_count
                best_song_id = song_id
                

        if best_song_id != -1:
            return self.song_id_name_mapping[best_song_id]
        else:
            return "No match."
