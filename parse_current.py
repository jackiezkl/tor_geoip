import os, sys, stem, time, linecache, pygeoip
import geoip2.database
from stem.descriptor import DocumentHandler, parse_file
from stem.descriptor.remote import DescriptorDownloader

GEOIP_FILENAME = "GeoLite2-City.mmdb"
geoip_reader = None

def generate_csv(consensus, path_to_file, year, month, day):
  print(year+"."+month+"."+day)

def download_consensus():
  downloader = DescriptorDownloader()
  try:
    consensus = downloader.get_consensus(document_handler = DocumentHandler.DOCUMENT).run()[0]
  except Exception:
    print("Couldn't download consensus file, please try again!")
    sys.exit(1)
    
  with open('/tmp/consensus_dump', 'w') as descriptor_file:
    descriptor_file.write(str(consensus))

def main():
  download_consensus()

  fifth_line = linecache.getline('/tmp/consensus_dump',4).split()
  commd = "cp /tmp/consensus_dump ./data/"+fifth_line[1]+"_"+fifth_line[2]
  os.system(commd)    

  year, month, day = [fifth_line[1].split('-')[i] for i in (0,1,2)]

  path_to_file = "/home/node11/Desktop/geoip/tor_geoip/data/"+fifth_line[1]+"_"+fifth_line[2]
  print("Reading consensus file: %s" % path_to_file)
  
  try:
    print("test1")
    consensus = next(parse_file(path_to_file,descriptor_type = 'network-status-consensus-3 1.0',document_handler = DocumentHandler.DOCUMENT))
    print("test2")
    generate_csv(consensus, path_to_file, year, month, day)
  except Exception as e:
    print("There was an error finding the file!")
    pass
  print("done") 


if __name__=='__main__':
  # Make sure we have a GeoIP database (maxmind)
  if not os.path.isfile(GEOIP_FILENAME):
    print("%s not found. It must be in the same directory as this script." % GEOIP_FILENAME)
    print("Get the Maxmind city database here:")
    print("-> https://dev.maxmind.com/geoip/legacy/geolite")
    sys.exit(1)
  geoip_reader = geoip2.database.Reader('./%s' % GEOIP_FILENAME)
  
  if not os.path.isdir("./data"):
    #os.system("rm -R ./data")
    os.mkdir("./data")
  os.system("chmod 777 data")
  
  main()
