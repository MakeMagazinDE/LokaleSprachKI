"""Text mit einer heruntergeladenen Piper-Stimme als WAV speichern."""
from pathlib import Path
from functools import cache
import wave


@cache
def stimme_laden():
    import onnxruntime
    onnxruntime.disable_telemetry_events()
    from piper import PiperVoice

    modell = Path(__file__).resolve().with_name("de_DE-thorsten-medium.onnx")
    return PiperVoice.load(str(modell))


def sprechen(text, ausgabe="antwort.wav"):
    stimme = stimme_laden()
    with wave.open(str(ausgabe), "wb") as datei:
        stimme.synthesize_wav(text, datei)


def main(argv=None):
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("text", help="Zu sprechender Text, in Anführungszeichen")
    args = parser.parse_args(argv)
    if not args.text.strip():
        parser.error("Der Text darf nicht leer sein.")
    sprechen(args.text)


if __name__ == "__main__":
    main()
