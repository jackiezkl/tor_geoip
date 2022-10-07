import threading
from ping_relay import node_ping

class myThread (threading,Thread):
  def __init__(self, threadID, name, counter, file_path, node_option):
    threading.Thread.__init__(self)
    self.threadID = threadID
    self.name = name
    self.counter = counter
    self.path = file_path
    self.option = node_option
  def run(self):
    print("starting " + self.name)
    node_ping(self.path,self.option)
    print("exiting " + self.name)

thread1 = myThread(1, "Ping exit", 1, "data/all_node_info-2022-10-05-16-00-00.csv", "exit")
thread2 = myThread(2, "Ping exit", 2, "data/all_node_info-2022-10-05-16-00-00.csv", "guard")

thread1.start()
thread2.start()

thread2.join()
thread2.join()
