import soundfile as sf
from nemo.collections.tts.models import FastPitchModel
from nemo.collections.tts.models import HifiGanModel

fastpitch_name = "tts_es_fastpitch_multispeaker"
hifigan_name = "tts_es_hifigan_ft_fastpitch_multispeaker"

# Load spectrogram generator
spec_generator = FastPitchModel.from_pretrained(fastpitch_name)

# Load Vocoder
model = HifiGanModel.from_pretrained(hifigan_name)

# Generate audio
text = "Escribe tu texto aquí."
# Optionally, provide custom IPA input escaped with |
# text = "|e s k ɾ ˈ i β e| tu |t ˈ e k s t o| aquí."

parsed = spec_generator.parse(text, normalize=False)
speaker = 5
spectrogram = spec_generator.generate_spectrogram(tokens=parsed, speaker=speaker)
audio = model.convert_spectrogram_to_audio(spec=spectrogram)
audio = audio.detach().cpu().numpy()

# Save the audio to disk in a file called speech.wav
sample_rate = 44100
sf.write("speech.wav", audio, sample_rate)