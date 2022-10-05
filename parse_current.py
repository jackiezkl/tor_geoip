# This program pulls the current consensus, then extract information
# to form a new csv file, which contains the nickname, fingerprint, 
# ip, country, city, state.

import os, sys, stem, time, linecache, pygeoip
import geoip2.database
from stem.descriptor import DocumentHandler, parse_file
from stem.descriptor.remote import DescriptorDownloader
from ping_relay import node_ping

GEOIP_FILENAME = "GeoLite2-City.mmdb"
geoip_reader = None

# create the csv file to put the processed consensus info
def create_csv_file(date_of_consensus,time_of_consensus):
    csv_filename = 'data/all_node_info-%s-%s.csv' % \
            (date_of_consensus,time_of_consensus)
    csv = open(csv_filename, 'w+')

    csv.write('Name,Fingerprint,Flags,IP,OrPort,BandWidth,CountryCode,City,State\n')
    print("  [+] Created CSV file: %s" % (csv_filename))
    return csv,csv_filename

# ip address lookup for the country, city and state
def geo_ip_lookup(ip_address):
    record = geoip_reader.city(ip_address)
    if record is None:
        return (False, False)
    return (record.country.iso_code, record.city.name, record.subdivisions.most_specific.name)

# process the latest consensus, save the extracted info to csv file.
def generate_csv(consensus, path_to_file, date_of_consensus, time_of_consensus):
  csv_fill, node_file_path = create_csv_file(date_of_consensus,time_of_consensus)
  print("  [+] Filling in the relay nodes information to CSV file...")
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

    csv_fill.write("%s,%s,%s,%s,%s,%s,%s,%s,%s\n" % (desc.nickname,
                                                   desc.fingerprint,flag,desc.address,desc.or_port,
                                                   float(desc.bandwidth/1000.0/1000.0),country,city,state))
  csv_fill.close()
  return node_file_path

# acquire the latest consensus
def download_consensus():
  downloader = DescriptorDownloader()
  flag = False
  while flag == False:
    try:
      consensus = downloader.get_consensus(document_handler = DocumentHandler.DOCUMENT).run()[0]
      print("  [+] Latest Tor censensus file downloaded.")
      flag = True
    except Exception:
      print("  [+] Couldn't download consensus file, trying again...")
      continue
    
  with open('/tmp/consensus_dump', 'w') as descriptor_file:
    descriptor_file.write(str(consensus))

def main():
  start_time = time.perf_counter()
  download_consensus()

  fifth_line = linecache.getline('/tmp/consensus_dump',4).split()
  date_of_consensus = fifth_line[1]
  time_of_consensus = fifth_line[2].replace(":", "-")
  commd = "cp /tmp/consensus_dump ./data/"+date_of_consensus+"-"+time_of_consensus+"-consensus"
  os.system(commd)

#   year, month, day = [fifth_line[1].split('-')[i] for i in (0,1,2)]

  path_to_file = '/tmp/consensus_dump'
  print("  [+] Reading consensus file...")
  consensus = next(parse_file(path_to_file,descriptor_type = 'network-status-consensus-3 1.0',document_handler = DocumentHandler.DOCUMENT))

  print("  [+] Generating the relay information...")
  node_file_path = generate_csv(consensus, path_to_file, date_of_consensus, time_of_consensus)
  
  print("  [+] Pinging US guard nodes...")
  node_ping(node_file_path,'guard')
  
  print("  [+] Pinging US middle nodes...")
  node_ping(node_file_path,'middle')
  
  print("  [+] Pinging US exit nodes...")
  node_ping(node_file_path,'exit')
  end_time = time.perf_counter()
  
  difference = end_time - start_time
  print("  [+] All process done! Total time spent: %s seconds" & str(difference))
if __name__=='__main__':
  geoip_reader = geoip2.database.Reader('/usr/share/GeoIP/%s' % GEOIP_FILENAME)
  
  if not os.path.isdir("./data"):
    #os.system("rm -R ./data")
    os.mkdir("./data")
  os.system("chmod 777 data")
  
  main()
