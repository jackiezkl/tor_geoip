import os, sys, stem, time, linecache, pygeoip
import geoip2.database
from stem.descriptor import DocumentHandler, parse_file
from stem.descriptor.remote import DescriptorDownloader

GEOIP_FILENAME = "GeoLite2-City.mmdb"
geoip_reader = None

def download_consensus():
  downloader = DescriptorDownloader()
  consensus = downloader.get_consensus(document_handler = DocumentHandler.DOCUMENT).run()[0]

  with open('/tmp/consensus_dump', 'w') as descriptor_file:
    descriptor_file.write(str(consensus))

def filecopy():
  fifth_line = linecache.getline('/tmp/consensus_dump',4).split()
  commd = "cp /tmp/consensus_dump ./data/"+fifth_line[1]+"_"+fifth_line[2]
  os.system(commd)

def main():
  try:
    download_consensus()
    filecopy()
  except Exception:
    try:
      download_consensus()
      filecopy()
    except Exception:
        try:
          download_consensus()
          filecopy()
        except Exception:
          pass

if __name__=='__main__':
  # Make sure we have a GeoIP database (maxmind)
  if not os.path.isfile(GEOIP_FILENAME):
    print("%s not found. It must be in the same directory as this script." % GEOIP_FILENAME)
    print("Get the Maxmind city database here:")
    print("-> https://dev.maxmind.com/geoip/legacy/geolite")
    sys.exit(1)
  geoip_reader = geoip2.database.Reader('./%s' % GEOIP_FILENAME)
  
  if not os.path.isdir("./data"):
    os.mkdir("./data")
  
  main()
