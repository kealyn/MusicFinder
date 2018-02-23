# start imports
import numpy as np
import os, sys, inspect
import RunParams
import pandas as pd
from numpy import genfromtxt
cmd_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]))
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)

cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"subfolder")))
if cmd_subfolder not in sys.path:
    sys.path.insert(0, cmd_subfolder)
# end imports

# Constants
FILE_ID = 'FileId'
FILE_NAME = 'FileName'
HASHVALUE = 'HashValue'
OFFSET = 'Offset'

'''
Class that is mainly responsible for organizing and storing hash values
'''
class HashingManager(object):

    '''
    Method that dumps hash values along with music metadata into file
    '''
    def dump_to_file(self, file_id, file_name, hashes):

        # Create the hashlist by appending metadata to each (hash, offset) pair
        # TODO: remove this redundant information by using separate files or database
        hashlist = []
        for h,t in hashes:
            hashlist.append((file_id, file_name, h, t))

        # Data frame created with the hash list
        df = pd.DataFrame(hashlist, columns=[FILE_ID, FILE_NAME, HASHVALUE, OFFSET])

        # Dump to csv file
        df.to_csv(RunParams.Default_Hash_File_Name, mode='a', sep=',', encoding='utf-8', index=False)

    '''
    Method that loads hash values along with music metadata from file
    '''
    def read_from_file(self, file_name):
        df = pd.read_csv(file_name, header=0)

        #print (df.head(20))

        song_id_name_mapping = {}
        song_id_hash_mapping = {}
        for _, row in df.iterrows():

            song_id = row[FILE_ID]

            # Create a song_id and song_name mapping
            song_id_name_mapping[song_id] = row[FILE_NAME]

            # Convert flat hash info into dictionary
            # Key1  : song id
            # Value1: dictionary of [hash, offset]
            #   Key2  : hash
            #   Value2: time offset of that hash
            if song_id not in song_id_hash_mapping:
                song_id_hash_mapping[song_id] = {}
            song_id_hash_mapping[song_id][row[HASHVALUE]] = row[OFFSET]

        return song_id_name_mapping, song_id_hash_mapping









        
