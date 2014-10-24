
FROM sdhibit/rpi-raspbian

RUN apt-get update
RUN apt-get upgrade --yes
RUN \
  sudo apt-get install vim git-core espeak python-dev python-pip bison libasound2-dev libportaudio-dev python-pyaudio --yes && \
  sudo apt-get install -y libsox-dev libsox-fmt-all curl libav-tools supervisor

RUN sed 's/options snd-usb-audio index=-2/options snd-usb-audio index=0' /etc/modprobe.d/alsa-base.conf

ADD bash_profile ~/.bash_profile

RUN \
  wget http://downloads.sourceforge.net/project/cmusphinx/sphinxbase/0.8/sphinxbase-0.8.tar.gz && \
  wget http://downloads.sourceforge.net/project/cmusphinx/pocketsphinx/0.8/pocketsphinx-0.8.tar.gz && \
  tar -zxvf sphinxbase-0.8.tar.gz && \
  tar -zxvf pocketsphinx-0.8.tar.gz && \
  cd ~/sphinxbase-0.8/ && \
  ./configure --enable-fixed && \
  make && \
  sudo make install && \
  cd ~/pocketsphinx-0.8/ && \
  ./configure && \
  make && \
  sudo make install

RUN apt-get install subversion autoconf libtool automake gfortran g++ --yes

RUN \
  svn co https://svn.code.sf.net/p/cmusphinx/code/trunk/cmuclmtk/ && \
  cd cmuclmtk/ && \
  ./autogen.sh && sudo make && sudo make install


RUN \
  wget http://distfiles.macports.org/openfst/openfst-1.3.3.tar.gz && \
  wget https://mitlm.googlecode.com/files/mitlm-0.4.1.tar.gz && \
  wget https://m2m-aligner.googlecode.com/files/m2m-aligner-1.2.tar.gz && \
  wget https://phonetisaurus.googlecode.com/files/phonetisaurus-0.7.8.tgz && \
  wget http://phonetisaurus.googlecode.com/files/g014b2b.tgz && \
  tar -xvf m2m-aligner-1.2.tar.gz && \
  tar -xvf openfst-1.3.3.tar.gz && \
  tar -xvf phonetisaurus-0.7.8.tgz && \
  tar -xvf mitlm-0.4.1.tar.gz && \
  tar -xvf g014b2b.tgz && \
  cd ~/openfst-1.3.3/ && \
  sudo ./configure --enable-compact-fsts --enable-const-fsts --enable-far --enable-lookahead-fsts --enable-pdt && \
  sudo make install && \
  cd ~/m2m-aligner-1.2/ && \
  sudo make

#Build MITLMT:

RUN \
  cd ~/mitlm-0.4.1/ && \
  sudo ./configure && \
  sudo make install && \
  cd ~/phonetisaurus-0.7.8/ && \
  cd src && \
  sudo make && \
  sudo cp ~/m2m-aligner-1.2/m2m-aligner /usr/local/bin/m2m-aligner && \
  sudo cp ~/phonetisaurus-0.7.8/phonetisaurus-g2p /usr/local/bin/phonetisaurus-g2p && \
  cd ~/g014b2b/ && \
  ./compile-fst.sh
  mv ~/g014b2b ~/phonetisaurus

RUN \
  git clone https://github.com/chriswijones/jasper-client.git jasper && \
  sudo pip install --upgrade setuptools && \
  sudo pip install -r jasper/client/requirements.txt && \
  chmod +x jasper/jasper.py

#create the jasper profile
RUN \
  cd ~/jasper/client && \
  python populate.py