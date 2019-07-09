
import obd 
from obd import OBDCommand,Unit,ECU
from datetime import datetime
import time
import json
#https://stackoverflow.com/questions/51252910/obd-python-unable-to-get-vin-number
#cars support the 0902 command (mode 9 PID 2) to get the VIN. 

obd.logger.setLevel(obd.logging.DEBUG)

##print(type(obd.commands.SPEED ))
#print(obd.commands)
#connection = obd.Async()

# print(type(OBDResponse))
# print(help(OBDResponse))
# print(dir(OBDResponse))

def bytes_to_int(bytes):
    result = 0

    for b in bytes:
        result = result * 256 + int(b)

    return result

def vin(messages):
    """ decoder for RPM messages """
    print("the msg is : "+ str(messages))
    d = messages[0].data # only operate on a single message
    d = d[2:] # chop off mode and PID bytes
    v = bytes_to_int(d) / 4.0  # helper function for converting byte arrays to ints
    return v  # construct a Pint Quantity

c = OBDCommand("VIN",           # name
           "VIN NUMBER",    # description
           b"0902",         # command
           17,              # number of return bytes to expect
           vin,             # decoding function
           ECU.ENGINE,      # (optional) ECU filter
           True)            # (optional) allow a "01" to be added for speed
o = obd.OBD()
o.supported_commands.add(c)
o.query(c)
print('Data: ' + str(datetime.datetime.now()) + ' -- VIN NUMBER: '+str(o.query(c)))

obdVals = {}
obdVals['DEVICE_ID']='RaspbereyPi_bf4e'
obdVals['TIME_ISO']=datetime.now().isoformat()
obdVals['TIME']=time.time()
print(obdVals)

status=o.query(obd.commands["STATUS"]).value
print(help(status))
print(dir(status))
print(status.ignition_type)
print(status.DTC_count)
print(status.MIL)
vals=vars(status)
obdVals.update(vals)
print(obdVals)