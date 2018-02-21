
from src import MusicFinder

if __name__ == '__main__':

    # create a MusicFinder instance
	mf = MusicFinder()

    # Fingerprint all the files with given extension in the directory
	mf.record_fingerprints_directory("Audios", [".mp3"])
