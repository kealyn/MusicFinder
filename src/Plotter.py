# start imports
import numpy as np
import os, sys, inspect
import RunParams

from matplotlib.font_manager import FontManager
import matplotlib.pyplot as plt

from pylab import mpl
import subprocess
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

    '''
    Method that plots the distribution of the provided fingerprints

    Params:
      - id_name: mapping of {song_id, song_name}
      - id_hash_fingerprints: mapping of {song_id, {hash, offset}}
    '''
    def plot_fingerprints_ditribution (self, id_name, id_hash_fingerprints):

        if not id_name or not id_hash_fingerprints:
            print ("No fingerprints to be plot!")
            return

        print ("Plotting distribution of fingerprints...")


        #

        # Convert to a mapping of {song_name, number of hash values}
        name_hash_count = {}
        for song_id, original_hash_mapping in id_hash_fingerprints.items():
            name_hash_count[id_name[song_id]] = len(original_hash_mapping)

        # Prepare data for plot
        keys = list(name_hash_count.keys())
        values = list(name_hash_count.values())
        #zipped = zip(keys, values)
        #sorted(zipped, key=lambda x: x[1])

        names = [x for _,x in sorted(zip(values,keys))]
        counts = sorted(values)
        
        # position of bar
        bar_width = 10
        y_pos = np.arange(len(names)) * (bar_width + 1)
        counts = np.array(counts)

        mask1 = counts < 20000
        mask2 = counts >= 20000

        plt.rcParams["figure.figsize"] = [10,30]
        plt.rcParams.update({'font.size': 32})
        plt.rc('font', family='Microsoft YaHei')
        plt.barh(y_pos[mask1], counts[mask1], color = 'blue', height=bar_width, align='center')
        plt.barh(y_pos[mask2], counts[mask2], color = 'purple', height=bar_width, align='center')

        # Plot distribution
        #plt.barh(y_pos, counts, height=bar_width, align='center')
        plt.yticks(y_pos, names,rotation=45, size=8)
        plt.xlabel('Number of fingerprints')
        plt.title('Distribution of fingerprints')
        plt.subplots_adjust(left=0.2, top=0.8)
        plt.savefig("Plots/Fingerprints_distribtion.png", dpi = 400, bbox_inches='tight')

        return
