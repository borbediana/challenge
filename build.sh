#!/bin/bash

echo "-----Start executing build.sh-----"

if [ -z "$1" ]
   then 
	echo "Sources located at: "$1
   else 
	echo "No sources to build. Exiting!"
fi

echo "-----Clean environment-----"
docker system prune -f

docker build $1 -f $1/dockerfile-compile -t runner 2> error_file
ERROR=$(<$1/error_file)

if [ -z "$ERROR" ]
   then 
	echo "Build successful!"
   else 
	echo "Build failed!"
	exit 1
fi

docker run --name runner-container --detach -t runner

if [ -d $1/target ]
   then
	echo "Target foldet exists! Cleaning it!"
	rm -rf $1/target
fi

mkdir $1/target

docker cp runner-container:/workspace/HelloWorld.class $1/target/
docker stop runner-container

#docker build . -f dockerfile-app -t app
#docker run --name app-container -t app

# leave a clean environment
docker system prune -f

echo "-----Finished executing build.sh-----"
