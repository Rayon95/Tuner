import pyaudio
import numpy as np
import matplotlib.pyplot as plt

# Definisci la frequenza di campionamento e la lunghezza del buffer audio
RATE = 44100
CHUNK = 1024

# Inizializza PyAudio
p = pyaudio.PyAudio()

# Apri lo stream audio
stream = p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

# Loop di acquisizione e elaborazione audio
while True:
    # Acquisisci il buffer audio
    data = np.frombuffer(stream.read(CHUNK), dtype=np.float32)
    
    # Esegui la FFT sui dati audio
    fft_data = np.abs(np.fft.fft(data))
    
    # Identifica la frequenza fondamentale
    freq_index = np.argmax(fft_data[:len(fft_data)//2])
    fundamental_freq = freq_index * RATE / CHUNK
    
    # Confronta la frequenza fondamentale con la nota desiderata
    note_freqs = {
        'E2': 82.41,
        'A2': 110.00,
        'D3': 146.83,
        'G3': 196.00,
        'B3': 246.94,
        'E4': 329.63
    }
    note_name, note_freq = max(note_freqs.items(), key=lambda x: x[1] - fundamental_freq)
    deviation = fundamental_freq - note_freq
    
    # Fornisci un feedback visivo o sonoro
    if abs(deviation) < 5:
        print(f'Accordato a {note_name}')
    else:
        print(f'Deviazione di {deviation:.2f} Hz da {note_name}')
    
    # Plot della FFT (opzionale)
    plt.plot