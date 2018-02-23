import numpy as np
from FFT import FFT
import matplotlib.pyplot as plt
import math
import hashlib
import RunParams
import scipy.ndimage.filters as filters
import scipy.ndimage.morphology as morphology

'''
Class that is responsible for computing finger prints from the channel samples
'''
class FingerPrinter:

    '''
    Constructor
    '''
    def __init__(self):
        self.FFT = FFT()
		
    '''
    FFT the channel, log transform output, find local maxima, then return
    locally sensitive hashes.
    '''
    def fingerprint(self, chan_number, channel_samples, fs):
        # ToDo: To be completed
            # Step 1: FFT the signal and extract frequency components
        spectrum = self.FFT.run(channel_samples, fs)
		
        # Step 2: Find peak points
        # find local maxima as peak points
        peaks, time_idx, frequency_idx = self.get_peaks_above_threshold(spectrum, threshold=RunParams.Default_Peak_Threshold)

        # Plot the peaks (when flag is set to True)
        self.plot_spectrum(spectrum, time_idx, frequency_idx, chan_number)

        # Step 3: Compute hashes
        return self.generate_hashes(peaks)

    '''
    Method that identifies and returns the peak points from a given spectrum.
    It treats the spectrogram as an image and uses the high pass filter from
    image processing toolkit in scipy.
    '''
    def get_peaks_above_threshold(self, spectrum, threshold):
        
        print ("    Finding peaks...")
        # Generate a binary structure for binary morphological operations.
        struct = morphology.generate_binary_structure(2, 1)
        neighborhood = morphology.iterate_structure(struct, RunParams.Default_Peak_Neighborhood_Size)

        # find peaks using maximum filter
        peaks = filters.maximum_filter(spectrum, footprint=neighborhood) == spectrum
        background = (spectrum == 0)
        eroded_background = morphology.binary_erosion(background, structure=neighborhood, border_value=1)

        # Boolean mask of spectrum with True at peaks
        peaks = peaks - eroded_background

        print ("    Peaks extrated.")

        # extract peaks
        peaks_extracted = spectrum[peaks]
        j, i = np.where(peaks)

        # create a list of tuple (freq, time, amp)
        p = zip(i, j, peaks_extracted.flatten())
        peaks_filtered = [x for x in p if x[2] > threshold]

        print ("    Number of peaks:", len(peaks_filtered))
        # get indices for frequency and time
        frequency_idx = [x[1] for x in peaks_filtered]
        time_idx      = [x[0] for x in peaks_filtered]

        return peaks_filtered, time_idx, frequency_idx

    '''
    Method that plots the peaks in the spectrum into file
    '''
    def plot_spectrum(self, spectrum, time_idx, frequency_idx, chan_number):
        if RunParams.Should_Plot_Peaks:
            print ("    Plotting peaks for channel ", chan_number)
            # scatter of the peaks
            fig, ax = plt.subplots()
            ax.imshow(spectrum)
            ax.scatter(time_idx, frequency_idx)
            ax.set_xlabel('Time')
            ax.set_ylabel('Frequency')
            ax.set_title("Spectrogram_channel_" + str(chan_number))
            plt.gca().invert_yaxis()
            plt.savefig("Plots/Channel_"+str(chan_number)+".png")

    '''
    Method that generates hash values for each peak point with a time offset.
    The algorithm to generate the hash is as shown in 
        https://github.com/kealyn/MusicFinder

    Returns:
      - List structure of (hash, offset).
    '''
    def generate_hashes(self, peaks):
        for i in range(len(peaks)):
            freq1 = peaks[i][0]
            t1 = peaks[i][1]
            t_delta = 0
            freq_delta = 0
            for j in range(1, RunParams.Default_Target_Area):
                if (i + j) < len(peaks):
                    freq2 = peaks[i + j][0]
                    t2 = peaks[i + j][1]
                    t_delta += t2 - t1
                    freq_delta += math.fabs(freq2 - freq1)

                # Filter time and frequency difference within a reasonable range
                # TODO: calibration may be needed
                # 5000 hz of freq difference
                # 10 ms of time difference
                if freq_delta > 0 and freq_delta <= 5000 and t_delta > 0 and t_delta <= 441:         
                    line = "%s|%s|%s" % (str(freq1), str(freq_delta), str(t_delta))
                    h = hashlib.sha1(line.encode('utf-8'))
                    yield (h.hexdigest(), t1)
