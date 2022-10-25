from datetime import datetime
import time,threading,csv
from ping3 import ping
from os.path import exists

# def check_time(time_of_consensus, collection_length):
#   hour = time_of_consensus.split("-")
#   int_hour = (int(hour[0])+collection_length)%24
#   q = datetime.utcnow().hour
  
  
#   if int_hour == q:
#     print("got it")
# #     tor_proc.kill()
#     sys.exit()
#     os._exit()

# def check(i):
#   if i == 10:
#     return "F"
#   else:
#     return "T"
    
# if __name__ == "__main__":
#   i = 0
#   l = "T"
#   while l == "T":
#     print(i)
#     l = check(i)
#     i+=1
# if __name__=="__main__":
#   while True:
#     check_time("02-00-00",1)
#     time.sleep(1)
def node_ping(path_to_file, which_node, date_of_consensus, time_of_consensus):
  if which_node == 'guard':
    node = 'G'
    ping_result_filename = 'data/'+date_of_consensus+'-'+time_of_consensus+'-ping_guard_result.csv'
  elif which_node == 'middle':
    node = 'M'
    ping_result_filename = 'data/'+date_of_consensus+'-'+time_of_consensus+'-ping_middle_result.csv'
  elif which_node == 'exit':
    node = 'E'
    ping_result_filename = 'data/'+date_of_consensus+'-'+time_of_consensus+'-ping_exit_result.csv'

  does_file_exist = exists(ping_result_filename)
  if does_file_exist == True:
    while True:
      over_write = input("  [+] The ping file already exist, overwrite? (y/n):")
      if over_write.lower() == "n" or over_write.lower() == "no":
        print("  [+] Will not over write file.")
        return
      elif over_write.lower() == "y" or over_write.lower() == "yes":
        print("  [+] Overwriting file...")
        break
      else:
        print("  [+] Please answer 'yes' or 'no'.")
        continue


  result_fill = open(ping_result_filename, 'w+')
  result_fill.write('nickname,fingerprint,ip,latency\n')

  with open(path_to_file) as latest_relays:
    heading = next(latest_relays)

    relay_reader = csv.reader(latest_relays)

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
  print("  [+] Done pinging %s! Please check file data/%s-%s-ping_%s_result.csv" % (which_node,date_of_consensus,
                                                                                    time_of_consensus,which_node))

class pingThread (threading.Thread):
  def __init__(self, threadID, name, counter, file_path, node_option,date_of_consensus,time_of_consensus):
    threading.Thread.__init__(self)
    self.threadID = threadID
    self.name = name
    self.counter = counter
    self.path = file_path
    self.option = node_option
    self.date = date_of_consensus
    self.time = time_of_consensus
  def run(self):
    print("  [+] Pinging US %s nodes..." % self.option)
    node_ping(self.path,self.option,self.date,self.time)

if __name__ == "__main__":
  date_of_consensus = "2022-10-25"
  time_of_consensus = "03-00-00"
  node_file_path = "data/2022-10-25-03-00-00-all_node_info.csv"
  
  guard_thread = pingThread(1, "ping guard", 1, node_file_path, "guard",date_of_consensus, time_of_consensus)
  middle_thread = pingThread(2, "ping middle", 2, node_file_path, "middle",date_of_consensus, time_of_consensus)
  exit_thread = pingThread(3, "ping exit", 3, node_file_path, "exit",date_of_consensus, time_of_consensus)
  
  exit_thread.start()
  exit_thread.join()

  guard_thread.start()
  guard_thread.join()

  middle_thread.start()
  middle_thread.join()

