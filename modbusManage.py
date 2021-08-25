import modbusServer as mdbs
import math
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadBuilder
import scdManage as scd

def convertInteger(binaryArray):
    lnght = len(binaryArray)
    if lnght==1:
        return int(binaryArray[0])
    elif lnght>1:
        num = 0
        for i in range(lnght):
            num += math.pow(2,i) * binaryArray[i] 
        return int(num)

def convertBinary(intNum):
    binaryArr = []
    while(intNum):
        binaryArr.append(intNum %2 )
        intNum = int(intNum / 2) 
    for i in range(16-len(binaryArr)):
        binaryArr.append(0)
    return binaryArr

def convertBinaryArraySize(intNum , Size):
    return convertBinary(intNum)[0:Size]



def selectStatus(StartModbusCommand, record,periodic , sensorTest, deleteSensor , streamOnOff , streamPeriodic):

    if StartModbusCommand:
        if record and periodic:
            return 1
        if record :
            return 2
        if periodic:
            return 3
        if sensorTest:
            return 4
        if deleteSensor:
            return 5
        if streamOnOff and streamPeriodic:
            return 6
        if streamOnOff:
            return 7
        return 8
    else:
        return 0


class Modbus_Scd_Gate():

    def __init__(self):
        self.sensorTest = 0
        self.streamSpeed = 0
        self.deleteSensor = 0
        self.errorCode = 0
        self.streamingTime = 0
        self.streamAlways = 0
        self.streamStatus = 0
        self.streamPeriodic = 0
        self.StartModbusCommand = 0
        self.recordStatus = 0
        self.periodic = 0
        self.recordTime = 0
        self.recordSpeed = 0
        self.downloadStatus = 0
        self.recordPeriodTime = 0
        self.modbusStatus = 0
        self.CloseModbus = 0

    def updateVariables(self):
        set1 = convertBinary(mdbs.readSettings1(a=(mdbs.Context,))[0])
        set2 = convertBinary(mdbs.readSettings2(a=(mdbs.Context,))[0])
        self.sensorTest = set1[15]
        self.streamSpeed = convertInteger(set1[13:15])
        self.deleteSensor =  set1[12]
        self.errorCode = convertInteger(set1[8:12])
        self.streamingTime = convertInteger(set1[4:8])
        self.streamAlways = set1[3]
        self.streamStatus = set1[2]
        self.streamPeriodic = set1[1]
        self.StartModbusCommand = set2[15]
        self.recordStatus = set2[14]
        self.periodic = set2[13]
        self.recordTime = convertInteger(set2[9:13])
        self.recordSpeed =  convertInteger(set2[7:9])
        self.downloadStatus = convertInteger(set2[5:7])
        self.recordPeriodTime =convertInteger(set2[3:5])
        self.modbusStatus = convertInteger(set2[0:3])
        set2[15] = 0
        self.CloseModbus(convertInteger(set2))
        self.modbusStatus = self.setModbusStatus()
    
    def setZeroSettingModbus(self):
        builder = BinaryPayloadBuilder(byteorder=Endian.Big,wordorder=Endian.Little)
        builder.add_16bit_int(0)
        payload = builder.to_registers()
        mdbs.writeSettings1(a=(mdbs.Context,),values =payload)
        mdbs.writeSettings2(a=(mdbs.Context,),values =payload)

    def closeModbusAfterCommand(self):
        builder = BinaryPayloadBuilder(byteorder=Endian.Big,wordorder=Endian.Little)
        builder.add_16bit_int(self.CloseModbus)
        payload = builder.to_registers()
        mdbs.writeSettings2(a=(mdbs.Context,),values =payload)


    def setModbusStatus(self):
        self.modbusStatus = selectStatus(self.StartModbusCommand , self.recordStatus , self.periodic,self.sensorTest
        ,self.deleteSensor,self.streamStatus , self.streamPeriodic)

     
    def resetAfterCommand(self):
        self.streamStatus = 0
        self.sensorTest = 0
        self.deleteSensor = 0
        self.recordStatus = 0
        self.modbusStatus = 0

    
    async def startFromStatus(self):
        er = 0
        if self.modbusStatus == 1 :
            er = await scd.periodicRecord(self.recordTime , self.recordSpeed , self.streamingTime) #download status değişicek
        elif self.modbusStatus == 2: 
            er = await scd.record(self.recordTime , self.recordSpeed) #download status değişicek
        elif self.modbusStatus == 3:
            er = await scd.periodicStreamandRecord(self.recordTime,self.recordSpeed,self.streamingTime,self.streamSpeed) #download status değişicek
        elif self.modbusStatus == 4:
            er = await scd.selfTest()  # 1 dönüyosa başarılı 2 dönüyosa hata var # -2 dönüyosa BLE error 
        elif self.modbusStatus == 5:
            er = await scd.deleteFlashMemory()
        elif self.modbusStatus == 6:
            er = await scd.periodicLiveStream(self.streamingTime , self.recordTime , self.streamSpeed)
        elif self.modbusStatus == 7:
            if self.streamAlways:
                er = await scd.StreamWithNoTime( self.streamSpeed)
            else:
                er = await scd.StreamWithTime(self.streamingTime , self.streamSpeed)
        else:
            self.modbusStatus = 0
        if er < 1:
            self.errorCode = abs(er)
        else:
            if abs(er)  > 10 and abs(er) != 14:
                self.downloadStatus = await scd.downloadStatus()
        self.resetAfterCommand()
        self.convertModbus()
        # burada modbusa yazılacak
        

    
    def convertModbus(self):
        arr = []
        arr.append(0)
        arr.append(self.streamPeriodic)
        arr.append(self.streamStatus)
        arr.append(self.streamAlways)
        temprory = convertBinaryArraySize(self.streamingTime , 4)
        arr.append(temprory[0])
        arr.append(temprory[1])
        arr.append(temprory[2])
        arr.append(temprory[3])
        temprory = convertBinaryArraySize(self.errorCode , 4)
        arr.append(temprory[0])
        arr.append(temprory[1])
        arr.append(temprory[2])
        arr.append(temprory[3])
        arr.append(self.deleteSensor)
        temprory = convertBinaryArraySize(self.streamSpeed , 2)
        arr.append(temprory[0])
        arr.append(temprory[1])
        arr.append(self.sensorTest)
        writeSet1Num = convertInteger(arr)
        builder = BinaryPayloadBuilder(byteorder=Endian.Big,wordorder=Endian.Little)
        builder.add_16bit_int(writeSet1Num)
        payload = builder.to_registers()
        mdbs.writeSettings1(a=(mdbs.Context,),values =payload)
        arr = []
        arr.append(0)
        arr.append(0)
        arr.append(0)
        temprory = convertBinaryArraySize(self.recordPeriodTime , 2)
        arr.append(temprory[0])
        arr.append(temprory[1])
        temprory = convertBinaryArraySize(self.downloadStatus , 2)
        arr.append(temprory[0])
        arr.append(temprory[1])
        temprory = convertBinaryArraySize(self.recordSpeed , 2)
        arr.append(temprory[0])
        arr.append(temprory[1])
        temprory = convertBinaryArraySize(self.recordTime , 4)
        arr.append(temprory[0])
        arr.append(temprory[1])
        arr.append(temprory[2])
        arr.append(temprory[3])
        arr.append(self.periodic)
        arr.append(self.recordStatus)
        arr.append(0)
        writeSet1Num = convertInteger(arr)
        builder = BinaryPayloadBuilder(byteorder=Endian.Big,wordorder=Endian.Little)
        builder.add_16bit_int(writeSet1Num)
        payload = builder.to_registers()
        mdbs.writeSettings2(a=(mdbs.Context,),values =payload)
       

gate = Modbus_Scd_Gate() 
gate.updateVariables()
gate.startFromStatus()
while(1):
    gate.updateVariables()
    gate.startFromStatus()
