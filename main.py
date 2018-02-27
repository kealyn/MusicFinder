
from src import MusicFinder

import argparse,sys
import time

from argparse import RawTextHelpFormatter

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="MusicFinder: What is this song?",
        formatter_class=RawTextHelpFormatter)
    parser.add_argument('-f', '--f', nargs=1, 
        help='Fingerprint all audio files in a directory\n'
             'Usages: --f /path/to/directory [extension]\n')
    parser.add_argument('-r', '--r', action="store_true", dest="r", 
        help='Loading fingerprints and preparing for recognition')
    #parser.add_argument('-p', '--p', action="store_true", dest="p",
    #    help='Plot all fingerprints distribution.')
    args = parser.parse_args()
	
    # start timer
    t0 = time.time()

    # create a MusicFinder instance
    mf = MusicFinder()
    if args.f:
        # Fingerprint all files in a directory
        directory = args.f[0]

        if directory.lower() == "mic":
            mf.record_fingerprints_mic()
        else:
            if len(args.f) == 2:
                extension = args.f[1]
            else:
                extension = 'mp3'
            print("Fingerprinting all .%s files in the directory: %s" % (extension, directory))

        	# Fingerprint all the files with given extension in the directory
            mf.record_fingerprints_directory(directory, ["." + extension])
    elif args.r:
    	# Recognitions

        # Load all fingerprints
        mf.load_fingerprints()
        t1 = time.time()
        print ("Total time loading fingerprints: %.2f seconds." % (t1 - t0))

        while True:

            print ("-------------------------------------------------------------------------")
            print ("Choose from the following options:")
            print ("Option 1: type `print`            to print the fingerprints distribution.")
            print ("Option 2: type `mic`              to recognize a song from microphone.")
            print ("Option 3: type `path/to/the/song` to be recognized.")
            print ("Option 4: type `exit`             to exit the program.")
            print ("-------------------------------------------------------------------------")
            file_name = input ("\nYour input:")
            if file_name.lower() == "exit":
                break
            if file_name.lower() == "print":
                # Plot fingerprints distribution
                mf.plot_all_fingerprints()
                continue

            time_limit = input ("Please give a limit of time (in seconds): ")

            #file_name = args.r[0]
            #file_name = "Audios/Yesterday Once More.mp3"

            try:

                time_limit = int(time_limit)
                t2 = time.time()
                
                # Find best match
                song_name = mf.recognize_file(file_name,time_limit)
                
                t3 = time.time()

                # Display song name
                print ("Best match:", song_name, "\nTotal matching time: %.2f seconds" % (t3 - t2))
            except Exception as e:
                print ("Matching failed due to the following exception: ")
                print (e)

        	

    end = time.time()
    print ("Total time elapsed %.2f seconds." % (end - t0))
    sys.exit(0)

    
	#mf.record_fingerprints_directory("Audios", [".mp3"])

	#song_name = mf.recognize("Audios/Yesterday Once More.mp3")
