import subprocess,time,getpass,sys,stem
from stem import CircStatus
from stem.control import Controller
import pygeoip
import geoip2.database
import stem.connection

from stem.control import Controller

GEOIP_FILENAME = "GeoLite2-City.mmdb"
geoip_reader = None

def geo_country_iso_lookup(ip_address):
  record = geoip_reader.city(ip_address)
  if record is None:
      return ("unknown")
  return (record.country.iso_code)


def record_circuit():
  circuit_csv_filename = 'data/circuit.csv'

# def check_circuit(date_of_consensus,time_of_consensus):
#   circuit_csv_filename = 'data/%s-%s-all_node_info.csv' % (date_of_consensus,time_of_consensus)

  csv = open(circuit_csv_filename, 'w+')

  csv.write('Circuit ID,Circuit Purpose,Fingerprint,Nickname,IP,Country Origin\n')
  print("  [+] Created CSV file: %s" % (circuit_csv_filename))



  with Controller.from_port(port = 9051) as controller:
    controller.authenticate()

    for circ in sorted(controller.get_circuits()):
      if circ.status != CircStatus.BUILT:
        continue

      for i, (fingerprint, nickname) in enumerate(circ.path):

        desc = controller.get_network_status(fingerprint, None)
        address = desc.address if desc else 'unknown'
        country = geo_country_iso_lookup(address)

        csv.write("%s,%s,%s,%s,%s,%s\n" % (circ.id, circ.purpose, fingerprint, nickname, address, country))

def change_circuit():
  try:
    controller = Controller.from_port(port=9051)
  except stem.SocketError as exc:
    print("Unable to connect to tor on port 9051: %s" % exc)
    sys.exit(1)

  try:
    controller.authenticate()
  except stem.connection.MissingPassword:
    pw = getpass.getpass("Controller password: ")

    try:
      controller.authenticate(password = pw)
    except stem.connection.PasswordAuthFailed:
      print("Unable to authenticate, password is incorrect")
      sys.exit(1)
  except stem.connection.AuthenticationFailure as exc:
    print("Unable to authenticate: %s" % exc)
    sys.exit(1)

  print("  [+] Tor is changing circuit...")
  try:
    controller.new_circuit()
#     controller.signal(Signal.NEWNYM)
  except Exception as e:
    print("Error creating new circuit")
  controller.close()

if __name__ == '__main__':
  geoip_reader = geoip2.database.Reader('/usr/share/GeoIP/%s' % GEOIP_FILENAME)
  
  proc = subprocess.Popen(['python3','circuit.py'],stdout=subprocess.PIPE)
  while True:
    line = proc.stdout.readline()
    if "Bootstrapped 100% (done): Done" in line.decode().rstrip():
      while True:
        change_circuit()
        time.sleep(1)
        record_circuit()
        time.sleep(1)


#   tor_proc = subprocess.Popen(['tor','-f','data/torrc'])
#   print('building tor circuit...')

#   time.sleep(20)
  

