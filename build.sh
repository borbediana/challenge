#!/bin/bash

echo "-----Start executing build.sh-----"

echo "-----Clean environment-----"
docker system prune -f

docker build . -f dockerfile-compile -t runner
docker run --name runner-container --detach -t runner
docker cp runner-container:/workspace/HelloWorld.class ./
docker stop runner-container

docker build . -f dockerfile-app -t app
docker run --name app-container -t app

# leave a clean environment
docker system prune -f

echo "-----Finished executing build.sh-----"
