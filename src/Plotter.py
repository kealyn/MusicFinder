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
    '''
    def plot_fingerprints_ditribution (self, name_hash_count):

        if not name_hash_count:
            print ("No fingerprints to be plot!")
            return

        print ("Plotting distribution of fingerprints...")

        # Prepare data for plot
        keys = list(name_hash_count.keys())
        values = list(name_hash_count.values())

        # Sort based on values
        names = [x for _,x in sorted(zip(values,keys))]
        counts = sorted(values)
        
        # position of bar
        bar_width = 10
        y_pos = np.arange(len(names)) * (bar_width + 1)
        counts = np.array(counts)

        mask1 = counts < 60000
        mask2 = counts >= 60000

        plt.rcParams["figure.figsize"] = [10,30]
        plt.rcParams.update({'font.size': 18})
        plt.rc('font', family='Microsoft YaHei')
        plt.barh(y_pos[mask1], counts[mask1], color = 'blue', height=bar_width, align='center')
        plt.barh(y_pos[mask2], counts[mask2], color = 'purple', height=bar_width, align='center')

        # Plot distribution
        plt.yticks(y_pos, names,rotation=45, size=8)
        plt.xlabel('Number of fingerprints')
        plt.grid(color='gray', linestyle='dashed')
        plt.title('Fig. 4. Distribution of fingerprints across songs')
        plt.subplots_adjust(left=0.2, top=0.8)
        plt.savefig("Plots/Fingerprints_distribtion.png", dpi = 400, bbox_inches='tight')

        print ("Plotting saved to Plots/Fingerprints_distribtion.png")
        return

    '''
    Method that plots the distribution of candidates w.r.t. the given file
    '''
    def plot_candidates(self, song_name, num_hash_original, orig_candidates):

        # Convert values to confidence
        orig_values = list(orig_candidates.values())
        total_sum = sum(orig_values)

        candidates = {k: (v / total_sum * 100) for k, v in orig_candidates.items()}

        # Prepare data for plot
        keys = list(candidates.keys())
        values = list(candidates.values())

        # Sort based on values
        names = [x for _,x in sorted(zip(values,keys), reverse=True)]
        counts = sorted(values, reverse=True)

        # position of bar
        bar_width = 4
        y_pos = np.arange(len(names)) * (bar_width + 1)
        counts = np.array(counts)

        mask1 = counts < num_hash_original * 0.5
        mask2 = counts >= num_hash_original * 0.5

        plt.rcParams["figure.figsize"] = [16,9]
        plt.rcParams.update({'font.size': 18})
        plt.rc('font', family='Microsoft YaHei')
        plt.bar(y_pos[mask1], counts[mask1], color = 'darkgreen', width=bar_width, align='center')
        plt.bar(y_pos[mask2], counts[mask2], color = 'firebrick', width=bar_width, align='center')

        # Plot distribution
        plt.xticks(y_pos, names,rotation=45, size=14)
        plt.ylabel('Matching hashes')
        plt.title('Candidate songs')
        plt.subplots_adjust(bottom=0.2, top=0.8)
        plt.savefig("Plots/"+song_name+"_candidates.png", dpi = 400, bbox_inches='tight')
        #plt.show()

        return












