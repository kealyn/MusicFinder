
import os
import sys
import src.RunParams as RunParams
import src.Decoder as Decoder
import src.FingerPrinter as FingerPrinter
import src.Recognizer as Recognizer
import src.HashingManager as HashingManager

'''
Class body for MusicFinder. It defines the constructor and member functions.
'''
class MusicFinder(object):

    '''
    Constructor
    '''
    def __init__(self):
        self.limit = -1
        self.Decoder = Decoder.Decoder()
        self.FingerPrinter = FingerPrinter.FingerPrinter()
        self.Recognizer = Recognizer.Recognizer()
        self.HashingManager = HashingManager.HashingManager()

    '''
    Function that records fingerprints of all files with given extension in the given path
    '''
    def record_fingerprints_directory(self, path, extensions):
        filenames_to_fingerprint = []
        for filename, _ in self.Decoder.find_files_in_path(path, extensions):
            filenames_to_fingerprint.append(filename)

        print ("Recording fingerprints from [", path, "] for all extensions: ", extensions)
        print ("Files to process (total: ", len(filenames_to_fingerprint), ")")
        print ("---------------------------------------------------------")
        print ("\n".join(filenames_to_fingerprint))
        print ("---------------------------------------------------------")

        # Process audio files
        # TODO: This process can be optimized by processing multiple files in parallel
        file_id = 1
        count = 0
        for file_name in filenames_to_fingerprint:
            hashes = self.record(file_name, RunParams.Default_Audio_Limit)
            count += len(hashes)
            print ("Step 3: Writing hash values to file ...")

            # Find song name and extension
            song_name, extension = os.path.splitext(os.path.basename(filename))
            self.HashingManager.dump_to_file(file_id, song_name, hashes)

            print ("  "+ str(count) +" hash values have been written")

            file_id += 1



    '''
    Function that triggers the recording of the fingerprints for the given file
    '''
    def record(self, filename, limit=-1):

        # Read channel samples and frame rate from the file
        print ("Step 1: Reading data from file ", filename, "with limit = ", limit)
        channels, fs = self.Decoder.read(filename, limit)

        # Rashing result
        res_hash = set()
        channel_count = len(channels)

        print ("Step 2: Encoding channel data")
        for number, channel in enumerate(channels):
            print("  Channel %d/%d started..." % (number+1, channel_count))
            hashings_cur_channel = self.FingerPrinter.fingerprint(number+1, channel, fs=fs)
            print("  Channel %d/%d completed." % (number+1, channel_count))
            res_hash |= set(hashings_cur_channel)

        return res_hash

    '''
    Function that loads the fingerprints from designated csv file
    '''
    def load_fingerprints(self, csv_file_name = RunParams.Default_Hash_File_Name):
        id_name, id_hash = self.fingerprints = self.HashingManager.read_from_file(csv_file_name)



