'''
/*
 *
 * Licensed under the Apache License, Version 2.0 (the "License").
 *
 * This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES 
 * OR CONDITIONS OF ANY KIND, either express or implied. See the 
 * License for the specific language governing permissions and 
 * limitations under the License.
 */
 '''

import logging
import time
import argparse
import json
import random
import obd
import time
import timeit

# We enable all logging messages for initial development
obd.logger.setLevel(obd.logging.DEBUG)
#obd.logger.setLevel(obd.logging.INFO)

print ("Establishing MQTT Connection")
#Get a list of all Serial ports available
print(obd.scan_serial())


print("Initilizing OBD connection...")
connection = obd.OBD()

print("OBD connection established.")
# List of commands
commands_list = ['ABSOLUTE_LOAD', 'ACCELERATOR_POS_D', 'ACCELERATOR_POS_E', 'ACCELERATOR_POS_F', 'AIR_STATUS', 'AMBIANT_AIR_TEMP', 'AUX_INPUT_STATUS', 'BAROMETRIC_PRESSURE', 'CATALYST_TEMP_B1S1', 'CATALYST_TEMP_B1S2', 'CATALYST_TEMP_B2S1', 'CATALYST_TEMP_B2S2', 'COMMANDED_EGR', 'COMMANDED_EQUIV_RATIO', 'CONTROL_MODULE_VOLTAGE', 'COOLANT_TEMP', 'DISTANCE_SINCE_DTC_CLEAR', 'DISTANCE_W_MIL', 'EGR_ERROR', 'ELM_VERSION', 'ELM_VOLTAGE', 'EMISSION_REQ', 'ENGINE_LOAD', 'ETHANOL_PERCENT', 'EVAPORATIVE_PURGE', 'EVAP_VAPOR_PRESSURE', 'EVAP_VAPOR_PRESSURE_ABS', 'EVAP_VAPOR_PRESSURE_ALT', 'FREEZE_DTC', 'FUEL_INJECT_TIMING', 'FUEL_LEVEL', 'FUEL_PRESSURE', 'FUEL_RAIL_PRESSURE_ABS', 'FUEL_RAIL_PRESSURE_DIRECT', 'FUEL_RAIL_PRESSURE_VAC', 'FUEL_RATE', 'FUEL_STATUS', 'FUEL_TYPE', 'GET_CURRENT_DTC', 'GET_DTC', 'HYBRID_BATTERY_REMAINING', 'INTAKE_PRESSURE', 'INTAKE_TEMP', 'LONG_FUEL_TRIM_1', 'LONG_FUEL_TRIM_2', 'LONG_O2_TRIM_B1', 'LONG_O2_TRIM_B2', 'MAF', 'MAX_MAF', 'MAX_VALUES', 'O2_B1S1', 'O2_B1S2', 'O2_B1S3', 'O2_B1S4', 'O2_B2S1', 'O2_B2S2', 'O2_B2S3', 'O2_B2S4', 'O2_S1_WR_CURRENT', 'O2_S1_WR_VOLTAGE', 'O2_S2_WR_CURRENT', 'O2_S2_WR_VOLTAGE', 'O2_S3_WR_CURRENT', 'O2_S3_WR_VOLTAGE', 'O2_S4_WR_CURRENT', 'O2_S4_WR_VOLTAGE', 'O2_S5_WR_CURRENT', 'O2_S5_WR_VOLTAGE', 'O2_S6_WR_CURRENT', 'O2_S6_WR_VOLTAGE', 'O2_S7_WR_CURRENT', 'O2_S7_WR_VOLTAGE', 'O2_S8_WR_CURRENT', 'O2_S8_WR_VOLTAGE', 'O2_SENSORS', 'O2_SENSORS_ALT', 'OBD_COMPLIANCE', 'OIL_TEMP', 'PIDS_A', 'PIDS_B', 'PIDS_C', 'RELATIVE_ACCEL_POS', 'RELATIVE_THROTTLE_POS', 'RPM', 'RUN_TIME', 'RUN_TIME_MIL', 'SHORT_FUEL_TRIM_1', 'SHORT_FUEL_TRIM_2', 'SHORT_O2_TRIM_B1', 'SHORT_O2_TRIM_B2', 'SPEED', 'STATUS', 'STATUS_DRIVE_CYCLE', 'THROTTLE_ACTUATOR', 'THROTTLE_POS', 'THROTTLE_POS_B', 'THROTTLE_POS_C', 'TIME_SINCE_DTC_CLEARED', 'TIMING_ADVANCE', 'WARMUPS_SINCE_DTC_CLEAR']

# wait for the connection to be established and car ignition to be turned on
while not connection.status() == obd.OBDStatus.CAR_CONNECTED:
    print("Waiting for ignition to start. Check will be performed again in 1 second")
    print(connection.status())
    time.sleep(2)

# First we check and create a list of supported sub set of commands for  the connected vehicle
supported_commands_list = []
for i in commands_list:
    c = obd.commands[i]
    if connection.supports(c):
        supported_commands_list.append(i)
    else:
        continue

messageJson_array = []
count = 0

while True:
        # Query all commands in serial fashion
        # Note this can be changed to asynchronous format if required
        for i in supported_commands_list:
            if start_10==0:
                start_10 = timeit.timeit()
            start = timeit.timeit()
            c = obd.commands[i]
            response = connection.query(c)
            x ={}
            
            python_object = {
                'Device_ID':'RaspbereyPi_bf4e',
                'time':str(response.time),
                'Parameter':str(i),
                'Command':str(response.command),
                'Value:':str(response.value)
                }
            messageJson_array.append(python_object)
            count +=1
            print(str(count) + " of " + str(10*len(supported_commands_list)) + " messages held in buffer.")
            end = timeit.timeit()
            with open('/home/pi/aws_sdk/aws-iot-device-sdk-python/samples/basicPubSub/Certs/result.json', 'a+') as f:
                for item in messageJson_array:
                    f.write("%s\n" % item)
                messageJson_array = []
                count = 0
                
