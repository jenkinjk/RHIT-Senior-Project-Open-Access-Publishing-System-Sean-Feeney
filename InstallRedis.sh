#Installation of Redis
sudo apt-get update
sudo apt-get install build-essential
sudo apt-get tcl8.6
wget http://download.redis.io/releases/redis-stable.tar.gz
tar xzf redis-stable.tar.gz
cd redis-stable
make
sudo make install
