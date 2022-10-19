import subprocess,time

# tor_proc = subprocess.Popen(['tor','-f','data/torrc'])
# print('building tor circuit...')

# time.sleep(20)

proc = subprocess.Popen(['python3','circuit.py'],stdout=subprocess.PIPE)
while True:
  line = proc.stdout.readline()
  if not line:
    break
  print(line.decode().rstrip())
