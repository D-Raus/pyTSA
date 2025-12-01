"""
Functions to compute the time-synchronous average of a signal with varying cycle length

Two methods are tested:
- Time-domain method (function pyTSA_TimeDomain)
- Frequency-domain method (function pyTSA_fft)

D-Raus
11/02/21
"""

import numpy as np
import scipy



def pyTSA_TimeDomain(y,t,ind_pulse,fs):
    """
    Computation of the phase-average of a signal in the time domain

    Parameters
    ----------
    y : array of floats
        signal to be phase-averaged.
    t : array of floats
        time vector.
    ind_pulse : array of int
        indexes of the beginning of the cycles .
    fs : float
        sampling frequency of y.

    Returns
    -------
    y_TSA_TimeDomain : array of floats
        phase-average of y.
    t_interp : array of floats
        time vector of the phase-average.

    """
    # Length of the signal for the interpolation
    N = max(np.diff(ind_pulse/fs))*fs
    
    y_TSA_TimeDomain = np.zeros((1,round(N)))
    PP = 0

    for pp in np.arange(len(ind_pulse)-1):
        
        # Interpolates the signal onto grids of equally spaced samples corresponding to the different cycles.
        t_interp = np.linspace(t[ind_pulse[pp]],t[ind_pulse[pp+1]],round(N))
        y_rs = scipy.interpolate.pchip_interpolate(t[ind_pulse[pp]:ind_pulse[pp+1]],y[ind_pulse[pp]:ind_pulse[pp+1]],t_interp, der=0, axis=0)
        
        # Concatenates the resampled signal segments
        y_TSA_TimeDomain = y_TSA_TimeDomain + y_rs
        PP = PP + 1
        
    # Computes the average of all the segments.    
    y_TSA_TimeDomain = y_TSA_TimeDomain/PP

    return y_TSA_TimeDomain,t_interp



def pyTSA_fft(y,ind_pulse,fs):    
    """
    Computation of the phase-average of a signal in the frequency domain

    Parameters
    ----------
    y : array of floats
        signal to be phase-averaged.
        
    ind_pulse : array of int
        indexes of the beginning of the cycles .
    fs : float
        sampling frequency of y.

    Returns
    -------
    y_TSA_fft : array of floats
        phase-average of y.
    t_TSA_fft : array of floats
        time vector of the phase-average.
    """
    
    nF = np.min(np.diff(ind_pulse))-1
    Y_TSA_fft_tmp = np.zeros((len(ind_pulse),nF),dtype=complex)
    
    PP = 0
    
    for pp in np.arange(len(ind_pulse)-1):
        
        # Breaks the signal into segments corresponding to the different cycles.
        signal_crop = y[ind_pulse[pp]:ind_pulse[pp+1]]
        
        # Computes the discrete Fourier transform of each segment.
        spec = np.fft.fft(signal_crop)/len(signal_crop)
    
        # Truncates the longer transforms so all transforms have the same length.
        Y_TSA_fft_tmp[pp,:] = spec[0:nF]*nF*2
        
        PP = PP +1
    
    # Averages the spectra
    Y_TSA_fft = np.mean(Y_TSA_fft_tmp,0)

    # Computes the inverse discrete Fourier transform of the average to convert it to the time domain
    fd = np.append(np.append(Y_TSA_fft,0),np.conj(np.flipud(Y_TSA_fft[1:])))

    y_TSA_fft = np.real(np.fft.ifft(fd));
    t_TSA_fft = np.arange(0,len(y_TSA_fft)/fs,1/fs)
    

    return y_TSA_fft,t_TSA_fft
