import subprocess

tor_proc = subprocess.Popen(['tor','-f','data/torrc'],stdout=subprocess.PIPE)
  print("  [+] Tor started in the background. Collecting circuit information now...")
  while True:
    line = tor_proc.stdout.readline()
    print(line.decode().rstrip())
    if "Bootstrapped 100% (done): Done" in line.decode().rstrip():
      try:
        while True:
          print("test 2")
      except KeyboardInterrupt:
        print("[+] Progress manually stopped, gracefully existing...")
#         tor_proc.kill()
#         sys.exit(0)
#         os._exit(0)
