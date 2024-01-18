## If you don't have tkinter installed yet
### *sudo apt update && sudo apt install python3-tk*
## Install Pillow
### *python -m pip install -U Pillow*
## Move this repository into the default location
### *sudo cp -r ./pomodoro /opt/*
## Add the launcher to the start menu
### *sudo cd /opt/pomodoro && sudo cp ./tomato.desktop /usr/share/applications/*
## Set the launcher as "trusted"
### *gio set /usr/share/applications/tomato.desktop "metadata::trusted" yes*
### *sudo chmod +x /usr/share/applications/tomato.desktop*
