"""Eine kurze deutsche Antwort von Ollama abfragen."""
import json
from urllib.request import Request, urlopen


def fragen(text, url="http://localhost:11434/api/chat", verlauf=None):
    bisher = [] if verlauf is None else verlauf
    frage = {"role": "user", "content": text}
    daten = {
        "model": "gemma4:12b-it-qat",
        "stream": False,
        "options": {"num_ctx": 8192, "num_predict": 1024},
        "messages": [
            {"role": "system", "content": "Antworte auf Deutsch in höchstens zwei Sätzen."},
        ] + bisher + [frage],
    }
    anfrage = Request(url, data=json.dumps(daten).encode("utf-8"),
                      headers={"Content-Type": "application/json"})
    with urlopen(anfrage, timeout=180) as antwort:
        inhalt = json.load(antwort)["message"]["content"]
    if not isinstance(inhalt, str) or not inhalt.strip():
        raise ValueError("Ollama hat keine Textantwort geliefert.")
    if verlauf is not None:
        verlauf.extend([frage, {"role": "assistant", "content": inhalt}])
        del verlauf[:-20]  # Höchstens zehn vollständige Frage-Antwort-Paare behalten.
    return inhalt


if __name__ == "__main__":
    print(fragen(input("Frage: ")))
