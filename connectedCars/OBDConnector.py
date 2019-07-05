import logging
import argparse
import json
import obd
import time

logger = logging.getLogger(__name__)
# We enable all logging messages for initial development
obd.logger.setLevel(obd.logging.DEBUG)
#obd.logger.setLevel(obd.logging.INFO)

#Get a list of all Serial ports available
print(obd.scan_serial())

print("Initilizing OBD connection...")
#connection = obd.OBD()
connection = obd.Async() # same constructor as 'obd.OBD()'
print("OBD connection established.")

#DEBUG INFO
# the name of the currently connected port
portName=obd.port_name()
# the ID of the protocol being used by the ELM327
protocolId=obd.protocol_id()
#the name of the protocol being used by the ELM327
protocolName=obd.protocol_name()
# OBD connection status 
status=obd.status()



#Prints all commands supported by the car. 
#For working in interactive mode.
#obd.print_commands()

# wait for the connection to be established and car ignition to be turned on
while not connection.status() == obd.OBDStatus.CAR_CONNECTED:
    print("Waiting for ignition to start. Check will be performed again in 1 second")
    print(connection.status())
    time.sleep(2)

# First we check and create a list of supported sub set of commands for  the connected vehicle
supported_commands_list = []

for command_list in obd.commands.modes:
    for cmd in command_list:
        if cmd is None:
           continue  # this command is reserved
        elif (cmd.mode >= 1) and (cmd.mode <= 9) :
           #print(cmd.name)
           if connection.supports(obd.commands[cmd.name]):
              supported_commands_list.append(cmd.name)


print(supported_commands_list)              

obdVals = {}
connection.watch(obd.commands["RPM"])
connection.watch(obd.commands["FUEL_STATUS"])
connection.start()

for i in range(5):
   time.sleep(5)
   obdVals["RPM"]=connection.query(obd.commands["RPM"])
   obdVals["FUEL_STATUS"]=connection.query(obd.commands["FUEL_STATUS"])

connection.stop()
connection.unwatch_all()

obdValsJson = json.dumps(obdVals)

print(obdVals)

print(obdValsJson)

with open('obdVals.txt', 'w') as obd_file:
  json.dump(obdVals, obd_file)