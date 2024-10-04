#!/bin/bash

# Aktualisiere die Paketlisten
sudo apt update

# Aktualisiere alle installierten Pakete
sudo apt full-upgrade -y

# Entferne nicht benötigte Pakete
sudo apt autoremove -y

# Bereinige den Cache
sudo apt clean

echo "Dein Ubuntu-System wurde erfolgreich aktualisiert!"