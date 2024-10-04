#!/bin/sh
# https://jellyfin.org/docs/ !Vorablesen!
# added new Proxmox LXC
# Default Settings: 2GB RAM - 8GB Storage - 2vCPU
# use Ubuntu server 

# Aktualisieren Sie das Paketverzeichnis
sudo apt update

# Aktualisieren Sie alle Pakete
sudo apt full-upgrade -y

# Entfernen Sie nicht benötigte Pakete
sudo apt autoremove -y

# Bereinigen Sie den Cache
sudo apt clean


#mkdir /jellyfin                                                                                   // Verzeichnis im LXC Container (Server) erstellen

#nano /etc/fstab                                                                                   // Hier wird das NAS Laufwerk gemountet
#//127.0.0.1/jellyfin /jellyfin cifs credentials=/home/.smbcredentials,uid=1000,gid=1000 0 0         // DEINE IP muss die vom NAS sein, wenn die Daten extern liegen.
                                                                                                  #// Auf dem NAS habe ich einen Ordner names /jellyfin erstellt wo wo all meine Inhalte der mediathek liegen

#nano /home/.smbcredentials                                                                        // Diese Datei muss noch angelegt werden
#username=                                                                                         // Benutzername vom NAS User der auf den Ordner daraufzugreifen darf 
#password=                                                                                         // Passwort vom NAS User der auf den Ordner daraufzugreifen darf

#mount -a                                                                                          // Mit dem befehl wird der Ordner gemountet und wenn kein Fehler kommt, wurde alles richtig eingetragen

#cd /jellyfin/                                                                                     // In den Ordner wechseln

#ls                                                                                                // Überprüfen ob die Ordner vom NAS auch gefunden wurden

#cd Movies/                                                                                        // Hiermit prüfen wird ob Dateien im NAS Ordner sind  

#apt install sudo curl                                                                             // Pakete sudo und curl nach installieren für die installation von Jellyfin

#curl https://repo.jellyfin.org/install-debuntu.sh | sudo bash                                     // Mit Enter besätigten und auf die aufforderung "press <Enter>" warten und wieder bestätigen

# Kurz warten und dann wurde Jellyfin installiert, dies ist Hilfeanleitung wie man eine Instanz unter Proxmox aufsetzt
