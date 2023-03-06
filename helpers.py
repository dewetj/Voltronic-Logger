import crcmod
import datetime
import config

xmodem_crc_func = crcmod.mkCrcFun(0x11021, rev=False, initCrc=0x0000, xorOut=0x0000)

#dummy data list reponses for testing
qpigs_structure = ['grid_voltage', 'grid_frequency', 'inverter_voltage', 'inverter_frequency', 'inverter_apparent_output', 'inverter_active_power', 'inverter_load', 'bus_voltage', 'battery_voltage','charge_current',
                    'battery_capacity','inverter_temperature','pv_input_current','pv_input_voltage','battery_voltage_scc','discharge_current','inverter_status','battery_voltage_offset_fan','eeprom_version','pv_in_power','device_status']
dummy_qpigs = ['240.0', '50.0', '240.0', '50.0', '0368', '0278', '007', '346', '49.70', '050', '096', '0042', '00.0', '000.0', '00.00', '00000', '00010000', '00', '00', '00000', '010zx9fxzr']

qid_structure = ['serial_number']
dummy_qid = ['12345678901234zx9fxzr']

qmod_structure = ['mode']
dummy_qmod = ['Lzx9fxzr']

def calc_crc(comando):
    global crc
    crc = hex(xmodem_crc_func(comando))
    return crc

def execute_command(command):
    if command == 'QPIGS':
        nbytes = 110
        return_list = dummy_qpigs
    elif command == 'QID':
        nbytes = 18
        return_list = dummy_qid
    elif command == 'QMOD':
        nbytes = 5
        return_list = dummy_qmod
    else:
        return ['']

    #TESTING!!!!!
    if config.testing == True:
        return return_list

    calc_crc(command.encode('utf-8'))

    crc1=crc[0:4]
    crc2=crc[0:2]+crc[4:6]

    crc1=int(crc1, base=16)
    crc2=int(crc2, base=16)

    string_command = command+chr(crc1)+chr(crc2)+'\r'
    bytes_command = string_command.encode('ISO-8859-1')

    fd = open('/dev/hidraw0', 'rb+') #Open file to read and write in bytes (rb+)
    fd.flush()
    fd.write(bytes_command)
    data_in_bytes = fd.read(nbytes)
    fd.close()
        
    data_in_string = data_in_bytes.decode('ISO-8859-1')
    data_as_list = data_in_string.split("//")

    return_list = data_as_list[0][1:].split(" ")

    return return_list

def map_mode(qmod):
    modes = {"P":"Power On","S":"Standby","L":"Line","B":"Battery","F":"Fault","H":"Power saving"}
    return modes[qmod[0]]
        
def map_datatypes(data_list):
    out_data = list()
    out_data.append(float(data_list[0]))
    out_data.append(float(data_list[1]))
    out_data.append(float(data_list[2]))
    out_data.append(float(data_list[3]))
    out_data.append(float(data_list[4]))
    out_data.append(float(data_list[5]))
    out_data.append(float(data_list[6]))
    out_data.append(float(data_list[7]))
    out_data.append(float(data_list[8]))
    out_data.append(float(data_list[9]))
    out_data.append(float(data_list[10]))
    out_data.append(float(data_list[11]))
    out_data.append(float(data_list[12]))
    out_data.append(float(data_list[13]))
    out_data.append(float(data_list[14]))
    out_data.append(float(data_list[15]))
    out_data.append(data_list[16])
    out_data.append(float(data_list[17]))
    out_data.append(data_list[18])
    out_data.append(float(data_list[19]))
    out_data.append(data_list[20])
    #Clean mode as it can have shitty data in for some weird reason.
    if data_list[21] not in ['P','S','L','B','F','H']:
        out_data.append(' ')
    else:
        out_data.append(data_list[21])
    
    return out_data

def create_dict(data_list):
    data_keys = ["grid_voltage", "grid_frequency", "inverter_voltage", "inverter_frequency", "inverter_apparent_output", "inverter_active_power", "inverter_load", "bus_voltage", "battery_voltage","charge_current",
                    "battery_capacity","inverter_temperature","pv_input_current","pv_input_voltage","battery_voltage_scc","discharge_current","inverter_status","battery_voltage_offset_fan","eeprom_version",
                    "pv_in_power","device_status","mode"]
    data_dict = dict(zip(data_keys, data_list))
    return data_dict