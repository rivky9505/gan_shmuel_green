#!/bin/bash
SCRIPTPATH="$( cd "$(dirname "$0")" ; pwd -P)"

cd "$SCRIPTPATH"
git clone https://github.com/greendeveleap/gan_shmuel_green.git
cd gan_shmuel_green
git checkout master
cd ..

#create logfile
touch "$SCRIPTPATH"/endtoend/logs/end2endreport.log

#dockerize
#cd "$SCRIPTPATH
docker-compose up --build -d
sleep 30 #wait for docker to fully go up
python3 "$SCRIPTPATH"/endtoend/endtoendWeight.py
sleep 3 
docker-compose down

#checklog
status=$(sudo python3 testlog.py)

#remove log+repo+docker images
rm -rf gan_shmuel_green
rm "$SCRIPTPATH"/endtoend/logs/end2endreport.log
docker rmi $(sudo docker images -q) --force

#print 0 if all tests pass else 1
if [ $status -eq 0 ]
then
    return 0
else
    return 1
fi
