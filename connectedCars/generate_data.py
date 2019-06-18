import json
import time
import random


class obd_simulate(object):
    """
    This class will simulate obd sensor since we cannot have the
    entire setup for working with Kafka integration.
    This will create similar json objects to real data which can then be
    ingested by kafka as required.

    The objects can be stored in a json file and picked up from there,
    or they can be directly picked up as a python dict or json object and processed.
    """

    def __init__(self):
        __author__ = 'Yogesh Chaudhari'
        __version__ = '0.01'
        
        self.list_of_parameters = ['PIDS_A', 'STATUS', 'FREEZE_DTC', 'FUEL_STATUS', 'ENGINE_LOAD', 'COOLANT_TEMP', 'SHORT_FUEL_TRIM_1', 'LONG_FUEL_TRIM_1', 'SHORT_FUEL_TRIM_2', 'LONG_FUEL_TRIM_2', 'FUEL_PRESSURE', 'INTAKE_PRESSURE', 'RPM', 'SPEED', 'TIMING_ADVANCE', 'INTAKE_TEMP', 'MAF', 'THROTTLE_POS', 'AIR_STATUS', 'O2_SENSORS', 'O2_B1S1', 'O2_B1S2', 'O2_B1S3', 'O2_B1S4', 'O2_B2S1', 'O2_B2S2', 'O2_B2S3', 'O2_B2S4', 'OBD_COMPLIANCE', 'O2_SENSORS_ALT', 'AUX_INPUT_STATUS', 'RUN_TIME', 'PIDS_B', 'DISTANCE_W_MIL', 'FUEL_RAIL_PRESSURE_VAC', 'FUEL_RAIL_PRESSURE_DIRECT', 'O2_S1_WR_VOLTAGE', 'O2_S2_WR_VOLTAGE', 'O2_S3_WR_VOLTAGE', 'O2_S4_WR_VOLTAGE', 'O2_S5_WR_VOLTAGE', 'O2_S6_WR_VOLTAGE', 'O2_S7_WR_VOLTAGE', 'O2_S8_WR_VOLTAGE', 'COMMANDED_EGR', 'EGR_ERROR', 'EVAPORATIVE_PURGE', 'FUEL_LEVEL', 'WARMUPS_SINCE_DTC_CLEAR', 'DISTANCE_SINCE_DTC_CLEAR', 'EVAP_VAPOR_PRESSURE', 'BAROMETRIC_PRESSURE', 'O2_S1_WR_CURRENT', 'O2_S2_WR_CURRENT', 'O2_S3_WR_CURRENT', 'O2_S4_WR_CURRENT', 'O2_S5_WR_CURRENT', 'O2_S6_WR_CURRENT', 'O2_S7_WR_CURRENT', 'O2_S8_WR_CURRENT', 'CATALYST_TEMP_B1S1', 'CATALYST_TEMP_B2S1', 'CATALYST_TEMP_B1S2', 'CATALYST_TEMP_B2S2', 'PIDS_C', 'STATUS_DRIVE_CYCLE', 'CONTROL_MODULE_VOLTAGE', 'ABSOLUTE_LOAD', 'COMMANDED_EQUIV_RATIO', 'RELATIVE_THROTTLE_POS', 'AMBIANT_AIR_TEMP', 'THROTTLE_POS_B', 'THROTTLE_POS_C', 'ACCELERATOR_POS_D', 'ACCELERATOR_POS_E', 'ACCELERATOR_POS_F', 'THROTTLE_ACTUATOR', 'RUN_TIME_MIL', 'TIME_SINCE_DTC_CLEARED', 'MAX_MAF', 'FUEL_TYPE', 'ETHANOL_PERCENT', 'EVAP_VAPOR_PRESSURE_ABS', 'EVAP_VAPOR_PRESSURE_ALT', 'SHORT_O2_TRIM_B1', 'LONG_O2_TRIM_B1', 'SHORT_O2_TRIM_B2', 'LONG_O2_TRIM_B2', 'FUEL_RAIL_PRESSURE_ABS', 'RELATIVE_ACCEL_POS', 'HYBRID_BATTERY_REMAINING', 'OIL_TEMP', 'FUEL_INJECT_TIMING', 'FUEL_RATE']
        self.arr = []

    def scan_all_sensors_simulate(self):
        for param in self.list_of_parameters:
            """
            {
            Time: <time in epoch format>
            Parameter: <description of parameter – eg speed/rpm>
            Value: <magnitude and unit of parameter(where applicable) – eg 40 kph, 2000 rpm>
            Device_ID: <Id of device – (currently set as <hostname>_<partial mac address>)
            }
            """
            self.my_object = dict()
            self.my_object['Time'] = str(time.ctime())
            self.my_object['Parameter'] = str(param)
            self.my_object['Value'] = str(random.randint(1,100))
            self.my_object['Device_ID'] = 'RaspberryPi_fe47'
            self.arr.append(self.my_object)
        return self.arr

    def scan_and_write_to_json_file(self):
        arr_obj = self.scan_all_sensors_simulate()
        with open('result.json', 'w+') as fp:
            for item in arr_obj:
                json_obj = json.dumps(item)
                json.dump(json_obj, fp)

    def print_scanned_sensor_values_every_n_seconds(self, timer = 5):
        while(1):
            print(self.scan_all_sensors_simulate())
            print("Ctrl+C to break")
            print ("Next scan in 5 seconds")
            time.sleep(timer)
            
    

    
if __name__ == '__main__':
    simulate = obd_simulate()
    simulate.scan_and_write_to_json_file()
    simulate.scan_and_write_to_json_file()
    simulate.print_scanned_sensor_values_every_n_seconds()
