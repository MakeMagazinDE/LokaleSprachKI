Die Anleitung im Artikel lässt sich auch mit **WSL2** (Windows Subsystem for Linux) umsetzen. Wer dieses Tool noch nie verwendet hat, findet [in diesem Make-Artikel](https://www.heise.de/ratgeber/Fuer-Maker-Windows-Subsystem-fuer-Linux-2-einrichten-9598528.html) den passenden Einstieg. Hier sind nur die wichtigsten Schritte aufgelistet:

1. In der Powershell `wsl.exe --install Debian` eingeben (aktiviert WSL2 und lädt Debian).
2. Windows neu starten.
3. Den Anleitungsschritten im Artikel folgen.

**Folgende Dinge muss man bei WSL2 beachten:**
- Die Beispiel-Skripte kann man mithilfe des Explorers in WSL2 kopieren: Dafür scrollt man bei den Laufwerken runter zu "Linux" und legt die Dateien dann in den Ordner "Debian/home/[Benutzer]/sprachki".
- Falls WSL2 das heruntergeladene Ollama nicht entpacken kann, weil ihm "zstd" fehlt, kann man es mit diesem Befehl nachinstallieren: `sudo apt install zstd`
- WSL2 besitzt standardmäßig keine emulierte Soundkarte. Daher muss man ein Bridge-Plug-in installieren: <br>`sudo apt install alsa-utils libasound2-plugins pulseaudio.utils`
- Das Abspielen einer Audiodatei funktioniert dann mit: `aplay -D pulse antwort.wav`
- Damit wir nicht immer `pulse` eingeben müssen, stellen wir es als Standardgerät ein. Gleichzeitig beseitigen wir ein Sound-Pufferproblem von WSL2. Dafür geben wir `nano ~/.asoundrc` ein. Dann tragen wir in das Dokument folgende Zeilen ein und speichern mit Strg+X: <br>
```
pcm.!default {
     type pulse
     hint.description „Default Audio Device via PulseAudio“
}

ctl.!default {
	type pulse
}

# Verhindert Underruns unter WSL2, indem der Puffer vergrößert wird
pcm.pulse {
	type pulse
	buffer_size 16384
	period_size 4096
}
```
PCM steuert den Stream und ctl z. B. die Lautstärke.<br>

- Damit das Skript `verstehen.py` funktioniert, brauchen wir noch PyAV in einer Version vor 19.x: `python -m pip install "av<19"`





