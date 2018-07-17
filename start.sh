sudo docker kill $(sudo docker ps -q)
docker build -t chatbot .
echo "docker build"
docker run -it -p 8080:8080 chatbot

#echo "start tests"
#python3 -m pytest tests