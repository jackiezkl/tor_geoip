import datetime

def check_time(time_of_consensus, collection_length):
  hour = time_of_consensus.split("-")
  int_hour = (int(hour[0])+collection_length)%24
  q = datetime.datetime.now().hour
  
  
  if int_hour == q:
    tor_proc.kill()
    sys.exit()
    os._exit()
  else:
    continue
  


if __name__=="__main__":
  while True:
    check_time("02-00-00",1)
