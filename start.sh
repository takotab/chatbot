sudo docker kill $(sudo docker ps -q)
sudo docker build -t chatbot .
sudo docker run -t -p 8080:8080 chatbot