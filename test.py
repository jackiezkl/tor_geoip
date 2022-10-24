import subprocess,time
import tor_controller, circuit

# tor_proc = subprocess.Popen(['tor','-f','data/torrc'])
# print('building tor circuit...')

# time.sleep(20)

proc = subprocess.Popen(['python3','circuit.py'],stdout=subprocess.PIPE)
while True:
  change_circuit()
  time.sleep(1)
  record_circuit()
  time.sleep(1)
