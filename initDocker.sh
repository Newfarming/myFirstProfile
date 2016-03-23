#!/bin/bash


cd ~/pinbot/
docker-machine start default
docker-machine env default
eval "$(docker-machine env default)"

docker-compose -f pinbot-service.yml -p service start

