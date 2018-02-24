# start imports
import numpy as np
import os, sys, inspect
import RunParams

import matplotlib.pyplot as plt

cmd_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]))
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)

cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"subfolder")))
if cmd_subfolder not in sys.path:
    sys.path.insert(0, cmd_subfolder)
# end imports


'''
Class that is mainly responsible for plotting
'''
class Plotter(object):


    '''
    Method that plots the peaks in the spectrum into file
    '''
    def plot_spectrum(self, spectrum, time_idx, frequency_idx, chan_number):
        if RunParams.Should_Plot_Peaks:
            # scatter of the peaks
            fig, ax = plt.subplots()
            ax.imshow(spectrum)
            ax.scatter(time_idx, frequency_idx)
            ax.set_xlabel('Time')
            ax.set_ylabel('Frequency')
            ax.set_title("Spectrogram_channel_" + str(chan_number))
            plt.gca().invert_yaxis()
            plt.savefig("Plots/Channel_"+str(chan_number)+".png")
            print ("    Plotting peaks for channel", chan_number, "completed.")

    def plot_fingerprints_ditribution (self, id_name, id_hash):
        return
