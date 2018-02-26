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

We have covered the part that how to compute the hash values for peak points, but wait, where did you get these peaks and anchors? Taking one step back, identifying peak points itself is a different (and interesting) problem.

From the spectrum image, a natural way to identify peaks is to traverse all the pixels and apply against a high-pass filtering. Thus, we treat this problem as a image processing problem with the help of [mathematical morphology](https://en.wikipedia.org/wiki/Mathematical_morphology).


<img src="https://github.com/kealyn/MusicFinder/blob/master/Figures/Morphological_neighborhood.png" width="400">

To accurately identify a peak, it is important to consider its neighborhood to decrease the interference from noises. 

**Step 1.** We use the following neighborhood structure to serve as a "mask" and apply to the spectrum recursively for each pixel that is greater than threshold. The result of this step is a matrix `M` with identified local maximums.

**Step 2.** By employing [erosion](https://en.wikipedia.org/wiki/Erosion_(morphology)), a background `B` with erosion operation has been generated.

**Step 3.** Subtract `M` by `B` will yield the peaks `P0`.

**Step 4.** To adjust the number of fingerprints, a threshold `Default_Peak_Threshold`<sup>(i)</sup> is applied to `P0` and finally we get the desired peaks as `P`. 

<sup>(i)</sup> `Default_Peak_Threshold`: Minimum amplitude in spectrogram in order to be considered a peak. Higher value could reduce number of fingerprints, but can negatively affect accuracy.


## Storing the fingerprints

The above-mentioned combinatorial hashing leads to a good amount of hash values: a hash value for each peak point. However, hash values by themselves are not enough to identify a specific rhythm, we need to store the correct order of them, i.e. time dimension.

As we know, each song is consist of multiple hash values, and each hash value corresponds to a time offset. In addition, it also has some metadata such as id and name. There are different ways to store such data:
- **Database.** To avoid storing redundant information, we propose to follow [3NF](https://en.wikipedia.org/wiki/Third_normal_form) and create two tables: song table and hash table. Song id will be used as the primary key for the song table, as well as the foreign key for the hash table. The benefit of using database is that database could help build indexes on the data and help increase the performance; in the meantime, we also get database built-in features, such as concurrent processing, and query optimization. 
- **File.** Storing in file is easier from an API perspective. It is also flexible and does not dependent on other libraries (such as database APIs). However, it may lead to higher space consumption and worse I/O performance.
- **In-memory data grid.** If we have a server with dedicated memory space, we could build an in-memory cache that helps cache and retrieve data through simple `put` and `get` APIs. Apache ignite is an example. However, it is required that such a server to be stable. Moreover, there are quite a number of steps that could set up such a service.


As the initial trial, we decided to use file system to store the fingerprints, more specifically, `.csv` files. The header of the file is consist of [`song_id`, `song_name`, `hash_value`, `offset`]. Note that there can be thousands of hash values for one song, essentially we will store the song_id and song_name thousands of times. However, it does not prevent us from proving the concept.


## Recognition

This section will introduce when a new song is provided (either by music file or through microphone), how the system will match and recognize this song.

**1. Preprocessing.** Load the hash values and song information from the file into main memory and formulate a nested dictionary structure: {song_id, {hash_value, offset}}. We name this data structure as `lib`.

**2. Fingerprinting of the audio.** We will re-use the module of fingerprinting to perform FFT in overlapping windows over the length of the song, extract peaks, and then form fingerprints `new_hash`.

**3. Matching hash values.** Traverse the `lib` and for each song, we try to match the `new_hash` with the hash in the `lib`. We will select `top-k` matches in terms of matching count as the candidates. We also enforce a condition that the number of matchings should be more than 50% compared to the best matching to be considered as a `candidate`.

**4. Aligning time offsets.** If there are more than one candidate, we will then consider the difference between the time offsets of the song in the library and in the new song. This step is needed due to the reason that the new song clip may not necessarily to start from the beginning. We need to examine the differences between offsets to make sure that the "rhythms" are matching. This step is illustrated in the following figure:

<img src="https://github.com/kealyn/MusicFinder/blob/master/Figures/Align_fingerprints.png" width="700">

As shown in the Fig. 3, although the time-offsets of the hashes in the new song do not match the original library, their differences are matching. In addition, we also have two missing hash values in the new song, however, this will not have an impact to the alignment process.

After these steps, we will pick the top-1 song that has the best match and the best alignment to be the returning result.


## Performance

The empirical setup can be found in the following table:

| Item | Description |
| --- | --- |
| Number of songs | 100 |
| Sampling rate | 44100 Hz |
| Total fingerprints | 1.3 million |
| Library file size | 99.3 MB |


The following figure depicts the number of fingerprints w.r.t. each song in the library:

<img src="https://github.com/kealyn/MusicFinder/blob/master/Plots/Fingerprints_distribtion.png" width="800">

From the data, it suggests that the number of collected fingerprints vary from one song to another. The largest number of fingerprints for one song is 32,906 while the least number is 1,551. 

Next, we will perform three set of experiments.

The first set of experiment is to recognize local music files. For this purpose, we have randomly picked 10 songs out of the 100 songs and try to find the best match. We only feed in the system with the first 10 seconds of the song. Here are the results:

| Time limit (s) | Encoding time (s) | Recognition time | Recognition rate |
| --- | --- | --- | --- |
| 10 | 3.18 (avg) | 0.09 (avg) | 100% |

It is shown that all of the testing songs can be recognized within 10 seconds.

The second set of experiment is to recognize songs from the microphone. Again, we have randomly chosen 10 songs to be played through the microphone. In addition, we also put some extra noise while playing. Here are the results:

| Noise level |Time limit (s) | Encoding time (s) | Recognition time | Recognition rate |
| --- |--- | --- | --- | --- |
| Normal | 10 | 3.18 (avg) | 0.09 (avg) | 100% |
| Extra  | 10 | 


The third set of experiment is to give a new song that does not appear in the song library.



## Enhancements
- **Fingerprint library service**: This can save the loading time of fingerprints prior to recognition.
- **A simple GUI**
- **"Pseudo" voice recognition:** Add audio samples of words, phrases, and sentences so that MF could also identify certain commands, such as "turn on the TV". 
- **Voice recognition:** The voice recognition mentioned in the above point is very limited and cannot process natural languages. For example, MF will not find the similarities between "turn off the computer" and "could you please shut down the computer". To make MF equip with voice recognition, neural network models need to be integrated and properly trained.
- **Emotional detector:** If the audio files are labeled with auxiliary information, MF can be used to find the appropriate label for the new sample with the help of a probability model. For example, with emotional labels for different voices, such as angry, excited, sad, etc., MF could perform as an `emotional detector` that suggests the likelihood of the given sample being recorded with a angry emotion, or happy emotion.



## Reference
[1] Surdu, Nicolae (January 20, 2011). "How does Shazam work to recognize a song?". Archived from the original on 2016-10-24. Retrieved 12 February 2018.

[2]  Li-Chun Wang, Avery. "An Industrial-Strength Audio Search Algorithm." Columbia University. Web. 1 Dec. 2014.
