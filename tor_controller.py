# This program changes the tor circuit each time it runs.

import getpass
import sys

import stem
import stem.connection

from stem.control import Controller

#start and change to a new circuit

if __name__ == '__main__':
  try:
    controller = Controller.from_port()
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

  print("Tor is changing circuit...")
  try:
    controller.new_circuit()
#     controller.signal(Signal.NEWNYM)
  except Exception as e:
    print("Error creating new circuit")
  controller.close()
