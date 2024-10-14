echo on
docker-compose down
docker-compose pull
docker system df
docker builder prune -f
docker system df
docker-compose up -d
echo "program was rebuilded and running!"
