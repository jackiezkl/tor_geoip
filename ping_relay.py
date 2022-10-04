import csv,sys
from ping3 import ping

if len(sys.argv) == 1:
  print("Usage: python3 ping_relay.py [path to latest_relays file from parse_current.py]")
  sys.exit(1)

path_to_file = sys.argv[1]

ping_result_filename = 'data/ping_result.csv'

result_fill = open(ping_result_filename, 'w+')
result_fill.write('nickname,fingerprint,ip,latency\n')

with open(path_to_file) as latest_relays:
  heading = next(latest_relays)
  
  relay_reader = csv.reader(latest_relays)
  
  for row in relay_reader:
    line = row
    if 'E' in line[2]:
      if line[6] == 'US':
        try:
          result_fill.write("%s,%s,%s,%s\n" % (line[0],line[1],line[3],str(ping(line[3], unit='ms'))))
        except Exception:
          continue
