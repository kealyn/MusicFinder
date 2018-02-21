import matplotlib.mlab as mlab
import RunParams
import numpy as np

'''
Class that is responsible for Fast Fourier Transformation
'''
class FFT:

    '''
    Method that performes FFT on the channel samples with given parameters.
    '''
    def run(self, channel_samples, fs=RunParams.Default_Frequency_Rate, width=RunParams.Default_Width_FFT, overlap_ratio=RunParams.Default_Overlap_Ratio):
		
        # Perform FFT with mlab.specgram and retrieve the spectrum (columns: times, rows: frequencies)
        # NFFT     : The number of data points used in each block for the FFT.
        # Fs       : The sampling frequency (samples per time unit).
        # window   : A function or a vector of length NFFT.
        # noverlap : The number of points of overlap between blocks.
        (spectrum, freqs, t) = mlab.specgram(channel_samples, NFFT=width, Fs=fs, window=mlab.window_hanning, noverlap=int(width * overlap_ratio))
		
        # Transform to log scale
        Z = 10. * np.log10(spectrum)
		
	# replace infs with zeros
	Z[Z == -np.inf] = 0 
		
	return Z
