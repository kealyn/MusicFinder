
import os
import sys
import time

import src.RunParams as RunParams
import src.Decoder as Decoder
import src.FingerPrinter as FingerPrinter
import src.Recognizer as Recognizer
import src.HashingManager as HashingManager
import src.Plotter as Plotter
import src.MicRecorder as MicRecorder

'''
Class body for MusicFinder. It defines the constructor and member functions.
'''
class MusicFinder(object):

    '''
    Constructor
    '''
    def __init__(self):
        self.limit = -1
        self.fingerprint_loaded = False
        self.Decoder = Decoder.Decoder()
        self.FingerPrinter = FingerPrinter.FingerPrinter()
        self.Recognizer = Recognizer.Recognizer()
        self.HashingManager = HashingManager.HashingManager()
        self.Plotter = Plotter.Plotter()
        self.MicRecorder = MicRecorder.MicRecorder()

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

            # Find song name and extension
            song_name, extension = os.path.splitext(os.path.basename(file_name))
            print ("(%d/%d) Processing file %s" % (file_id, len(filenames_to_fingerprint), song_name))

            hashes = self.record(file_name, RunParams.Default_Audio_Limit)
            count += len(hashes)
            print ("Step 3: Writing hash values to file ...")

            self.HashingManager.dump_to_file(file_id, song_name, hashes)

            print ("  "+ str(count) +" hash values have been written")

            file_id += 1



    '''
    Function that triggers the recording of the fingerprints for the given file
    '''
    def record(self, filename, limit=-1):

        # Read channel samples and frame rate from the file
        print ("Step 1: Reading data from file", filename, "with limit =", limit)
        channels, fs = self.Decoder.read(filename, limit)

        # Rashing result
        res_hash = set()
        channel_count = len(channels)

        print ("Step 2: Encoding channel data")
        for number, channel in enumerate(channels):
            print("  Channel %d/%d started..." % (number+1, channel_count))
            hashings_cur_channel, spectrum, time_idx, frequency_idx, chan_number \
                = self.FingerPrinter.fingerprint(number+1, channel, fs=fs)
            # Plot the peaks (when flag is set to True)
            self.Plotter.plot_spectrum(spectrum, time_idx, frequency_idx, chan_number)
            print("  Channel %d/%d completed." % (number+1, channel_count))
            res_hash |= set(hashings_cur_channel)

        print ("Hash count:", len(res_hash))
        return res_hash

    '''
    Function that loads the fingerprints from designated csv file
    '''
    def load_fingerprints(self, csv_file_name = RunParams.Default_Hash_File_Name):
        self.id_name, self.id_hash = self.HashingManager.read_from_file(csv_file_name)
        self.Recognizer.initialize_fingerprints_library(self.id_name, self.id_hash)
        self.name_hash_count = self.compute_song_id_hash_count_mapping(self.id_name, self.id_hash)
        self.fingerprint_loaded = True

        for name, count in self.name_hash_count.items():
            print (name, ": ", count)
        print ("Fingerprints library loaded.")

    '''
    Method that plots the distribution of the provided fingerprints

    Params:
      - id_name: mapping of {song_id, song_name}
      - id_hash_fingerprints: mapping of {song_id, {hash, offset}}

    Returns:
      - name_hash_count: mapping of {song_name, hash_count}
    '''
    def compute_song_id_hash_count_mapping(self, id_name, id_hash_fingerprints):
        # Convert to a mapping of {song_name, number of hash values}
        name_hash_count = {}
        for song_id, original_hash_mapping in id_hash_fingerprints.items():
            name_hash_count[id_name[song_id]] = len(original_hash_mapping)
        return name_hash_count

    '''
    API function that plots the distribution of all loaded fingerpritns
    '''
    def plot_all_fingerprints(self):
        if not self.fingerprint_loaded:
            self.load_fingerprints()
        self.Plotter.plot_fingerprints_ditribution(self.name_hash_count)


    '''
    Method that recognizes the given music file and return the name of the song 
    that is the best match from the library
    '''
    def recognize_file(self, file_name, time_limit=-1):

        if not self.fingerprint_loaded:
            self.load_fingerprints()

        t1 = time.time()
        if (file_name.lower() == "mic"):
            # Take input from microphone
            data = self.MicRecorder.get_recording(time_limit)

            new_hash = set()
            for samples in data:
                cur_hash, spectrum, time_idx, frequency_idx, chan_number \
                    = self.FingerPrinter.fingerprint(1, samples, RunParams.Default_Frequency_Rate)
                new_hash |= set(cur_hash)
                
            print ("Hash count:", len(new_hash))
        else:

            song_name, extension = os.path.splitext(os.path.basename(file_name))

            # Convert given music to hash
            new_hash = self.record(file_name, time_limit)

        t2 = time.time()
        print ("Encoding time in seconds: %.2f" % (t2 - t1))

        # Find the best match of given the new hashing
        song_name, candidates = self.Recognizer.find_song_name(new_hash)
        t3 = time.time()
        print ("Matching time in seconds: %.2f" % (t3 - t2))

        # Plot the candidates distribution
        self.Plotter.plot_candidates(song_name, len(new_hash), candidates)

        return song_name

