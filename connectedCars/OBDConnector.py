import logging
import json
import obd
import time
from datetime import datetime
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
portName=connection.port_name()
# the ID of the protocol being used by the ELM327
protocolId=connection.protocol_id()
#the name of the protocol being used by the ELM327
protocolName=connection.protocol_name()
# OBD connection status 
status=connection.status()

print("The connector is connected to "+portName+" with a status "+status)
print("The protocol id is "+protocolId+" and protocol name is " + protocolName)

paramTemplate = """{{ "type": "string", "optional": true, "field": "{source}" }}"""

schemaTemplate="""{{ "schema":  "type": "struct",
                        "optional": false,
                        "name": "foobar",
                        "fields": {{ [{schemaTemp}] }}
                       ,
            "payload": {payload}
}}"""

schemaLst=[]
schemaLst.append(paramTemplate.format(source="DEVICE_ID"))
schemaLst.append(paramTemplate.format(source="TIME_ISO"))
schemaLst.append(paramTemplate.format(source="TIME"))

#Prints all commands supported by the car. 
#For working in interactive mode.
#obd.print_commands()

# wait for the connection to be established and car ignition to be turned on
# while not connection.status() == obd.OBDStatus.CAR_CONNECTED:
#     print("Waiting for ignition to start. Check will be performed again in 1 second")
#     print(connection.status())
#     time.sleep(2)

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
              connection.watch(obd.commands[cmd.name])
              schemaLst.append(paramTemplate.format(source=cmd.name))

print(supported_commands_list)   
#Generate the schema           
schemaElement=",".join(schemaLst)

connection.start()

while True:
   time.sleep(1)
   obdVals = {}
   obdVals['DEVICE_ID']='RaspbereyPi_bf4e'
   obdVals['TIME_ISO']=datetime.now().isoformat()
   obdVals['TIME']=time.time()
   for cmdNm in supported_commands_list:
      if 'STATUS' == cmdNm :
         status = connection.query(obd.commands[cmdNm]).value
         if status is None:
            obdVals[cmdNm]="None"
         else :
            obdVals[cmdNm]=str(status.ignition_type)
            #vals=vars(status)
            #obdVals.update(vals)
      else :
         obdVals[cmdNm]=str(connection.query(obd.commands[cmdNm]).value)   

   obdValsJson = json.dumps(obdVals)
   print(obdValsJson)
   schemaTemplate.format(schemaTemp=schemaElement,payload=obdValsJson)
   with open('obdVals_'+time.strftime("%Y-%m-%d")+'.txt', 'a+') as obd_file:
      obd_file.write(schemaTemplate+ "\n")


connection.stop()
connection.unwatch_all()
