import csv

with open('data/latest_relays-2022-09-29-15:00:00.csv') as latest_relays:
  heading = next(latest_relays)
  
  relay_reader = csv.reader(latest_relays)
  
  for row in relay_reader:
    line = row
    if 'E' in line[2] then:
      if line[6] == 'US' then:
      print(line[0]+':'+line[3])
