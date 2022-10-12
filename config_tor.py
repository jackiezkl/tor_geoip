import csv

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

def main():
  entries = ''
  middles = ''
  exits = ''
  
  entries = extract_relay_fingerprints('./data/2022-10-08-14-00-00-ping_guard_result.csv')
  middles = extract_relay_fingerprints('./data/2022-10-08-14-00-00-ping_middle_result.csv')
  exits = extract_relay_fingerprints('./data/2022-10-08-14-00-00-ping_exit_result.csv')
  
  with open('torrc', 'w') as tor_config:
    tor_config.write('SOCKSPort 172.17.0.1:9050\n')
    tor_config.write('\n')
    tor_config.write('EntryNodes '+entries+'\n')
    tor_config.write('MiddleNodes '+middles+'\n')
    tor_config.write('ExitNodes '+exits+'\n')
    tor_config.write('\n')
    tor_config.write('ControlPort 9051\n')
    
  tor_config.close()
  
if __name__ == '__main__':
  main()
