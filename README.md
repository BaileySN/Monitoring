# Monitoring

Dieses kleine Programm prüft Täglich die Kapazität der Platten.

Falls eine Platte über den eingestellten Wert kommt, schickt es eine E-Mail an den Admin.


## config.py

Die Konfiguration findet in der config.py statt conf/config.py.

Beim ersten lauf sollte das Template config.py.orig nach config.py umbenannt werden.

Folgende Werte sollten eingestellt und geprüft werden.


* Schwellwert in %
    
    DSPACEPERCENT = 80 

* E-Mail Absender z.b.: root
    
    EMAIL_SENDER = "root"

* E-Mail Empfänger kann ein Benutzer im System oder eine E-Mail Adresse sein
    
    EMAIL_RECIPIENT = "guenter"

* E-Mail Server
    
    SMTPSERVER = "127.0.0.1"

