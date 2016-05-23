# Monitoring

Dieses kleine Programm prüft Täglich die Kapazität der Platten.

Falls eine Platte über den eingestellten Wert kommt, schickt es eine E-Mail an den Admin.

## Benötigte Packete
* python3-psutil (derzeit geht auch noch python-psutil)
* python3 (derzeit geht auch noch pyhton2)


## config.py

Die Konfiguration findet in der config.py statt conf/config.py.

Beim ersten lauf sollte das Template config.py.orig nach config.py umbenannt werden.

Bei Updates sollte man die Werte config.py.orig und config.py vergleichen. (da derzeit nur die config.py.orig erweitert wird)

Folgende Werte sollten eingestellt und geprüft werden.


* Schwellwert in %
    
    DSPACEPERCENT = 80 

* E-Mail Absender z.b.: root
    
    EMAIL_SENDER = "root"

* E-Mail Empfänger kann ein Benutzer im System oder eine E-Mail Adresse sein
    
    EMAIL_RECIPIENT = "guenter"

* E-Mail Server
    
    SMTPSERVER = "127.0.0.1"

Ab Version 0.2 muss folgendes in der config.py hinzugefügt werden.

    SMTP_SSL = False (Falls SSL am Mailserver verwendet wird mit TRUE ersetzen)
    USE_AUTH = False (Falls Authentifizierung am Mailserver verwendet wird mit TRUE ersetzen)

Ab Version 0.4a kommt noch folgendes hinzu.

    SMTP_PORT = 465 (Oder falls kein SSL/TLS Port 25)

## cronjob einrichten

Das Programm können wir mit dem Befehl im Programmordner starten:

''python3 program.py'' (derzeit geht auch noch mit dem Aufruf Python)

Dabei prüft es ob die Laufwerke alle unter dem eingestelltem Wert sind.
Testweise ist mir Aufgefallen, dass die Berechnung ein wenig von der Systemansicht abweicht.
Somit kann es sein falls mit ''df -h'' eigentlich 81% stehen würden es aber mit dem Programm nur 78% oder 79% ermittelt werden.

Sollten die Tests gut laufen, kann man es derzeit direct in den Cronjob einbauen.
Beispiel.: (Ich habe das packet mit git unter ''/opt'' runtergeladen und Konfiguriert, der Pfad lautet somit ''/opt/Monitoring/'').

30 6    * * *   root    cd /opt/Monitoring &&python3 program.py <oder python program.py>

Man sollte statt den Benutzer Root einen anderen nehmen, der dies Ausführen darf.

Achtung: Dieses Programm ist noch in der Entwicklung, somit bitte gut Testen!


## Hilfe

Die Hilfe Funktion kann man wie folgt öffnen.

''python3 program.py --help''

