#LOCAL RUN INSTRUCTIONS 
docker build -t providers_mysql .
docker run -it -d -e MYSQL_ROOT_PASSWORD=123  providers_mysql
docker exec -it <container_name> bash
#INSIDE CONTAINER
mysql -u root -p                      // pass = 123 

#DB COMMANDS
show databases
use <db_name>
show tables
.
.
