sudo apt-get update
sudo apt-get install build-essential
wget http://prdownloads.sourceforge.net/libpng/libpng-1.5.4.tar.gz?download
tar xf libpng-1.5.4.tar.gz?download
cd libpng-1.5.4
./configure
sudo make
sudo make install
cd ..
sudo apt-get install libpng-dev
sudo apt-get install libmagickwand-dev
sudo apt-get install python-wand
wget http://www.imagemagick.org/download/ImageMagick.tar.gz
tar xf ImageMagick.tar.gz
cd ImageMagick-6.9.2-8
./configure
sudo ldconfig
sudo make
sudo make install
cd ..
