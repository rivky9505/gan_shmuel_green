#!/bin/bash

cd weighttest
git clone git@github.com:greendeveleap/gan_shmuel_green.git
cd gan_shmuel_green
git checkout weight
cd ..

#create logfile
touch "$(pwd)"/endtoend/logs/end2endreport.log

#dockerize
docker-compose up --build -d
sleep 30 #wait for docker to fully go up
python3 "$(pwd)"/endtoend/endtoendWeight.py
sleep 3 
docker-compose down

#checklog
status=$(python3 testlog.py)

#print 0 if all tests pass else 1
if [ $status -eq 0 ]
then
    echo 0
else
    echo 1
fi

#remove log+repo+docker images
rm -rf gan_shmuel_green
rm "$(pwd)"/endtoend/logs/end2endreport.log
docker rmi $(docker images -q) --force
