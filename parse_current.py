import os,sys,stem,time,pygeoip,geoip.database
from stem.descriptor import DocumentHandler, parse_file

GEOIP_FILENAME = "GeoLite2-City.mmdb"
geoip_reader = None

def main():
  
if __name__=='__main__':
  # Make sure we have a GeoIP database (maxmind)
  if not os.path.isfile(GEOIP_FILENAME):
    print("%s not found. It must be in the same directory as this script." % GEOIP_FILENAME)
    print("Get the Maxmind city database here:")
    print("-> https://dev.maxmind.com/geoip/legacy/geolite")
    sys.exit(1)
