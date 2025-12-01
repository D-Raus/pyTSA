The Matlab function 'tsa' allows to compute the phase-average of a signal with varying cycles length.

As an avid user of this Matlab function, I was frustrated not to find an equivalent with Python.

## Algorithms
Time-domain method (pyTSA_TimeDomain function):
1. Divide the signal into segments corresponding to the different cycles
2. Interpolate the signals in each segment on the same number of samples
3. Compute the average of all the resampled segments

Frequency-domain method (py_TSA_fft function):
1. Divide the signal into segments corresponding to the different cycles
2. Compute the fft of each segment
3. Truncate the results on each segment so that all fft have the same length as the one of the shortest cycle
4. Average all the spectra
5. Compute the inverse fft to obtain the phase-averaged signal in the time domain.

## Example
The code 'pyTSA_example.py' presents an example of use of the TSA algorithms for the computation of the time-synchronous average of the position of a fan blade as it slows down after switchoff.
This example is inspired by the Matlab example presented in the 'tsa' function help page 

The scipy.signal 'find_peaks' is first used to detect the beginning of each cycle:
<img width="997" height="413" alt="blade position" src="https://github.com/user-attachments/assets/45aeaef1-fe9a-45fe-b799-277c7fe6a856" />

The pyTSA module is then tested to compute the phase-averaged position of the the fan blade during one cycle:
<img width="1023" height="480" alt="blade position phase average" src="https://github.com/user-attachments/assets/5596e627-bb58-47d9-8c9f-5ce25ea0fd36" />




## Reference
Bechhoefer, Eric, and Michael Kingsley. "A Review of Time-Synchronous Average Algorithms." Proceedings of the Annual Conference of the Prognostics and Health Management Society, San Diego, CA, September-October, 2009.




