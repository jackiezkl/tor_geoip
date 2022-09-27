# tor_geoip

Original file was borrowed from https://github.com/dgoulet/tor-parser/

Made some change because of the discontinued GeoLite database from maxmind.

to use geoipupdate, run the following command:

sudo add-apt-repository ppa:maxmind/ppa
sudo apt update
sudo apt install geoipupdate

create /usr/local/etc/GeoIP.conf
enter the following content
AccountID 
LicenseKey 
EditionIDs GeoLite2-ASN GeoLite2-City GeoLite2-Country
