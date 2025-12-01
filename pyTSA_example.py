"""
This code presents an example of use of the TSA algorithms. 
for the computation of the time-synchronous average of the position of a fan blade as it slows down after switchoff.
This example is inspired by the Matlab example presented in the 'tsa' function help page 

Two methods are tested:
- Time-domain method (function pyTSA_TimeDomain)
- Frequency-domain method (function pyTSA_fft)

D-Raus
11/02/21
"""

import numpy as np
import matplotlib.pyplot as plt
import scipy as sp

### Load pyTSA module
import pyTSA_functions as pyTSA



def main():

    
    ### Create instantaneous signal
    fs = 1000
    time_lim = 3
    t = np.arange(0,time_lim,1/fs)

    rpm0 = 2400   
    a = 0.1
    f0 = rpm0/60    # original rotation frequency (Hz)
    T = 0.75        # decay time (s)
    phi = 2*np.pi*f0*T*(1-np.exp(-t/T))
    
    signal = a*np.cos(phi) + np.random.randn(np.size(phi))/200
        
    ### Detect beginning of cycles
    ind_pulse,_ = sp.signal.find_peaks(-a*np.cos(phi))
    
    ### Plot signal to check that cycles beginning are well detected
    plt.figure()
    plt.plot(t,signal)
    plt.plot(t[ind_pulse],signal[ind_pulse],'r+')
    plt.xlabel('$t$')
    plt.ylabel('Amplitude')
    

    ### Compute the phase-averaged signal with the Time-domain method
    y_TSA_TimeDomain,t_interp = pyTSA.pyTSA_TimeDomain(signal,t,ind_pulse,fs)

    ### Compute the phase-averaged signal with the fft method
    y_TSA_fft,t_TSA_fft = pyTSA.pyTSA_fft(signal,ind_pulse,fs)
    

    ### Plot the phase-averaged signal and compare with the instantaneous signal
    plt.figure()

    for pp in np.arange(len(ind_pulse)-1):
        t_instant_norm = (t[ind_pulse[pp]:ind_pulse[pp+1]]-t[ind_pulse[pp]])/max((t[ind_pulse[pp]:ind_pulse[pp+1]]-t[ind_pulse[pp]]));
        p_instant, = plt.plot(t_instant_norm,signal[ind_pulse[pp]:ind_pulse[pp+1]],color=(0.8, 0.8, 0.8))
    p_method1, = plt.plot((t_interp-t_interp[1])/max(t_interp-t_interp[1]),np.rot90(y_TSA_TimeDomain),color=(0.1, 0.2, 0.5))
    p_method2, = plt.plot(t_TSA_fft/max(t_TSA_fft),y_TSA_fft,'r')
    plt.legend([p_instant, p_method1, p_method2],["Original signal","TSA: Time-domain method","TSA: FFT method"])
    plt.xlabel("Phase (rotations)")
    plt.ylabel("Amplitude")
    plt.title('Time-synchronous average')
    
    
    
if __name__ == '__main__':
    main()
    
    




