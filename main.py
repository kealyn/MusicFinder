
from src import MusicFinder

import argparse,sys
import time

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="MusicFinder: What is this song?")
    parser.add_argument('-f', '--f', nargs='*', 
        help='Fingerprint all audio files in a directory\n'
             'Usages:\n'
             '--f /path/to/directory [extension]\n')
    parser.add_argument('-r', '--r', action="store_true", dest="r", 
        help='Loading fingerprints and preparing for recognition')
    parser.add_argument('-p', '--p', action="store_true", dest="p",
        help='Plot all fingerprints distribution.')
    args = parser.parse_args()
	
    # start timer
    t0 = time.time()

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

        # Load all fingerprints
        mf.load_fingerprints()
        t1 = time.time()
        print ("Total time loading fingerprints: %.2f seconds." % (t1 - t0))

        while True:
            file_name = input ("\nPlease type the path of the song to be recognized (or type exit): ")
            if file_name.lower() == "exit":
                break

            #file_name = args.r[0]
            #file_name = "Audios/Yesterday Once More.mp3"

            try:
                t2 = time.time()
                
                # Find best match
                song_name = mf.recognize_file(file_name)
                
                t3 = time.time()
                
                # Display song name
                print ("Best match:", song_name, "total matching time: %.2f seconds" % (t3 - t2))
            except Exception as e:
                print ("Matching failed due to the following exception: ")
                print (e)

        	
    elif args.p:
        # Plot fingerprints distribution

        # Load all fingerprints
        mf.load_fingerprints()
        mf.plot_all_fingerprints()


    end = time.time()
    print ("Total time elapsed %.2f seconds." % (end - t0))
    sys.exit(0)

    
	#mf.record_fingerprints_directory("Audios", [".mp3"])

	#song_name = mf.recognize("Audios/Yesterday Once More.mp3")
