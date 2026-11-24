"""Eine bereits aufgenommene Frage beantworten und die Antwort abspielen."""
import subprocess
from fragen import fragen
from sprechen import sprechen
from verstehen import verstehen


def dialog():
    frage = verstehen("frage.wav")
    print("Erkannt:", frage)
    if not frage.strip():
        print("Keine Sprache erkannt. Bitte die Aufnahme prüfen und erneut versuchen.")
        return
    antwort = fragen(frage)
    print("Antwort:", antwort)
    sprechen(antwort, "antwort.wav")
    subprocess.run(["aplay", "antwort.wav"], check=True)


if __name__ == "__main__":
    dialog()
