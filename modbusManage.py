import time
import math
import nest_asyncio
import scdManage as scd
from pymodbus.payload import BinaryPayloadBuilder
from pymodbus.constants import Endian
import modbusServer as mdbs
from bleak import BleakClient
import asyncio
import nest_asyncio
import time
import rotAnalysis as rta
import threading
import asyncio
import nest_asyncio
nest_asyncio.apply()
nest_asyncio.apply()


def convertInteger(binaryArray):
    lnght = len(binaryArray)
    if lnght == 1:
        return int(binaryArray[0])
    elif lnght > 1:
        num = 0
        for i in range(lnght):
            num += math.pow(2, i) * binaryArray[i]
        return int(num)


def convertBinary(intNum):
    binaryArr = []
    while(intNum):
        binaryArr.append(intNum % 2)
        intNum = int(intNum / 2)
    for i in range(16-len(binaryArr)):
        binaryArr.append(0)
    return binaryArr


def convertBinaryArraySize(intNum, Size):
    return convertBinary(intNum)[0:Size]


class RotationalObj():

    def __init__(self, refer, refOverlap, amplitude, freq):
        self.refer = refer
        self.refOverlap = refOverlap
        self.amplitude = amplitude
        self.freq = freq
        

        self.specialThread = threading.Thread(target= self.updatePeriodic)
        
   

    def getAnalysis(self):
        val = rta.getAnlaysis(self.refer, self.refOverlap)
        sendModbus = convertBinary(val[0])
        sendModbus[15] = 0
        mdbs.writeRotationalFault(convertInteger(sendModbus))
        mdbs.writeFreq(val[1])
        mdbs.writeAmplitute(val[2])

    def updatePeriodic(self):
        while(1):
            if self.refer == None:
                self.refer = 0
                self.refOverlap = 0

            val = rta.getAnlaysis(self.refer, self.refOverlap)
            sendModbus = convertBinary(val[0])
            sendModbus[15] = 0
            mdbs.writeRotationalFault(convertInteger(sendModbus))
            mdbs.writeFreq(val[1])
            mdbs.writeAmplitute(val[2])
            time.sleep(240)
        
    def breakPeriod(self):
        self.specialThread.exit()

    def getThreadAlive(self):
        self.specialThread.isAlive()
        

updater = RotationalObj(0, 0, 0, 0)





def selectStatus(StartModbusCommand, record, periodic, sensorTest, deleteSensor, streamOnOff, streamPeriodic):

    if StartModbusCommand:
        if record and periodic:
            return 1
        if record:
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


threadResults = []


