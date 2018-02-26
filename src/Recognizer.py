# start imports
import numpy as np
import os, sys, inspect
import RunParams
import AbstractRecognizer
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
    def find_match(self, original_hash_set, new_hash_list):
        
        # Conver the original hash into dictionary
        mapper = {}
        for h, offset in original_hash_set:
            mapper[h] = offset

        return self.find_match_from_mapping(new_hash_list, mapper)

    '''
    Method that counts the number of matchings of the hash values between the 
    new hash set and the mapper library
    '''
    def find_match_from_mapping(self, new_hash_list, mapper):
        
        res = 0

        # Find matches
        for newh, _ in new_hash_list:
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
    def find_song_name(self, new_hash_list):

        max_count = 0
        best_song_id = -1
        candidates = {}
        for song_id, original_hash_mapping in self.song_id_hash_mapping.items():
            cur_count = self.find_match_from_mapping(new_hash_list, original_hash_mapping)
            #print (self.song_id_name_mapping[song_id], "matching:", cur_count)
            if cur_count > max_count:
                max_count = cur_count
                best_song_id = song_id
                candidates[self.song_id_name_mapping[best_song_id]] = cur_count
                
        print ("Matching hashes:", max_count)
        print ("Prior Candidates are:")
        print (candidates)

        # Post processing to filter out the candidates that are not qualified
        candidates = dict((k, v) for k, v in candidates.items() \
            if v >= max_count * RunParams.Default_Candidate_Threshold_In_Percentage)

        print ("Post Candidates are:")
        print (candidates)

        aligned = True
        if len(candidates) > 1:
            # Alignment of fingerprints
            best_match_hash_set = self.song_id_hash_mapping[best_song_id]
            new_hash_set = self.list_to_dict(new_hash_list)
            aligned = self.are_fingerprints_aligned(best_match_hash_set, new_hash_set)

        if best_song_id != -1:
            if aligned:
                return self.song_id_name_mapping[best_song_id], candidates
            else:
                print ("Fingerprints not aligned.")
                return "No match.", candidates
        else:
            return "No match.", candidates


    '''
    Method the decides wether the given two set of hashes align with each other
    w.r.t. time offsets
    '''
    def are_fingerprints_aligned(self, best_match_hash_set, new_hash_set):

        count = 0
        t_count = 0
        # Traverse 
        prev_new = 0
        prev_best = 0
        for k, v in new_hash_set.items():
            if k in best_match_hash_set:
                cur_new = v
                cur_best = best_match_hash_set[k]
                if (cur_new - prev_new == cur_best - prev_best):
                    count += 1
                prev_new = cur_new
                prev_best = cur_best
                t_count += 1

        return count > t_count * RunParams.Default_Alignment_Ratio

    '''
    utility method that helps convert a list of key-value pairs to a dictionary
    '''
    def list_to_dict(self, li):  
        d = {}
        for k,v in li:
            d[k] = v
        return d


