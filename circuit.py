# This file gets the current circuit information from tor.
# It defaults to use COntrolPort 9051, so before running this 
# file, make sure the tor is running in the background. 

from stem import CircStatus
from stem.control import Controller
import pygeoip
import geoip2.database

GEOIP_FILENAME = "GeoLite2-City.mmdb"
geoip_reader = None



def geo_ip_lookup(ip_address):
    record = geoip_reader.city(ip_address)
    if record is None:
        return ("unknown")
    return (record.country.iso_code)

if __name__ == '__main__':
  geoip_reader = geoip2.database.Reader('/usr/share/GeoIP/%s' % GEOIP_FILENAME)
  
  with Controller.from_port(port = 9051) as controller:
    controller.authenticate()

    for circ in sorted(controller.get_circuits()):
      if circ.status != CircStatus.BUILT:
        continue

      print("Circuit %s (%s)" % (circ.id, circ.purpose))

      for i, entry in enumerate(circ.path):
#         div = '+' if (i == len(circ.path) - 1) else '|'
        fingerprint, nickname = entry

        desc = controller.get_network_status(fingerprint, None)
        address = desc.address if desc else 'unknown'
        country = geo_ip_lookup(address)

        print(" %s- %s (%s, %s, %s)" % (div, fingerprint, nickname, address, country))
