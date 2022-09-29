import os, sys, stem, time, linecache, pygeoip
import geoip2.database
from stem.descriptor import DocumentHandler, parse_file
from stem.descriptor.remote import DescriptorDownloader

GEOIP_FILENAME = "GeoLite2-City.mmdb"
geoip_reader = None

def create_csv_file(date,time):
    # Process the consensuses that we are interested in.
    csv_filename = 'data/latest_relays-%s-%s.csv' % \
            (date,time)
#     if os.path.exists(csv_filename):
#         os.system('rm %s' % csv_filename)
#         return None
    csv = open(csv_filename, 'w+')
    print("  [+] Creating CSV file %s" % (csv_filename))
    csv.write('Name,Fingerprint,Flags,IP,OrPort,BandWidth,CountryCode,City,State\n')
    return csv

def geo_ip_lookup(ip_address):
    record = geoip_reader.city(ip_address)
    if record is None:
        return (False, False)
    return (record.country.iso_code, record.city.name, record.subdivisions.most_specific.name)

def generate_csv(consensus, path_to_file, year, month, day, date, time):
  csv_fp = create_csv_file(date,time)
  for desc in consensus.routers.values():
    country, city, state = geo_ip_lookup(desc.address)

    if city is False and country is False and state is False:
      pass
    
    flag = "M"
    if stem.Flag.GUARD in desc.flags:
      flag += "G"
    if stem.Flag.EXIT in desc.flags:
      flag += "E"
    if stem.Flag.HSDIR in desc.flags:
      flag += "H"

    csv_fp.write("%s,%s,%s,%s,%s,%s,%s,%s,%s\n" % (desc.nickname,desc.fingerprint,flag,desc.address,desc.or_port,float(desc.bandwidth/1000.0/1000.0),country,city,state))
  csv_fp.close()

def download_consensus():
  downloader = DescriptorDownloader()
  flag = False
  while flag == False:
    try:
      consensus = downloader.get_consensus(document_handler = DocumentHandler.DOCUMENT).run()[0]
      flag = True
    except Exception:
      print("Couldn't download consensus file, trying again...")
      continue
    
  with open('/tmp/consensus_dump', 'w') as descriptor_file:
    descriptor_file.write(str(consensus))

def main():
  download_consensus()

  fifth_line = linecache.getline('/tmp/consensus_dump',4).split()
  commd = "cp /tmp/consensus_dump ./data/"+fifth_line[1]+"_"+fifth_line[2]
  os.system(commd)

  year, month, day = [fifth_line[1].split('-')[i] for i in (0,1,2)]

#   path_to_file = "/home/node11/Desktop/geoip/tor_geoip/data/"+fifth_line[1]+"_"+fifth_line[2]
  path_to_file = '/tmp/consensus_dump'
  print("Reading consensus file: %s" % path_to_file)
  
#   try:
  consensus = next(parse_file(path_to_file,descriptor_type = 'network-status-consensus-3 1.0',document_handler = DocumentHandler.DOCUMENT))
  generate_csv(consensus, path_to_file, year, month, day, fifth_line[1], fifth_line[2])
#   except Exception as e:
#     print("There was an error finding the file!")
#     pass


if __name__=='__main__':
  # Make sure we have a GeoIP database (maxmind)
  geoip_reader = geoip2.database.Reader('/usr/share/GeoIP/%s' % GEOIP_FILENAME)
  
  if not os.path.isdir("./data"):
    #os.system("rm -R ./data")
    os.mkdir("./data")
  os.system("chmod 777 data")
  
  main()
