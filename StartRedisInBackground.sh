# run this as sudo
# this specifies a config file that has daemonize yes instead of using the default which is no
redis-server ~/redis-stable/redis.conf

# you can check if server is running by tryping redis-cli
# then ping (response is PONG)
# you can shutdown server with shutdown
# redis-cli shutdown
# then quit with quit
