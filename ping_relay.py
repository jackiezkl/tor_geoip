import csv
from ping3 import ping

with open('data/latest_relays-2022-09-29-15:00:00.csv') as latest_relays:
  heading = next(latest_relays)
  
  relay_reader = csv.reader(latest_relays)
  
  for row in relay_reader:
    line = row
    if 'E' in line[2]:
      if line[6] == 'US':
        try:
          print(line[0]+': '+line[3]+', '+str(ping(line[3], unit='ms')))
        except Exception:
          continue
