from scipy.io import wavfile
from scipy.signal import welch
import numpy as np
from pylab import subplots, show, asarray, int16
from numpy import dot, zeros, convolve, abs, sqrt, cumsum, std, searchsorted
from numpy.random import randn
from sounddevice import play as playsound
from scipy.linalg import svd
import matplotlib.pyplot as plt

def play(w, fs=40000):
    "Play audio from float array"
    w16 = asarray(w / abs(w).max() * (1 << 15), int16)
    playsound(w16, samplerate=fs)


def q16(w):
    "quantize into signed 16bit (autoscaled)"
    w = asarray(w)
    return asarray(w / np.max(abs(w)) * (1<<15), int16)


###
### Question #1
###


class LMS(object):
    def __init__(self, N, mu=1e-12):
        """
      Create a generator which applies an Nth order adaptive filter
      """
        # Set initial FIR filter
        if type(N) is int:
            self.beta = zeros(N)
        else:
            self.beta = asarray(N)
        self.mu = float(mu)

    def feed(self, x):
        """
       Feed signal into LMS filter to train it
       """
        x = asarray(x)
        b = self.beta[::-1]
        N = self.beta.size
        for n in range(N, x.size):
            ###
            ### insert computation to update b here
            y = x[n]
            xtemp = x[n - N:n]
            error = y - np.matmul(b, xtemp)
            ###
            b += mu * np.dot(error, xtemp)  ### something
        # Renormalize to unit magnitude
        self.beta = b[::-1] / sqrt(dot(b, b))

    def getFIR(self):
        "Get the adaptive filter"
        return self.beta.copy()

    def clear(self):
        "Reset the adaptive filter"
        self.beta[:] = 0


# Train on chirp
cwfs, cw = wavfile.read('chirp.wav')
cw = cw / std(cw)  # Normalize chirp amplitude

length_fir = 40
fig, ax = plt.subplots(figsize=(12, 8))
for mu in [1e-5, 1e-4, 1e-3]:
    fil = LMS(length_fir, mu)
    fil.feed(cw)
    ax.plot(fil.getFIR(), '.-', label=f"$\\mu={mu}$")
ax.legend(loc=0)
ax.set_title('FIR Coefficients for Different Learning Rates')
ax.set_xlabel('Coefficient Index')
ax.set_ylabel('Amplitude')
ax.grid()

# Plot the filter response
fig1, ax1 = plt.subplots(figsize=(12, 8))
wn = randn(100000)  # Generate white noise
ax1.semilogy(*welch(wn, fs=1.0), label='White Noise')
ax1.semilogy(*welch(cw, fs=1.0), label='Chirp Signal')
ax1.semilogy(*welch(np.convolve(fil.getFIR(), wn)), label='Filtered Noise')
ax1.legend(loc=0)
ax1.set(xlabel='sample freq [fs]', ylabel='power')
ax1.set_title('Power Spectral Density Comparison')
ax1.grid()

# Apply the filter to the mixed sound

fs, mw = wavfile.read('mixed_sound.wav')
print("Playing original mixed sound...")
play(mw, fs)
f = fil.getFIR()
f2 = np.convolve(f, f)  # Double filter: convolve(f2, x) = convolve(f, convolve(f, x))
f4 = np.convolve(f2, f2)  # Quadruple filter

# Plot the Welch power spectral density for raw and filtered signals
fig2, ax2 = plt.subplots(figsize=(12, 8))
ax2.semilogy(*welch(mw, fs=fs), label='Raw Mixed Sound')
ax2.semilogy(*welch(np.convolve(f, mw), fs=fs), label='Enhanced (Single Filter)')
ax2.semilogy(*welch(cw, fs=fs), label='Chirp Signal')
ax2.semilogy(*welch(np.convolve(f4, mw), fs=fs), label='Enhanced (Quadruple Filter)', linewidth=1.5)
ax2.set(xlabel='sample freq [fs]', ylabel='power')
ax2.legend(loc=0)
ax2.set_title('Power Spectral Density of Raw and Enhanced Sounds')
ax2.grid()
plt.show()

enhanced_single = convolve(f, mw)
enhanced_quadruple = np.convolve(f4, mw, "valid")

# Save the audio files as WAV
#wavfile.write('original_mixed_sound.wav', fs, (mw * 32767).astype(np.int16))
wavfile.write('enhanced_single_filter.wav', fs, (q16(enhanced_single)))
wavfile.write('enhanced_quadruple_filter.wav', fs, (q16(enhanced_quadruple)))

print("Audio files saved successfully.")


###
### Question #2
###

def prjFor(dat, lvl=0.999):
    """
    Create projection onto lvl fraction of the variance
    """
    # Perform SVD
    U, s, V = svd(dat, full_matrices=False)
    # Calculate cumulative variance ratio
    cumulative_variance = np.cumsum(s**2) / np.sum(s**2)
    # Determine the number of components needed to capture lvl fraction of the variance
    c = np.searchsorted(cumulative_variance, lvl, side='left') + 1
    # Create the projection matrix
    P = np.matmul(U[:, :c], V[:c, :])
    return P


if 1:
    # Load and normalize the data
    vfs, vw = wavfile.read('voice.wav')
    vw = vw / np.std(vw)
    Pv = prjFor(vw.reshape(115, 500)[:50, :])

    cfs, cw = wavfile.read('chirp.wav')
    cw = cw / np.std(cw)
    Pc = prjFor(cw.reshape(115, 500)[:50, :])

    mfs, mw = wavfile.read('mixed_sound.wav')
    mw = mw / np.std(mw)

    # Convert mixed sound to a collection of clips
    mwm = mw.reshape(115, 500)
    # Project onto the feature spaces for voice and chirp
    vf = np.dot(np.dot(mwm, Pv.T), Pv).flatten()  # Project onto voice subspace
    cf = np.dot(np.dot(mwm, Pc.T), Pc).flatten()  # Project onto chirp subspace
    print(np.shape(Pv.T), np.shape(cf))
    # Plot the Welch power spectral density for each signal
    fig3, ax = plt.subplots(1, 1, figsize=(12, 8))
    ax.semilogy(*welch(vw, fs=vfs), '-r', label="Train Voice")
    ax.semilogy(*welch(cw, fs=cfs), '-b', label="Train Chirp")
    ax.semilogy(*welch(mw, fs=mfs), '-y', label="Mixed")
    ax.semilogy(*welch(vf, fs=mfs), '-m', label="Recovered Voice")
    ax.semilogy(*welch(cf, fs=mfs), '-c', label="Recovered Chirp")
    ax.legend(loc='best')
    ax.set(xlabel='Sample Frequency [fs]', ylabel='Power')
    ax.set_title('Power Spectral Density of Original and Recovered Signals')

plt.show()

# Save the audio files as WAV
wavfile.write('original_mixed_sound.wav', mfs, q16(mw))
wavfile.write('recovered_voice.wav', vfs, q16(vf))
wavfile.write('recovered_chirp.wav', cfs, q16(cf))

