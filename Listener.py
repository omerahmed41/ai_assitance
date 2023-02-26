import speech_recognition as sr
from scipy.signal import butter, filtfilt, iirnotch


class Listener:
    def __init__(self):
        self.active = True

    def bandpass_filter(self, data, lowcut, highcut, fs, order=5):
        # Generate bandpass filter coefficients
        nyq = 0.5 * fs
        low = lowcut / nyq
        high = highcut / nyq
        b, a = butter(order, [low, high], btype='band')

        # Apply filter to data using forward-backward filtering
        filtered_data = filtfilt(b, a, data)
        return filtered_data

    def listen(self, keyword="sayda", timeout=5):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            # Set filter to a bandpass filter that removes low and high-frequency noise
            source.filter = lambda data, _: self.bandpass_filter(data, 300, 2000, source.SAMPLE_RATE)
            # Apply notch filter to remove speaker output frequency range
            nyq = source.SAMPLE_RATE / 2.0
            notch_freq = 3000  # Adjust this frequency to remove the speaker output range
            notch_width = 100  # Adjust this width to widen the frequency range to remove
            b, a = iirnotch(notch_freq / nyq, notch_width / nyq)

            # Apply filter to data using forward-backward filtering
            source.filter = lambda data, _: filtfilt(b, a, self.bandpass_filter(data, 300, 2000, source.SAMPLE_RATE))

            r.adjust_for_ambient_noise(source)  # adjust for ambient noise
            print("Speak now...")
            audio = r.listen(source, phrase_time_limit=timeout)
            try:
                user_input = r.recognize_google(audio)
                return user_input

            except sr.UnknownValueError:
                pass
                # print("Sorry, I couldn't understand what you said.")
            except sr.RequestError:
                pass
                # print("Sorry, my speech recognition service is down.")
