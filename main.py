
from src import MusicFinder

import argparse,sys
import time

if __name__ == '__main__':

    start = time.time()
    parser = argparse.ArgumentParser(description="MusicFinder: What is this song?")
    parser.add_argument('-f', '--f', nargs='*', 
        help='Fingerprint all audio files in a directory\n'
             'Usages:\n'
             '--f /path/to/directory [extension]\n')
    parser.add_argument('-r', '--r', nargs=1, 
        help='Recognize given music file\n'
             'Usage:\n'
             '--r "/path/to/file" \n')
    parser.add_argument('-p', '--p', action="store_true", dest="p",
        help='Plot all fingerprints distribution.')
    args = parser.parse_args()
	
    # create a MusicFinder instance
    mf = MusicFinder()
    if args.f:
        # Fingerprint all files in a directory
        directory = args.f[0]

        if len(args.f) == 2:
            extension = args.f[1]
        else:
            extension = 'mp3'
        print("Fingerprinting all .%s files in the directory: %s" % (extension, directory))

    	# Fingerprint all the files with given extension in the directory
        mf.record_fingerprints_directory(directory, ["." + extension])
    elif args.r:
    	# Recognitions
        #file_name = args.r[0]
        file_name = "Audios/Yesterday Once More.mp3"

    	# Load all fingerprints
        mf.load_fingerprints()

    	# Find best match
        song_name = mf.recognize_file(file_name)

    	# Display song name
        print ("Best match:", song_name)
    elif args.p:
        # Plot fingerprints distribution

        # Load all fingerprints
        mf.load_fingerprints()
        mf.plot_all_fingerprints()


    end = time.time()
    print ("Total time elapsed", (end - start), "seconds.")
    sys.exit(0)

    
	#mf.record_fingerprints_directory("Audios", [".mp3"])

	#song_name = mf.recognize("Audios/Yesterday Once More.mp3")
