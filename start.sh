sudo docker kill $(sudo docker ps -q)
sudo docker build -t chatbot .
echo "docker build"
sudo docker run -t -p 8080:8080 chatbot