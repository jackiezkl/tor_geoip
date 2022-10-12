import csv

def main():
  fields = []
  rows = ''
  
  with open ('./data/2022-10-08-14-00-00-ping_exit_result.csv') as exit_relays:
    relay_list_reader = csv.reader(exit_relays)
    fields = next(relay_list_reader)
    for row in relay_list_reader:
      rows = rows + row[1] + ','
  rows = rows[:-1]
  print(rows)
  
  with open('torrc', 'w') as tor_config:
    tor_config.write('SOCKSPort 172.17.0.1:9050\n')
    tor_config.write('\n')
    tor_config.write('EntryNodes {us} StrictNodes 1\n')
    tor_config.write('MiddleNodes {us} StrictNodes 1\n')
    tor_config.write('ExitNodes '+rows+'\n')
    tor_config.write('\n')
    tor_config.write('ControlPort 9051\n')
    
  tor_config.close()
  
if __name__ == '__main__':
  main()
