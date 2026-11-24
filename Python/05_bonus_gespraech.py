"""Enter startet und stoppt die Aufnahme. q + Enter beendet das Gespräch."""
from pathlib import Path
import signal
import subprocess
from tempfile import TemporaryDirectory
from fragen import fragen
from sprechen import sprechen
from verstehen import verstehen


def aufnehmen(datei):
    datei.unlink(missing_ok=True)
    with subprocess.Popen([
        "arecord", "-q", "-D", "default", "-t", "wav",
        "-f", "S16_LE", "-r", "16000", "-c", "1", str(datei),
    ], stdin=subprocess.DEVNULL, start_new_session=True) as prozess:
        try:
            input("Aufnahme läuft – Enter zum Stoppen: ")
        finally:
            if prozess.poll() is None:
                prozess.send_signal(signal.SIGINT)  # WAV sauber abschließen.
            code = prozess.wait()
    if code:
        raise subprocess.CalledProcessError(code, prozess.args)


def main():
    verlauf = []  # Bleibt nur während dieses Gesprächs im Arbeitsspeicher.
    try:
        with TemporaryDirectory(prefix="sprachki-") as ordner:
            frage_wav = Path(ordner) / "frage.wav"
            antwort_wav = Path(ordner) / "antwort.wav"
            while input("Enter zum Sprechen, q zum Beenden: ").strip().lower() != "q":
                aufnehmen(frage_wav)
                text = verstehen(str(frage_wav))
                print("Du:", text)
                if not text.strip():
                    print("Keine Sprache erkannt. Bitte erneut versuchen.")
                    continue
                antwort = fragen(text, verlauf=verlauf)
                print("KI:", antwort)
                sprechen(antwort, antwort_wav)
                subprocess.run(["aplay", "-q", str(antwort_wav)], check=True)
    except (KeyboardInterrupt, EOFError):
        pass
    print("Gespräch beendet.")


if __name__ == "__main__":
    main()
