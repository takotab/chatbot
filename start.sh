#!/bin/sh

sudo docker kill $(sudo docker ps -q)
sudo docker build -t chatbot .
echo "docker build"
sudo docker run -it -p 8080:8080 -e GOOGLE_APPLICATION_CREDENTIALS='/app/Chatbot TINA-a050ea22b80f.json' chatbot