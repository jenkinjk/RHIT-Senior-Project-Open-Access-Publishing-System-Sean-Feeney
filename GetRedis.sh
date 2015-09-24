#Run a basic get
sudo service redis_6379 start
redis-cli get $1
sudo service redis_6379 stop
