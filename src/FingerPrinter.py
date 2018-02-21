import numpy as np
from FFT import FFT

'''
Class that is responsible for computing finger prints from the channel samples
'''
class FingerPrinter:

    '''
    Constructor
    '''
    def __init__(self):
        self.FFT = FFT.FFT()
		
	'''
	FFT the channel, log transform output, find local maxima, then return
	locally sensitive hashes.
	'''
	def fingerprint(self, channel_samples, fs):
	    # ToDo: To be completed
            # Step 1: FFT the signal and extract frequency components
	    spectrum = self.FFT.run(channel_samples, fs)
		
	    # Step 2: Find peak points
		
	    # Step 3: Compute hashes
		
	    # return hashes

