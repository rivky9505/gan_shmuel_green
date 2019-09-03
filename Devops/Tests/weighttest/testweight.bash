#!/bin/bash


git clone git@github.com:greendeveleap/gan_shmuel_green.git
cd gan_shmuel_green
git checkout master
cd ..
touch "$(pwd)"/endtoend/logs/end2endreport.log
docker-compose up --build -d
sleep 5
python3 "$(pwd)"/endtoend/endtoendWeight.py
sleep 5
docker-compose down
status=$(python3 testlog.py)
echo status = $status

if [ $status -eq 0 ]
then
    echo 0
else
    echo 1
fi


rm -rf gan_shmuel_green
rm "$(pwd)"/endtoend/logs/end2endreport.log

