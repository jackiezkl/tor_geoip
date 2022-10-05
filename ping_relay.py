import csv,sys
from ping3 import ping


def node_ping(path_to_file, which_node):
  if which_node == 'guard':
    node = 'G'
    ping_result_filename = 'data/ping_guard_result.csv'
  elif which_node == 'middle':
    node = 'M'
    ping_result_filename = 'data/ping_middle_result.csv'
  elif which_node == 'exit':
    node = 'E'
    ping_result_filename = 'data/ping_exit_result.csv'

  result_fill = open(ping_result_filename, 'w+')
  result_fill.write('nickname,fingerprint,ip,latency\n')

  with open(path_to_file) as latest_relays:
    heading = next(latest_relays)

    relay_reader = csv.reader(latest_relays)
#     print("[+] Start pinging, hold on...")
    for row in relay_reader:
      line = row
      if node in line[2]:
        if line[6] == 'US':
          latency = ping(line[3], unit='ms')
          if latency is None:
            continue
          elif latency < 100:
            try:
              result_fill.write("%s,%s,%s,%s\n" % (line[0],line[1],line[3],str(latency)))
            except Exception:
              continue

  latest_relays.close()
  result_fill.close()
  print("  [+] Done! Please check file ./data/ping_%s_result.csv" % which_node)

if __name__ == '__main__':
  if len(sys.argv) < 3:
    print("\nUsage: python3 ping_guard.py [path to latest_relays file from parse_current.py] guard | middle | exit")
    sys.exit(1)
  
  path_to_file = sys.argv[1]
  which_node = sys.argv[2]
  node_ping(path_to_file, which_node)

