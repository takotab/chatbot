sudo docker kill $(sudo docker ps -q)
sudo docker build -t chatbot .
echo "docker build"
sudo docker run -it -p 8080:8080 chatbot