import subprocess

proc = subprocess.Popen(['python3','circuit.py'],stdout=subprocess.PIPE)
while True:
  line = proc.stdout.readline()
  if not line:
    break
  print(line.decode().rstrip())
