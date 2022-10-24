# This program pulls the current consensus, then extract information to form a new csv file, which contains
# the nickname, fingerprint, ip, country, city, state. With the new file, the program pings all relays that
# geolocated in US, save the nodes' information that are having round trip latency less than 100ms. At last,
# the program pull the fingerprint information to form a tor config file for the tor program. When tor runs,
# it will only picking the relays within US.

import os, csv, sys, stem, time, linecache, pygeoip, threading, subprocess, 
import geoip2.database
from stem.descriptor import DocumentHandler, parse_file
from stem.descriptor.remote import DescriptorDownloader
from stem.control import Controller
import stem.connection
from ping3 import ping
from stem import CircStatus


GEOIP_FILENAME = "GeoLite2-City.mmdb"
geoip_reader = None

#multi-thread class
class pingThread (threading.Thread):
  def __init__(self, threadID, name, counter, file_path, node_option,date_of_consensus,time_of_consensus):
    threading.Thread.__init__(self)
    self.threadID = threadID
    self.name = name
    self.counter = counter
    self.path = file_path
    self.option = node_option
    self.date = date_of_consensus
    self.time = time_of_consensus
  def run(self):
    print("  [+] Pinging US %s nodes..." % self.option)
    node_ping(self.path,self.option,self.date,self.time)

#ping each node with options of guard, middle, or exit, then
#put into file if the round trip time is less than 100 ms.
def node_ping(path_to_file, which_node, date_of_consensus, time_of_consensus):
  if which_node == 'guard':
    node = 'G'
    ping_result_filename = 'data/'+date_of_consensus+'-'+time_of_consensus+'-ping_guard_result.csv'
  elif which_node == 'middle':
    node = 'M'
    ping_result_filename = 'data/'+date_of_consensus+'-'+time_of_consensus+'-ping_middle_result.csv'
  elif which_node == 'exit':
    node = 'E'
    ping_result_filename = 'data/'+date_of_consensus+'-'+time_of_consensus+'-ping_exit_result.csv'

  result_fill = open(ping_result_filename, 'w+')
  result_fill.write('nickname,fingerprint,ip,latency\n')

  with open(path_to_file) as latest_relays:
    heading = next(latest_relays)

    relay_reader = csv.reader(latest_relays)

    for row in relay_reader:
      line = row
      if node in line[2]:
        if line[6] == 'US':
          latency = ping(line[3], unit='ms')
          if latency is None:
            continue
          elif latency < 100:
            try:
              result_fill.write("%s,%s,%s,%s\n" % (line[0],line[1],line[3],str(latency)))
            except Exception:
              continue

  latest_relays.close()
  result_fill.close()
  print("  [+] Done pinging %s! Please check file data/%s-%s-ping_%s_result.csv" % (which_node,date_of_consensus,
                                                                                    time_of_consensus,which_node))

# ip address lookup for the country, city and state
def geo_ip_lookup(ip_address):
    record = geoip_reader.city(ip_address)
    if record is None:
        return (False, False)
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

# extract the wanted relay fingerprint information
def extract_relay_fingerprints(path_to_ping_result_file):
  rows = ''
  with open (path_to_ping_result_file) as exit_relays:
    relay_list_reader = csv.reader(exit_relays)
    fields = next(relay_list_reader)
    for row in relay_list_reader:
      rows = rows + row[1] + ','
  rows = rows[:-1]
  exit_relays.close()
  return rows

# write the new torrc file, and move it to place
def config_tor(date_of_consensus,time_of_consensus):
  entries = ''
  middles = ''
  exits = ''
  
  entries = extract_relay_fingerprints('data/'+date_of_consensus+'-'+time_of_consensus+'-ping_guard_result.csv')
  middles = extract_relay_fingerprints('data/'+date_of_consensus+'-'+time_of_consensus+'-ping_middle_result.csv')
  exits = extract_relay_fingerprints('data/'+date_of_consensus+'-'+time_of_consensus+'-ping_exit_result.csv')
  
  with open('data/torrc', 'w') as tor_config:
    tor_config.write('SOCKSPort 172.17.0.1:9050\n')
    tor_config.write('\n')
    tor_config.write('EntryNodes '+entries+'\n')
    tor_config.write('MiddleNodes '+middles+'\n')
    tor_config.write('ExitNodes '+exits+'\n')
    tor_config.write('\n')
    tor_config.write('ControlPort 9051\n')
    tor_config.write('ClientOnly 1')
    
  tor_config.close()
  
def geo_country_iso_lookup(ip_address):
  record = geoip_reader.city(ip_address)
  if record is None:
      return ("unknown")
  return (record.country.iso_code)

def change_circuit():
  controller = Controller.from_port(port=9051)
  controller.authenticate()
  print("  [+] Tor is changing circuit...")
  try:
    controller.new_circuit()
#     controller.signal(Signal.NEWNYM)
  except Exception as e:
    print("Error creating new circuit")
  controller.close()

def record_circuit(date_of_consensus,time_of_consensus):
  circuit_csv_filename = 'data/%s-%s-all_node_info.csv' % (date_of_consensus,time_of_consensus)
  csv = open(circuit_csv_filename, 'w+')

  csv.write('Circuit ID,Circuit Purpose,Fingerprint,Nickname,IP,Country Origin\n')
  print("  [+] Created CSV file: %s" % (circuit_csv_filename))



  with Controller.from_port(port = 9051) as controller:
    controller.authenticate()

    for circ in sorted(controller.get_circuits()):
      if circ.status != CircStatus.BUILT:
        continue

      for i, (fingerprint, nickname) in enumerate(circ.path):

        desc = controller.get_network_status(fingerprint, None)
        address = desc.address if desc else 'unknown'
        country = geo_country_iso_lookup(address)

        csv.write("%s,%s,%s,%s,%s,%s\n" % (circ.id, circ.purpose, fingerprint, nickname, address, country))
        
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
  
  guard_thread = pingThread(1, "ping guard", 1, node_file_path, "guard",date_of_consensus, time_of_consensus)
  middle_thread = pingThread(2, "ping middle", 2, node_file_path, "middle",date_of_consensus, time_of_consensus)
  exit_thread = pingThread(3, "ping exit", 3, node_file_path, "exit",date_of_consensus, time_of_consensus)
  
  guard_thread.start()
  middle_thread.start()
  exit_thread.start()
  
  guard_thread.join()
  middle_thread.join()
  exit_thread.join()

  end_time = time.perf_counter()
  
  difference = end_time - start_time
  print("  [+] Done pinging! Total time spent: %s seconds" % str(difference))
  
  print("  [+] Generating new tor config file...")
  config_tor(date_of_consensus, time_of_consensus)
  
  print("  [+] All done! New tor configure file has generated.")
  print("  [+] Starting tor with the new config...")
  tor_proc = subprocess.Popen(['tor','-f','data/torrc'])
  
  time.sleep(20)

  while true:
    chance_circuit()
    time.sleep(1)
    record_circuit(date_of_consensus,time_of_consensus)
    time.sleep(1)

if __name__=='__main__':
  geoip_reader = geoip2.database.Reader('/usr/share/GeoIP/%s' % GEOIP_FILENAME)
#   geoip_reader = geoip2.database.Reader('./%s' % GEOIP_FILENAME)
  if not os.path.isdir("./data"):
    #os.system("rm -R ./data")
    os.mkdir("./data")
  os.system("chmod 777 data")
  
  main()
