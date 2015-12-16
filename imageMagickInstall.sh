sudo apt-get update
sudo apt-get install build-essential
wget http://downloads.sourceforge.net/project/libpng/libpng16/1.6.18/libpng-1.6.18.tar.xz
tar xf libpng-1.6.18.tar.xz
cd libpng-1.6.18
./configure
sudo make
sudo make install
cd ..
sudo apt-get install libmagickwand-dev
sudo apt-get install python-wand
#wget http://www.imagemagick.org/download/ImageMagick.tar.gz
#tar xf ImageMagick.tar.gz
#cd ImageMagick-6.9.2-8
#./configure
#sudo ldconfig
#sudo make
#sudo make install
#cd ..
