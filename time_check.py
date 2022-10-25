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
def overwrite(which_node, date_of_consensus,time_of_consensus):
  result_filepath = 'data/'+date_of_consensus+'-'+time_of_consensus+'-ping_'+which_node+'_result.csv'
  file_exist = exists(result_filepath)
  if file_exist == True:
    while True:
      user_decision = input("  [+] The "+which_node+" ping result file already exist, overwrite? (y/n):")
      if user_decision.lower() == "n" or user_decision.lower() == "no":
        print("  [+] Will not overwrite file.")
        break
      elif user_decision.lower() == "y" or user_decision.lower() == "yes":
        print("  [+] Will overwrite file...")
        return "yes"
        break
      else:
        print("  [+] Please answer 'yes' or 'no'.")
        continue
  elif file_exist == False:
    print("%s file does not exist" % which_node)
    return "does not exist"

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
    try:
      node_ping(self.path,self.option,self.date,self.time)
    except KeyboardInterrupt:
      pass

if __name__ == "__main__":
  date_of_consensus = "2022-10-25"
  time_of_consensus = "03-00-00"
  node_file_path = "data/2022-10-25-03-00-00-all_node_info.csv"

  guard_thread = pingThread(1, "ping guard", 1, node_file_path, "guard",date_of_consensus, time_of_consensus)
  middle_thread = pingThread(2, "ping middle", 2, node_file_path, "middle",date_of_consensus, time_of_consensus)
  exit_thread = pingThread(3, "ping exit", 3, node_file_path, "exit",date_of_consensus, time_of_consensus)

  guard_flag = overwrite("guard",date_of_consensus,time_of_consensus)
  middle_flag = overwrite("middle",date_of_consensus,time_of_consensus)
  exit_flag = overwrite("exit",date_of_consensus,time_of_consensus)

  if guard_flag == "yes":
    guard_thread.start()
  elif guard_flag == "does not exist":
    print("start")
    guard_thread.start()

  if middle_flag == "yes":
    middle_thread.start()
  elif middle_flag == "does not exist":
    print("start 2")
    middle_thread.start()

  if exit_flag == "yes":
    exit_thread.start()
  elif exit_flag == "does not exist":
    print("start 3")
    exit_thread.start()

  try:
    guard_thread.join()
    middle_thread.join()
    exit_thread.join()
  except (RuntimeError,KeyboardInterrupt):
    pass
