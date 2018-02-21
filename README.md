# MusicFinder
Imagine that you are at a coffee shop, writing code and enjoying the afternoon with a beautiful melody is playing in the background. You start wondering: what is this song? It sounds familiar. We know that Siri and Google Assistant are able to identify a music within half a minute, but how does it work?

Inspired by dejavu project, here I build and present the workflow of MusicFinder v1.

## Music fingerprinting

### FFT: from time domain to frequency domain

As a first step, we need to extract useful information from the music that could help identify it. For this purpose, we take help from [Fast Fourier Transform](https://en.wikipedia.org/wiki/Fast_Fourier_transform). 
FFT is an algorithm that samples a signal over a period of time (or space) and divides it into its frequency components. By transforming the music from time domain to frequency domain, we will have a unified representation of different musics
on the same scale.

Following is a picture ([spectrogram](https://en.wikipedia.org/wiki/Spectrogram)) for the song *Yesterday Once More* in frequency domain. 

<img src="https://github.com/kealyn/MusicFinder/blob/master/Spectro_Original.png" width="600">
                 Fig 1. Spectrogram of Yesterday Once More

The x-axis represents the sampling over time for the song. As per [Nyquist–Shannon sampling theorem](https://en.wikipedia.org/wiki/Nyquist%E2%80%93Shannon_sampling_theorem), we need a sampling rate of 44,100 Hz to avoid frequency loss. The y-axis represents the range of frequencies. The FFT shows us the strength, i.e. amplitude, of the signal at that particular frequency. As shown in the picture, the frequency and time values are discretized, while the amplitudes are continuous. Brighter color indicates higher amplitude.

### Fingerprints

After converting to spectrogram, the question is how to identify this song uniquely from a certain distribution or patterns. Moreover, our recognition step needs to survive in a noisy environment, requiring that this distribution to be robust and not sensitive to small interferences.

The process of [Acoustic Fingerprint](https://en.wikipedia.org/wiki/Acoustic_fingerprint) fits perfectly to our needs. If two files sound alike to the human ear, their acoustic fingerprints should match, even if their binary representations are quite different. Essentially, the fingerprints should differ from hash functions, which must be sensitive to any small changes in the data.

In the case of [Shazam](https://www.shazam.com/), their algorithm then picks out points where there are peaks in the graph, labeled as "higher energy content". In practice, this seems to work out to about three points per song [1]. Focusing on peaks in the audio greatly reduces the impact that background noise has on audio identification. 

### Shazam algorithm

To understand the algorithm behind the scene, we look at the following example:

<img src="https://web.archive.org/web/20161024115723/http://www.soyoucode.com/wp-content/uploads/2011/01/1.png" width="400">
       Fig 2 (a). The initial spectrogram

<img src="https://web.archive.org/web/20161024115723/http://www.soyoucode.com/wp-content/uploads/2011/01/2.png" width="400">
       Fig 2 (b). Simplified spectrogram (Constellation map)

Notice that the darker spots ("peaks") in Fig 2(a) match the crosses in the Fig 2 (b). To efficiently store and search for a match, they choose some of the peak points from within the simplified spectrogram (called "anchor points") and zones in the vicinity of them (called "target zone"). Now, for each point in the target zone, a hash that will be the aggregation of the following: the frequency at which the anchor point is located (`f1`) + the frequency at which the point in the target zone is located (`f2`)+ the time difference between the time when the point in the target zone is located in the song (`t2`) and the time when the anchor point is located in the song (`t1`) + `t1`. [2]

[Fig 3. Hash calculation](https://web.archive.org/web/20160324143227/http://www.soyoucode.com/wp-content/uploads/2011/01/4.png)

To simplify: `hash = (f1+f2+(t2-t1))+t1`, illustrated in the above figure (Fig 3).







## Storing the fingerprints



## Recognition



## Reference
[1] Surdu, Nicolae (January 20, 2011). "How does Shazam work to recognize a song?". Archived from the original on 2016-10-24. Retrieved 12 February 2018.
[2]  Li-Chun Wang, Avery. "An Industrial-Strength Audio Search Algorithm." Columbia University. Web. 1 Dec. 2014.
