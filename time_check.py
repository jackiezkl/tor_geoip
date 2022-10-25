from datetime import datetime
import time

def check_time(time_of_consensus, collection_length):
  hour = time_of_consensus.split("-")
  int_hour = (int(hour[0])+collection_length)%24
  q = datetime.utcnow().hour
  
  
  if int_hour == q:
    print("got it")
#     tor_proc.kill()
    sys.exit()
    os._exit()

def check(i):
  if i == 10:
    return "F"
  else:
    print(i)
    return "T"
    
if __name__ == "__main_":
  i = 0
  l = "T"
  while l == "T":
    l = check(i)
    i+=1
# if __name__=="__main__":
#   while True:
#     check_time("02-00-00",1)
#     time.sleep(1)
    
