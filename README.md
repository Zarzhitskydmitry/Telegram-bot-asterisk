# Telegram-bot-python
wget https://www.python.org/ftp/python/3.9.10/Python-3.9.10.tar.x
yum install xz -y
tar -xpJf Python-3.9.10.tar.xz
cd Python-3.9.10
yum groupinstall "Development tools" -y
yum install zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel -y
./configure --enable-optimizations
make install
ln -s /usr/local/bin/python3 /usr/bin/python3
pip3 install python-telegram-bot --upgrade

chmod +x ./bot.sh
chmod +x ./apache_status.sh
chmod +x ./aster_trunk.sh
chmod +x ./sip_show_registry.sh
chmod +x ./botsipr.sh
chmod +x ./cdr-clear.sh


ln -s ./apache_status.sh /usr/local/sbin/apachestatus
ln -s ./aster_trunk.sh /usr/local/sbin/astertrunk
ln -s ./botsipsr.sh /usr/local/sbin/botsipsr
ln -s ./botsipr.sh /usr/local/sbin/sip_r
ln -s ./sip_show_registry.sh /usr/local/sbin/sip_show_registry
