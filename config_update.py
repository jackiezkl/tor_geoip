import os, csv, sys, stem, time, linecache, pygeoip, threading, subprocess
import geoip2.database
from stem.descriptor import DocumentHandler, parse_file
from stem.descriptor.remote import DescriptorDownloader
from stem.control import Controller
import stem.connection
from ping3 import ping
from stem import CircStatus
from datetime import datetime
from os.path import exists

GEOIP_FILENAME = "GeoLite2-City.mmdb"
geoip_reader = None

# ip address lookup for the country, city and state
def geo_ip_lookup(ip_address):
    record = geoip_reader.city(ip_address)
    if record is None:
        return (False, False, False)
    return (record.country.iso_code, record.city.name, record.subdivisions.most_specific.name)
  
# create the csv file to put the processed consensus info
def create_csv_file(date_of_consensus,time_of_consensus):
    path_to_all_node_info_csv_file = 'data/%s-%s-all_node_info.csv' % \
            (date_of_consensus,time_of_consensus)
    csv = open(path_to_all_node_info_csv_file, 'w+')

    csv.write('Name,Fingerprint,Flags,IP,OrPort,BandWidth,CountryCode,City,State\n')
    print("  [+] Created CSV file: %s" % (path_to_all_node_info_csv_file))
    return csv,path_to_all_node_info_csv_file

# process the latest consensus, save the extracted info to csv file.
def generate_csv(consensus, path_to_file, date_of_consensus, time_of_consensus):
  csv_fill, node_file_path = create_csv_file(date_of_consensus,time_of_consensus)
  print("  [+] Filling in the relay nodes information to CSV file...")
  for desc in consensus.routers.values():
    country, city, state = geo_ip_lookup(desc.address)

    if city is False and country is False and state is False:
      pass
    else: 
      flag = "M"
      if stem.Flag.GUARD in desc.flags:
        flag += "G"
      if stem.Flag.EXIT in desc.flags:
        flag += "E"
      if stem.Flag.HSDIR in desc.flags:
        flag += "H"
      if stem.Flag.FAST in desc.flags:
        flag += "F"
      if stem.Flag.RUNNING in desc.flags:
        flag += "R"
      if stem.Flag.BADEXIT in desc.flags:
        flag += "B"

      csv_fill.write("%s,%s,%s,%s,%s,%s,%s,%s,%s\n" % (desc.nickname,
                                                     desc.fingerprint,flag,desc.address,desc.or_port,
                                                     float(desc.bandwidth/1000.0/1000.0),country,city,state))
  csv_fill.close()
  return node_file_path

def main():
  start_time = time.perf_counter()
  download_consensus()

  fifth_line = linecache.getline('/tmp/consensus_dump',4).split()
  date_of_consensus = fifth_line[1]
  time_of_consensus = fifth_line[2].replace(":", "-")
  commd = "cp /tmp/consensus_dump ./data/"+date_of_consensus+"-"+time_of_consensus+"-consensus"
  os.system(commd)

  path_to_file = '/tmp/consensus_dump'
  print("  [+] Reading consensus file...")
  consensus = next(parse_file(path_to_file,descriptor_type = 'network-status-consensus-3 1.0',document_handler = DocumentHandler.DOCUMENT))

  print("  [+] Generating the relay information...")
  node_file_path = generate_csv(consensus, path_to_file, date_of_consensus, time_of_consensus)

if __name__=='__main__':
  geoip_reader = geoip2.database.Reader('/usr/share/GeoIP/%s' % GEOIP_FILENAME)
#   geoip_reader = geoip2.database.Reader('./%s' % GEOIP_FILENAME)
  if not os.path.isdir("./data"):
    #os.system("rm -R ./data")
    os.mkdir("./data")
  os.system("chmod 777 data")

  main()
