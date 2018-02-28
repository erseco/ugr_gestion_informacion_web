# Search engine with Lucene

## How to install

### Install dependencies
```bash
sudo apt-get update
sudo apt-get install -y ant g++ python-dev python-setuptools python-pip default-jdk-headless
sudo pip install --upgrade pip
sudo pip install setuptools --upgrade
```



### Downloads and extract pylucene
```bash
wget http://apache.rediris.es/lucene/pylucene/pylucene-4.10.1-1-src.tar.gz
tar -zxvf pylucene-4.10.1-1-src.tar.gz
```

### Build and install jcc
```bash
cd pylucene-4.10.1-1/jcc
sed -i s/java-7-openjdk-amd64/java-8-openjdk-amd64/ setup.py
python setup.py build
sudo python setup.py install
cd ..
```

### Edit Makefile
```
# Linux     (Ubuntu 11.10 64-bit, Python 2.7.2, OpenJDK 1.7, setuptools 0.6.16)
# Be sure to also set JDK['linux2'] in jcc's setup.py to the JAVA_HOME value
# used below for ANT (and rebuild jcc after changing it).
PREFIX_PYTHON=/usr
ANT=JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64 /usr/bin/ant
PYTHON=$(PREFIX_PYTHON)/bin/python
JCC=$(PYTHON) -m jcc --shared
NUM_FILES=8
```

### Build and install pylucene
```bash
make
sudo make install
```



### Install Flask
```bash
sudo pip install Flask-WTF flask-table
```

### Redirect 8080 to 80
```bash
sudo iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to-port 8080
```

## Using the programs

### Indexer
```bash
python index.py iniciativas08 palabras_vacias_utf8.txt index
```

### Search Engine
```bash
python search.py index
```
