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

    '''
    Test function
    '''
    def find_match(self, original_hash, new_hash):
        
        res = 0

        # Conver the original hash into dictionary
        mapper = {}
        for h, offset in original_hash:
            mapper[h] = offset

        # Find matches
        for newh, _ in new_hash:
            if newh in mapper:
                res += 1

        return res

