import sys
sys.path.append('../')

# --------------------------------------------------------------------------- # 
# import the various server implementations
# --------------------------------------------------------------------------- #
from pymodbus.version import version
from pymodbus.server.asynchronous import StartTcpServer
import threading
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.datastore import ModbusSequentialDataBlock
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
from pymodbus.transaction import (ModbusRtuFramer,
                                  ModbusAsciiFramer,
                                  ModbusBinaryFramer)
from custom_message import CustomModbusRequest
# --------------------------------------------------------------------------- # 
# configure the service logging
# --------------------------------------------------------------------------- # 
import logging
FORMAT = ('%(asctime)-15s %(threadName)-15s'
          ' %(levelname)-8s %(module)-15s:%(lineno)-8s %(message)s')
logging.basicConfig(format=FORMAT)
log = logging.getLogger()

log.setLevel(logging.CRITICAL)


def writeRegister(a , address , values):  ###### Tüm blok yazım işlemleri için kullanılacak
    global Context
    context  = a[0]
    register = 3 # mode 3
    slave_id = 0x00
    context[slave_id].setValues(register, address, values) 


def readRegister(a , address):   ############## Tüm blok okuma işlemleri için
    global Context
    context  = a[0]
    register = 3 # mode 3
    slave_id = 0x00
    return context[slave_id].getValues(register, address, 1) 

def writeLiveStream(a , x_y_z_arr):  ##### kullanıcı anlık datayı buradan okuyacak
    
    writeRegister(a, 0 , x_y_z_arr) #  0 - 2 arası canlı veri okunacağı yer

def writeStreamSecond(a , x_y_z_All):    ##### kullanıcı saniyelik datayı buradan okuyacak 
    
    writeRegister(a, 3 , x_y_z_All) 

def readSettings1(a):
    return readRegister(a , 69) # server da ki 16. word adresinden itibaren values dizisini yükle.

def readSettings2(a):
    return readRegister(a , 70) # server da ki 16. word adresinden itibaren values dizisini yükle.

def writeSettings1(a , values):
    writeRegister(a , 69 , values)

def writeSettings2(a , values):
    writeRegister(a , 70 , values)
    
    
def readReferences(a):
    retArr = []
    for i in range(16):
        retArr.append(readRegister(a , 69)[0])
    return readReferences

def writeReferencesOverlap(a,value):
    writeRegister(a , 96,value)


def readReferencesOverlap(a,value):
    return readRegister(a , 96)[0]

def writeAmplitute(a,value):
    writeRegister(a , 97,value)
    

def writeFreq(a , Value):
    writeRegister(a , 98,value)

def writeRotationalFault(a , Value):
    writeRegister(a , 99,value)

def readRotationalFault(a):
    return readRegister(a , 99)[0]

def run_async_server():
    # Modbus kullanılabilir adress dizisini maple
    store = ModbusSlaveContext(
        di=ModbusSequentialDataBlock(0, [0]*100),
        co=ModbusSequentialDataBlock(0, [0]*100),
        hr=ModbusSequentialDataBlock(0, [0]*100),
        ir=ModbusSequentialDataBlock(0, [0]*100))
    store.register(CustomModbusRequest.function_code, 'cm',
                   ModbusSequentialDataBlock(0, [0] * 100))
    global Context
    Context = ModbusServerContext(slaves=store, single=True)
    
    identity = ModbusDeviceIdentification()
    identity.VendorName = 'Pymodbus'
    identity.ProductCode = 'PM'
    identity.VendorUrl = 'http://github.com/riptideio/pymodbus/'
    identity.ProductName = 'Pymodbus Server'
    identity.ModelName = 'Pymodbus Server'
    identity.MajorMinorRevision = version.short()
    import netifaces as ni
    ni.ifaddresses('eth0')
    ip = ni.ifaddresses('eth0')[ni.AF_INET][0]['addr']
    print(ip)
    StartTcpServer(Context, identity=identity, address=(ip, 5020),
                   custom_functions=[CustomModbusRequest])
 
if __name__ == "__main__":
    run_async_server()


