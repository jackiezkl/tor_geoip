import csv

def main():
  with open ('./data/2022-10-08-14-00-00-00-ping_exit_result.csv') as exit_relays:
    relay_list_reader = csv.reader(exit_relays)
    fields = next(relay_list_reader)
    for row in relay_list_reader:
      rows.append(row[1])
      print(rows)

if __name__ == '__main__':
  main()
