#Run a basic set
sudo service redis_6379 start
redis-cli hmset $1 "Author" $2 "Title" $3 "Publication Date"  $4 
sudo service redis_6379 stop
