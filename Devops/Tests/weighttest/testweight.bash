git checkout weight
git clone git@github.com:greendeveleap/gan_shmuel_green.git
touch "$(pwd)"/endtoend/logs/end2endreport.log
docker-compose up --build -d
sleep 5
python3 "$(pwd)"/endtoend/endtoendWeight.py
sleep 5
docker-compose down
rm -rf gan_shmuel_green
#rm endtoend/logs/end2endreport.log
#script to test log
#return 0 if all is 200
#return 1 if not all is 200
