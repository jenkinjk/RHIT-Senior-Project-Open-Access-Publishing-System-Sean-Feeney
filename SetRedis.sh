#Run a basic set
sudo service redis_6379 start
redis-cli set $1 $2
sudo service redis_6379 stop
