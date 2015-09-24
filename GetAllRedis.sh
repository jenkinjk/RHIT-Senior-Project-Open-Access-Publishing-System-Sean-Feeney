#Run a basic set
sudo service redis_6379 start
redis-cli hgetall $1
sudo service redis_6379 stop
