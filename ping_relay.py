import csv

with open('data/latest_relays-2022-09-29-15:00:00.csv') as latest_relays:
  heading = next(latest_relays)
  
  relay_reader = csv.reader(latest_relays)
  
  for row in relay_reader:
    line = row
    print(line[0])
