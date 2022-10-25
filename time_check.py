from datetime import datetime
import time,threading

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
    
# if __name__ == "__main_":
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
  
  guard_thread.start()
  middle_thread.start()
  exit_thread.start()
  
  guard_thread.join()
  middle_thread.join()
  exit_thread.join()
