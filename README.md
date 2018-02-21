# MusicFinder
Imagine that you are at a coffee shop, writing code and enjoying the afternoon with a beautiful melody is playing in the background. You start wondering: what is this song? It sounds familiar. We know that Siri and Google Assistant are able to identify a music within half a minute, but how does it work?

Inspired by dejavu project, here I build and present the workflow of MusicFinder v1.

## Music fingerprinting

### FFT: from time domain to frequency domain

As a first step, we need to extract useful information from the music that could help identify it. For this purpose, we take help from [Fast Fourier Transform] (https://en.wikipedia.org/wiki/Fast_Fourier_transform). 
FFT is an algorithm that samples a signal over a period of time (or space) and divides it into its frequency components. By transforming the music from time domain to frequency domain, we will have a unified representation of different musics
on the same scale.

Following is a picture ([spectrogram] (https://en.wikipedia.org/wiki/Spectrogram)) for the song *Yesterday Once More* in frequency domain. 










## Storing the fingerprints



## Recognition





