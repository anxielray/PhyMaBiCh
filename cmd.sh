docker-compose down
docker container prune -f  
docker image rm phymabich_frontend   
docker-compose build --no-cache frontend   


docker-compose up --build