def periodicThread(recordTime, recordSpeed, streamingTime):
    er = loop2.run_until_complete(scd.periodicRecord(
        recordTime, recordSpeed, streamingTime))  # download status değişicek



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
        self.StartModbusCommand = 1
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

        rotational = convertBinary(mdbs.readRotationalFault(a=(mdbs.Context,)))
        if rotational[15]:
            # Burada analiz talep etmiştir ve biz analiz yapan fonksyonları çağıracağızdır.
            updater.breakPeriod()
            updater.getAnalysis()
        elif not updater.getThreadAlive():
            updater.getAnalysis()

        #print("Set 1 " , set1 , " Set2 " , set2)
        self.sensorTest = set1[15]
        self.streamSpeed = convertInteger(set1[13:15])
        self.deleteSensor = set1[12]
        self.errorCode = convertInteger(set1[8:12])
        self.streamingTime = convertInteger(set1[4:8])
        self.streamAlways = set1[3]
        self.streamStatus = set1[2]
        self.streamPeriodic = set1[1]
        self.StartModbusCommand = 1
        self.recordStatus = set2[14]
        self.periodic = set2[13]
        self.recordTime = convertInteger(set2[9:13])
        self.recordSpeed = convertInteger(set2[7:9])
        self.downloadStatus = convertInteger(set2[5:7])
        self.recordPeriodTime = convertInteger(set2[3:5])
        self.modbusStatus = convertInteger(set2[0:3])
        set2[15] = 0
        self.CloseModbus = (convertInteger(set2))
        self.setModbusStatus()

    def setZeroSettingModbus(self):
        builder = BinaryPayloadBuilder(
            byteorder=Endian.Big, wordorder=Endian.Little)
        builder.add_16bit_int(0)
        payload = builder.to_registers()
        mdbs.writeSettings1(a=(mdbs.Context,), values=payload)
        mdbs.writeSettings2(a=(mdbs.Context,), values=payload)

    def closeModbusAfterCommand(self):
        builder = BinaryPayloadBuilder(
            byteorder=Endian.Big, wordorder=Endian.Little)
        builder.add_16bit_int(self.CloseModbus)
        payload = builder.to_registers()
        mdbs.writeSettings2(a=(mdbs.Context,), values=payload)

    def setModbusStatus(self):
        self.modbusStatus = selectStatus(self.StartModbusCommand, self.recordStatus, self.periodic,
                                         self.sensorTest, self.deleteSensor, self.streamStatus, self.streamPeriodic)

    def resetAfterCommand(self):
        self.streamStatus = 0
        self.sensorTest = 0
        self.deleteSensor = 0
        self.recordStatus = 0
        self.modbusStatus = 0

    def startFromStatus(self):
        er = 0
        global threadResults
        if self.modbusStatus == 1:
            print("Kayıt alınacak ve periyodik olacak")
            try:
                if not t4.is_alive():
                    print("Thread Periodic Başlangıcı")
                    t4.start()
            except:
                print("ilk başlıyor ")
                t4 = threading.Thread(target=periodicThread, args=(
                    self.recordTime, self.recordSpeed, self.streamingTime))

                # er = await scd.periodicRecord(self.recordTime , self.recordSpeed , self.streamingTime) #download status değişicek
        elif self.modbusStatus == 2:
            print("Kayıt alınacak ")
            er = loop2.run_until_complete(scd.record(
                self.recordTime, self.recordSpeed))  # download status değişicek
        elif self.modbusStatus == 3:
            print("Hem stream hem de periyodik kayıt başladı")
            er = loop2.run_until_complete(scd.periodicStreamandRecord(
                self.recordTime, self.recordSpeed, self.streamingTime, self.streamSpeed))  # download status değişicek
        elif self.modbusStatus == 4:
            print("SCD test sensör başladı")
            # 1 dönüyosa başarılı 2 dönüyosa hata var # -2 dönüyosa BLE error
            er = loop2.run_until_complete(scd.selfTest())
        elif self.modbusStatus == 5:
            print("Delete Flash Başladı")
            er = loop2.run_until_complete(scd.deleteFlashMemory())
        elif self.modbusStatus == 6:
            print("Yayın açık ve periyodik")
            er = loop2.run_until_complete(scd.periodicLiveStream(
                self.streamingTime, self.recordTime, self.streamSpeed))
        elif self.modbusStatus == 7:
            print("Yayın açık ")
            if self.streamAlways:
                print("Yayın süresiz")
                er = loop2.run_until_complete(
                    scd.StreamWithNoTime(self.streamSpeed))
            else:
                print("Yayın süreli")
                er = loop2.run_until_complete(scd.StreamWithTime(
                    self.streamingTime, self.streamSpeed))
        else:
            if self.modbusStatus == 8:
                print("Yetki açık ama herhangi bir işlem yapmamış")
            else:
                print("Yetki kapalı ")
                self.modbusStatus = 0
        if er < 0:
            print("Hata meydana geldi hata kodu ", er)
            self.errorCode = abs(er)
        else:
            if self.modbusStatus > 0 and self.modbusStatus < 4:
                self.downloadStatus = loop2.run_until_complete(
                    scd.downloadStatus())
            if self.modbusStatus == 4:
                if er != 1:
                    print("Sensör testte hatalı sensör var")
                    self.errorCode = 12

        self.resetAfterCommand()
        self.convertModbus()
        # burada modbusa yazılacak

    def convertModbus(self):
        arr = []
        arr.append(0)
        arr.append(self.streamPeriodic)
        arr.append(self.streamStatus)
        arr.append(self.streamAlways)
        temprory = convertBinaryArraySize(self.streamingTime, 4)
        arr.append(temprory[0])
        arr.append(temprory[1])
        arr.append(temprory[2])
        arr.append(temprory[3])
        temprory = convertBinaryArraySize(self.errorCode, 4)
        arr.append(temprory[0])
        arr.append(temprory[1])
        arr.append(temprory[2])
        arr.append(temprory[3])
        arr.append(self.deleteSensor)
        temprory = convertBinaryArraySize(self.streamSpeed, 2)
        arr.append(temprory[0])
        arr.append(temprory[1])
        arr.append(self.sensorTest)
        writeSet1Num = convertInteger(arr)
        builder = BinaryPayloadBuilder(
            byteorder=Endian.Big, wordorder=Endian.Little)
        builder.add_16bit_int(writeSet1Num)
        payload = builder.to_registers()
        mdbs.writeSettings1(a=(mdbs.Context,), values=payload)
        arr = []
        arr.clear()
        arr.append(0)
        arr.append(0)
        arr.append(0)
        temprory = convertBinaryArraySize(self.recordPeriodTime, 2)
        arr.append(temprory[0])
        arr.append(temprory[1])
        temprory = convertBinaryArraySize(self.downloadStatus, 2)
        arr.append(temprory[0])
        arr.append(temprory[1])
        temprory = convertBinaryArraySize(self.recordSpeed, 2)
        arr.append(temprory[0])
        arr.append(temprory[1])
        temprory = convertBinaryArraySize(self.recordTime, 4)
        arr.append(temprory[0])
        arr.append(temprory[1])
        arr.append(temprory[2])
        arr.append(temprory[3])
        arr.append(self.periodic)
        arr.append(self.recordStatus)
        if self.modbusStatus == 8:

            arr.append(1)
        else:
            arr.append(0)
        writeSet1Num = convertInteger(arr)
        if not (-32768 <= writeSet1Num and writeSet1Num <= 32767):
            print(writeSet1Num, " ***", len(arr), " *****", arr)
            writeSet1Num = 32767
        builder = BinaryPayloadBuilder(
            byteorder=Endian.Big, wordorder=Endian.Little)
        builder.add_16bit_int(writeSet1Num)
        payload = builder.to_registers()
        mdbs.writeSettings2(a=(mdbs.Context,), values=payload)


def clientDisconnect():
    scd.clientStatus = False


def clientConnect():
    scd.clientStatus = True


def printRemoteClientIP(ipAdd):
    print("Remote connection ip : ", ipAdd)


loop2 = asyncio.get_event_loop()


def GatewayTh():

    scd.client = BleakClient("18:04:ED:62:5B:B6")
    gate = Modbus_Scd_Gate()
    gate.updateVariables()
    gate.startFromStatus()
    while(1):
        gate.updateVariables()
        gate.startFromStatus()
        time.sleep(1)
