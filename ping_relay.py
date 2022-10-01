import csv

with open('data/latest_relays.csv') as latest_relays
  heading = next(latest_relays)
  
  relay_reader = csv.reader(latest_relays)
  
  for row in relay_reader:
    print(row)
