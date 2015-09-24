#Get all keys and values for a given hashmap
sudo service redis_6379 start
redis-cli hgetall $1
sudo service redis_6379 stop
