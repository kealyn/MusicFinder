# MusicFinder
Imagine that you are at a coffee shop, writing code and enjoying the afternoon with a beautiful melody playing in the background. You started wondering: what is this song? It sounds familiar, but you cannot recall the name. We know that Siri and Google Assistant are able to identify a music within half a minute, but how does it work?

Inspired by dejavu project, here I build and present the workflow of MusicFinder v1.

## Music fingerprinting

### FFT: from time domain to frequency domain

As a first step, we need to extract useful information from the music that could help identify it. For this purpose, we take help from [Fast Fourier Transform](https://en.wikipedia.org/wiki/Fast_Fourier_transform). 
FFT is an algorithm that samples a signal over a period of time (or space) and divides it into its frequency components. By transforming the music from time domain to frequency domain, we will have a unified representation of different musics
on the same scale.

Following is a picture ([spectrogram](https://en.wikipedia.org/wiki/Spectrogram)) for the song *Yesterday Once More* in frequency domain. 

<img src="https://github.com/kealyn/MusicFinder/blob/master/Figures/Spectro_Original.png" width="600">

The x-axis represents the sampling over time for the song. As per [Nyquist–Shannon sampling theorem](https://en.wikipedia.org/wiki/Nyquist%E2%80%93Shannon_sampling_theorem), we need a sampling rate of 44,100 Hz to avoid frequency loss. The y-axis represents the range of frequencies. The FFT shows us the strength, i.e. amplitude, of the signal at that particular frequency. As shown in the picture, the frequency and time values are discretized, while the amplitudes are continuous. Brighter color indicates higher amplitude.

### Fingerprints

After converting to spectrogram, the question is how to identify this song uniquely from a certain distribution or patterns. Moreover, our recognition step needs to survive in a noisy environment, requiring that this distribution to be robust and not sensitive to small interferences.

The process of [Acoustic Fingerprint](https://en.wikipedia.org/wiki/Acoustic_fingerprint) fits perfectly to our needs. If two files sound alike to the human ear, their acoustic fingerprints should match, even if their binary representations are quite different. Essentially, the fingerprints should differ from hash functions, which must be sensitive to any small changes in the data.

In the case of [Shazam](https://www.shazam.com/), their algorithm then picks out points where there are peaks in the graph, labeled as "higher energy content". In practice, this seems to work out to about three points per song [1]. Focusing on peaks in the audio greatly reduces the impact that background noise has on audio identification. 

### Shazam algorithm

To understand the algorithm behind the scene, we look at the following example:

<img src="https://github.com/kealyn/MusicFinder/blob/master/Figures/Shazam.png" width="1000">


Notice that the darker spots ("peaks") in Fig. 1A match the crosses in the Fig. 1B. To efficiently store and search for a match, they choose some of the peak points from within the simplified spectrogram (called "anchor points") and zones in the vicinity of them (called "target zone" in Fig. 1C). Now, for each point in the target zone, a hash that will be the aggregation of the following: the frequency at which the anchor point is located (`f1`) + the frequency at which the point in the target zone is located (`f2`)+ the time difference between the time when the point in the target zone is located in the song (`t2`) and the time when the anchor point is located in the song (`t1`) + `t1`. [2]

To simplify:

```
fingerprint hash value = F(frequencies of peaks, time difference between peaks) = (f1+f2+(t2-t1))+t1
```
illustrated in the above figure (Fig. 1D). Note that there are lots of different ways to do this, Shazam has their own, SoundHound another, and so on. The point is that by taking into account more than a single peak's values can create fingerprints that have more entropy and have less hash collision. 

In the MusicFinder project, we will employ a variation of Shazam algorithm. For each peak point *p*, we will identify *k* nearest anchors (`a_i, i = 1,..,k`) in time incremental order with a threshold *T* in frequency domain, and then we use the following formula to compute the hash value for this peak

<img src="http://latex.codecogs.com/gif.latex?Hash(p)=\{f(p)+\sum_{i=1}^{k}[|f(a_i)%20-%20f(p)|+|t(a_i)%20-%20t(p)|]\%20\Bigg|%20\%20|t(a_i)%20-%20t(p)|%20%3C%20T\}">

where *t(p)* represents the time value of point *p* while *f(p)* represents the frequency value of *p*. [This heuristic is to be tested and is subject to change in the following week.]

## Identifying peaks and anchors

We have covered the part that how to compute the hash values for peak points, but wait, where did you get these peaks and anchors? Taking one step back, identifying peak points is totally a different (and interesting) problem.

[to be written]



## Storing the fingerprints

The above-mentioned combinatorial hashing leads to a good amount of hash values: a hash value for each peak point.

[to be written]

However, hash values by themselves are not enough to identify a specific rhythm, we need to store the correct order of them.



## Recognition

[to be written]


## Performance

[to be written, original song vs microphone vs additive noise]


## Enhancements

- **"Pseudo" voice recognition:** Add audio samples of words, phrases, and sentences so that MF could also identify certain commands, such as "turn on the TV". 
- **Voice recognition:** The voice recognition mentioned in the above point is very limited and cannot process natural languages. For example, MF will not find the similarities between "turn off the computer" and "could you please shut down the computer". To make MF equip with voice recognition, neural network models need to be integrated and properly trained.
- **Emotional detector:** If the audio files are labeled with auxiliary information, MF can be used to find the appropriate label for the new sample with the help of a probability model. For example, with emotional labels for different voices, such as angry, excited, sad, etc., MF could perform as an `emotional detector` that suggests the likelihood of the given sample being recorded with a angry emotion, or happy emotion.



## Reference
[1] Surdu, Nicolae (January 20, 2011). "How does Shazam work to recognize a song?". Archived from the original on 2016-10-24. Retrieved 12 February 2018.

[2]  Li-Chun Wang, Avery. "An Industrial-Strength Audio Search Algorithm." Columbia University. Web. 1 Dec. 2014.
