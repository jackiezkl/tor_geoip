import csv
from ping3 import ping

ping_result_filename = 'data/ping_result.csv'

result_fill = open(ping_result_filename, 'w+')
result_fill.write('nickname,fingerprint,ip,latency\n')

with open('data/latest_relays-2022-09-29-15:00:00.csv') as latest_relays:
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
