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
  
  filename = ''
  
  
if __name__ == '__main__':
  main()
