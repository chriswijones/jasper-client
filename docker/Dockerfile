
FROM sdhibit/rpi-raspbian

sudo apt-get update
sudo apt-get upgrade --yes
sudo apt-get install vim git-core espeak python-dev python-pip bison libasound2-dev libportaudio-dev python-pyaudio --yes

RUN sed 's/options snd-usb-audio index=-2/options snd-usb-audio index=0' /etc/modprobe.d/alsa-base.conf

ADD bash_profile ~/.bash_profile

wget http://downloads.sourceforge.net/project/cmusphinx/sphinxbase/0.8/sphinxbase-0.8.tar.gz
wget http://downloads.sourceforge.net/project/cmusphinx/pocketsphinx/0.8/pocketsphinx-0.8.tar.gz
tar -zxvf sphinxbase-0.8.tar.gz
tar -zxvf pocketsphinx-0.8.tar.gz


cd ~/sphinxbase-0.8/
./configure --enable-fixed
make
sudo make install

cd ~/pocketsphinx-0.8/
./configure
make
sudo make install

sudo apt-get install subversion autoconf libtool automake gfortran g++ --yes

svn co https://svn.code.sf.net/p/cmusphinx/code/trunk/cmuclmtk/
cd cmuclmtk/
sudo ./autogen.sh && sudo make && sudo make install
cd ..

wget http://distfiles.macports.org/openfst/openfst-1.3.3.tar.gz
wget https://mitlm.googlecode.com/files/mitlm-0.4.1.tar.gz
wget https://m2m-aligner.googlecode.com/files/m2m-aligner-1.2.tar.gz
wget https://phonetisaurus.googlecode.com/files/phonetisaurus-0.7.8.tgz
wget http://phonetisaurus.googlecode.com/files/g014b2b.tgz

tar -xvf m2m-aligner-1.2.tar.gz
tar -xvf openfst-1.3.3.tar.gz
tar -xvf phonetisaurus-0.7.8.tgz
tar -xvf mitlm-0.4.1.tar.gz
tar -xvf g014b2b.tgz

cd openfst-1.3.3/
sudo ./configure --enable-compact-fsts --enable-const-fsts --enable-far --enable-lookahead-fsts --enable-pdt
sudo make install # come back after a really long time

cd m2m-aligner-1.2/
sudo make

#Build MITLMT:

cd mitlm-0.4.1/
sudo ./configure
sudo make install

#Build Phonetisaurus:

cd phonetisaurus-0.7.8/
cd src
sudo make

sudo cp ~/m2m-aligner-1.2/m2m-aligner /usr/local/bin/m2m-aligner
sudo cp ~/phonetisaurus-0.7.8/phonetisaurus-g2p /usr/local/bin/phonetisaurus-g2p
#Build Phonetisaurus model:

cd g014b2b/
./compile-fst.sh
#Finally, rename the following folder for convenience:

mv ~/g014b2b ~/phonetisaurus

git clone https://github.com/chriswijones/jasper-client.git jasper

sudo pip install --upgrade setuptools
sudo pip install -r jasper/client/requirements.txt

chmod +x jasper/jasper.py

#create the jasper profile
cd ~/jasper/client
python populate.py