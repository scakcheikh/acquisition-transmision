#Programme d'acquisition de données et de transmission basée sur le signal

##Organisation du document:

### ARCHITECTURE 1 : Raspberry + FONA_3G 
-----------------------------------------------------------------------
./controller/cntrlr2.py : programme d'acquisition et de transmission
./controller/fona_3G.py : librairie de fonctions pour l'acquisition des coordonnées gps
./controller/packageToXML.py : script d'empaquetage xml
./controller/scanWrlessForSignal.py : script de scan des réseaux wifi
./controller/interface.Sh : script de marquage des paquets selon le port de sortie sur le raspberry pi
./controller/records/ftp_client.py : client ftp pour l'envoi des fichiers xml
./controller/records/__init.py__.py: python script
./controller/stats/: folder to log stats
./controller/test/: for testing
./3G_modem_tutorial.pdf : how to turn FONA 3G into a modem
./pyftpdlib-1.5.0 2: ftplib directory
./adafruit docs: FONA 3G docs


### ANCIENNE ARCHITECTURE : Raspberry + Arduino + FONA_3G 
-----------------------------------------------------------------------
./controller/cntrlr.py : ancienne version du contrôleur, où le FONA est connecté à un arduino et l'arduino connecté au raspberry
./controller/fetch_gps.py : acquisition des coordonnées gps sur l'architecture Rpi+arduino+fona

### MODULES NECESSAIRES 
**[ftplib](https://docs.python.org/3/library/ftplib.html#module-ftplib)** : pour le transfert de fichier FTP
**wvdial


Repository: 