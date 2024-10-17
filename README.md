# jarvis

Tested on RasPi 3B

## files:
* /etc/systemd/system/jarvis_listener.service
* /home/pi/jarvis_listener.py

## Requirements
* $> pip install SpeechRecognition requests

## Enable Service
* $> sudo systemctl enable jarvis_listener.service
* $> sudo systemctl start jarvis_listener.service

## In Action
You need a Rest Service backend (NodeRed, for example) to execute whatever commands you want to execute over GPIO´s

