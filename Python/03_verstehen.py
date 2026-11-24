"""Eine deutsche Aufnahme mit faster-whisper in Text umwandeln."""
from functools import cache


@cache
def modell_laden():
    import os
    os.environ["HF_HUB_DISABLE_TELEMETRY"] = "1"
    os.environ["DO_NOT_TRACK"] = "1"
    from faster_whisper import WhisperModel

    return WhisperModel("small", device="cpu", compute_type="int8")


def verstehen(datei="frage.wav"):
    segmente, _ = modell_laden().transcribe(datei, language="de")
    return " ".join(segment.text.strip() for segment in segmente).strip()


if __name__ == "__main__":
    print(verstehen())
