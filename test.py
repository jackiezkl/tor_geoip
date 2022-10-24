import subprocess,time
from tor_controller import change_circuit
from circuit import geo_ip_lookup,record_circuit
from stem import CircStatus
from stem.control import Controller
import pygeoip
import geoip2.database

GEOIP_FILENAME = "GeoLite2-City.mmdb"
geoip_reader = None

# tor_proc = subprocess.Popen(['tor','-f','data/torrc'])
# print('building tor circuit...')

# time.sleep(20)

proc = subprocess.Popen(['python3','circuit.py'],stdout=subprocess.PIPE)
while True:
  change_circuit()
  time.sleep(1)
  record_circuit()
  time.sleep(1)
