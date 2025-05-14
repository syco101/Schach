# ♟️ Python Schach

Ein selbst entwickeltes Schachspiel mit Python. Es enthält die grundlegenden Spielfunktionen, eine einfache Benutzeroberfläche und die Möglichkeit, das Spiel zu gewinnen durch Schachmatt. Ich habe es möglichst ähnlich zum normalen Schach das jeder kennt programmiert.

## Features
- Volles Schachbrett mit 8×8 Feldern
- Alle standard Schachfiguren mit Bewegung
- Legalitätsprüfung aller Züge (Keine eigenen/überall platzierenden Züge möglich)
- Schach und Schachmatt Erkennung
- Spielerwechsel
- Bauernumwandlung zu Dame
- Startmenü mit Buttons (mit schönen blauen Buttons)
- Spiel beenden oder neu starten (Nach einer verlorenen oder gewonnenen Partie)

## Steuerung
- Figuren mit der Maus auswählen und ziehen
- Gelbe Kreise zeigen mögliche Züge
- Rote Kreise zeigen Schläge an
- „Grün gewinnt“ / „Blau gewinnt“-Anzeige bei Schachmatt

## Reflexion

Das Projekt war Teil einer grösseren Lernphase rund um Python, Logik, Zugregeln und UI-Design. Ich habe viele Probleme schrittweise gelöst und durch Testen und Debugging gelernt, wie man Spiellogik sauber strukturiert.

Ich wollte das Projekt unbedingt in Python umsetzen, weil ich bisher Python nur im Machine-Learning Modul 259 verwendet habe. Die Sprache hat mich fasziniert und ich wollte herausfinden, wie weit ich damit komme, wenn ich ein vollständiges Schachspiel entwickle. Das Projekt hat mich viel Zeit gekostet – auch, weil ich zu Beginn einige Schwierigkeiten mit der Sprache und mit pygame hatte. Gerade die Zuglogik und die ganzen Spezialfälle waren nicht einfach zu lösen.
Das Wichtigste ist aber: Ich habe durch dieses Projekt viel dazugelernt. Ich verstehe jetzt nicht nur Python besser (Auch wenn noch nicht perfekt), sondern auch, wie man komplexe Probleme Schritt für Schritt analysiert.
Heute bin ich deutlich weiter als am Anfang – sowohl im Programmieren als auch im logischen Denken. Es hat sich auf jeden Fall gelohnt.

Ein Fehler hat mich besonders viel Zeit gekostet:  
Ich wollte, dass der Bauer am Anfang 2 Felder nach vorne ziehen kann, **aber es hat nie funktioniert ohne mein Spiel zu zerstören**, obwohl die Logik für mich eigentlich richtig aussah. Nach sehr viel Testen habe ich dann gemerkt, dass ich aus Versehen `start_row = 6 if color == "b"` geschrieben hatte  also **blau** als untere Farbe gesetzt hatte, obwohl es eigentlich Grün sein musste. Das war ein kleiner, aber entscheidender Denkfehler.  
Nachdem ich das angepasst habe, ging plötzlich alles wie erwartet.

Ich habe auch gelernt, dass man sehr oft an kleinen Details scheitert aber genau das ist für mich das spannende in  programmieren: Fehler machen, debuggen, verstehen, verbessern.

---

Made by syco101
