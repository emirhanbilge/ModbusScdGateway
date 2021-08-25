import asyncio ,nest_asyncio ,sys , time
from scdCharacteristic import ServiceSCDSettings , ServiceShortTermExperiment , ServiceBulkDataTransfer
from bleak import BleakScanner , BleakClient
import modbusServer  as mdbs
sys.path.append('../')
nest_asyncio.apply()
from convertFunctions import s16floatfactor, s32floatfactor 

async def connect():
    await client.connect()
    print("Connected")

async def disconnect():
    await client.disconnect()
    print("Disconnected")


async def setModeSelection(mode):  #mode 0 : 0 değeri ; 1 ise 255 değerini yazar.
    try:
        await client.connect()
        print("First Mode Selection Started")
        #1 byte'tır ve 0 ile 255 değeri alır. Bunun dışındaki değerler reserved değerlerdir.  
        if mode:
            await client.write_gatt_char(ServiceSCDSettings["ModeSelection"] , b"\x00")
        else:
            await client.write_gatt_char(ServiceSCDSettings["ModeSelection"] , b"\xff")
        print("Mode Selection is Closed")
        await client.disconnect()
        return 1
    except : 
        return -1

async def selfTest():
    try:
        await client.connect()
        print("Self Test Starting ")
        res= await client.read_gatt_char(ServiceSCDSettings["SelfTestResult"])
        await client.disconnect()
        print("Self Test Closed")
        if res == b'\xc0':
            return 1
        else:
            return 2
    except:
        return -2

async def startToggle():
    try:
        await client.connect()
        vr = await client.read_gatt_char(ServiceShortTermExperiment["STEResults"])
        if (vr)[32] == 0:
            await client.write_gatt_char(ServiceSCDSettings["SCDGenericCommands"], b'\x20')
        await client.disconnect()
        return 1
    except:
        return -3

async def stopToggle():
    try:
        await client.connect()
        vr = await  client.read_gatt_char(ServiceShortTermExperiment["STEResults"])
        if (vr)[32] != 0:
            await client.write_gatt_char(ServiceSCDSettings["SCDGenericCommands"], b'\x20')
        await client.disconnect()
        return 1
    except:
        return -4

async def ToggleStatus():
    try:
        await client.connect()
        vr = await  client.read_gatt_char(ServiceShortTermExperiment["STEResults"])
        await client.disconnect()
        if (vr)[32] != 0:
            return 1
        return 0
    except:
        return -5

async def deleteFlashMemory():
    try:
        await client.connect()
        await client.write_gatt_char(ServiceSCDSettings["SCDGenericCommands"] ,b"\x30" )
        await client.disconnect()
        return 1
    except:
        return -6

async def resetSCD():
    try:
        await client.connect()
        await client.write_gatt_char(ServiceSCDSettings["SCDGenericCommands"] ,b"\x21" )
        await client.disconnect()
        return 1
    except:
        return -7

async def setSensorSpeed(speed):
    try:
        await client.connect()
        vr = await client.read_gatt_char(ServiceShortTermExperiment["STEConfigurationParameters"])
        if speed == 0:
            vr[5] = '\x00'
        elif speed == 1:
            vr[5] = '\x01'
        elif speed == 2:
            vr[5] = '\x02'
        elif speed == 3:
            vr[5] = '\x03'
        else:
            vr[5] = '\x00'
        await client.write_gatt_char(ServiceShortTermExperiment["STEConfigurationParameters"],vr) 
        await client.disconnect()
        return 1
    except :
        return -8

async def isThereDevice():
    devices = await BleakScanner.discover()
    for d in devices:
        if d.address == "18:04:ED:62:5B:B6":
            return 1
    return 0 





########################################## STREAM FONKSYONLARI ##############################################

sendModBus = []
accelroVariance=[]
comman = []
clientStatus = True

def notificationHandlerResult(sender, data):

    sendModBus.append(s16floatfactor(data[0:2] , 1))
    sendModBus.append(s16floatfactor(data[2:4] , 1))
    sendModBus.append(s16floatfactor(data[4:6] , 1))
    accelroVariance.append(   s32floatfactor(data[6:10]))
    accelroVariance.append(   s32floatfactor(data[10:14]))
    accelroVariance.append(   s32floatfactor(data[14:18]))
    mdbs.writeLiveStream(a=(mdbs.Context,) ,x_y_z_arr=sendModBus[-3:])
    #print(data)




async def StreamWithTime(timeS , speed):

    global sendModBus
    global accelroVariance
    global comman
    counterRasultTime = 0
    try:
        await client.connect()
        await stopToggle()
        vr = await client.read_gatt_char(ServiceShortTermExperiment["STEConfigurationParameters"])
        vr[4] = '\xf0'
        await client.write_gatt_char(ServiceShortTermExperiment["STEConfigurationParameters"])
        vr[4] = '\x01'
        await client.write_gatt_char(ServiceShortTermExperiment["STEConfigurationParameters"])
        await setSensorSpeed(speed) 
        await startToggle()
        await client.start_notify(ServiceShortTermExperiment["STEResults"], notificationHandlerResult)
        while(counterRasultTime<timeS):
            try:
                await asyncio.sleep(1.0)
                for i in sendModBus:
                    comman.append(i)
                for i in accelroVariance:
                    comman.append(i)
                mdbs.writeStreamSecond(a=(mdbs.Context,) , x_y_z_All=comman)
                accelroVariance = []
                sendModBus = []
            except:
                print("Somethings went wrong ")
            counterRasultTime +=1
        await client.stop_notify(ServiceShortTermExperiment["STEResults"])
        await client.disconnect()
        return 1
    except:
        return -9

async def StreamWithNoTime(speed):

    global sendModBus
    global accelroVariance
    counterRasultTime = 0
    try:
        await client.connect()
        await stopToggle()
        vr = await client.read_gatt_char(ServiceShortTermExperiment["STEConfigurationParameters"])
        vr[4] = '\xf0'
        await client.write_gatt_char(ServiceShortTermExperiment["STEConfigurationParameters"])
        vr[4] = '\x01'
        await client.write_gatt_char(ServiceShortTermExperiment["STEConfigurationParameters"])
        await setSensorSpeed(speed) 
        await startToggle()
        await client.start_notify(ServiceShortTermExperiment["STEResults"], notificationHandlerResult)
        while(clientStatus):
            try:
                await asyncio.sleep(1.0)
                accelroVariance = []
                sendModBus = []
            except:
                print("Somethings went wrong ")
            counterRasultTime +=1
        await client.stop_notify(ServiceShortTermExperiment["STEResults"])
        await client.disconnect()
        return 1
    except:
        return -10

############################################################################################################



################################################ Dowload Kısmı #############################################



allNotifiy = []
flagStartStop =[]
hundredPercent = 0
def notification_handler(sender, data):
   
    lists = []
    for i in data:
        lists.append(i)
    allNotifiy.append(lists)
    if len(allNotifiy) !=0:
        hundredPercent = int((len(allNotifiy) / int.from_bytes(bytearray(allNotifiy[0])[4:8] , "little"))*100) 
    if hundredPercent%10 == 0 :
        print("Yüzde %",hundredPercent," indirildi")
    #print(lists)
    if len(allNotifiy) ==  int.from_bytes(bytearray(allNotifiy[0])[4:8],"little"):
        print("************** " ,len(allNotifiy) ," Total Counter   Sağdaki paket sayısı" ,int.from_bytes(bytearray(allNotifiy[0])[4:8] , "little") )
        print("Download is successfully")




async def downloadRecord():


    try:
        await client.connect()
        await startToggle()
        await client.start_notify(ServiceBulkDataTransfer["BulkDataTransferDataFlow"] , notification_handler)
        await client.write_gatt_char(ServiceBulkDataTransfer["BulkDataTransferControl"],b'\x01')
        firsLenght = len(allNotifiy)
        counterL = 0
        second = 0
        while(1 ):
            try:    
                if counterL %10 == 0 :    
                    firsLenght = len(allNotifiy)
                    counterL = 0
                if second == firsLenght and firsLenght != 0:
                    break
                if len(allNotifiy)!=0 and len(allNotifiy) ==  int.from_bytes(bytearray(allNotifiy[0])[4:8] , "little"):
                    break
                await asyncio.sleep(1.0)
                counterL +=1
                second = len(allNotifiy)
            except:
                print("Download Error , some problem occure ")
        loop.run_until_complete(client.stop_notify(ServiceBulkDataTransfer["BulkDataTransferDataFlow"]))
        print("Notify lenght : " , len(allNotifiy))
        await disconnect()
        return 1 
    except:
        return -11



async def downloadStatus():
    try:
        await client.connect()
        vr=  await client.read_gatt_char(ServiceBulkDataTransfer["BulkDataTransferStatus"])
        await client.disconnect()
        if vr == b'\x00':
            return 0
        elif vr == b'\x01':
            return 1
        elif vr == b'\x02':
            return 2
        elif vr== b'\x03':
            return 3
        else : 
            return 3
    except:
        return -12
############################################################################################################


async def connectWithCheck():
    while(True ):
        if await isThereDevice():
           break
    await connect()


async def record(recordTime , recordSpeed):
    try:
        await deleteFlashMemory()
        await connectWithCheck()
        await stopToggle()
        vr = await client.read_gatt_char(ServiceShortTermExperiment["STEConfigurationParameters"])
        vr[4] = '\xf0'
        await client.write_gatt_char(ServiceShortTermExperiment["STEConfigurationParameters"])
        vr[4] = '\x01'
        vr[30] = '\xf1'
        await client.write_gatt_char(ServiceShortTermExperiment["STEConfigurationParameters"])
        await setSensorSpeed(recordSpeed)
        await startToggle()
        time.sleep(recordTime)
        await stopToggle()
        await disconnect()
        await downloadRecord()
        return 1
    except:
        return -13


#################################################### Periodic ##########################################
async def periodicLiveStream(liveTime , delayTime , speed):
    try:
        while(1):
            await StreamWithTime(liveTime,speed)
            time.sleep(delayTime)
        return 1
    except:
        return -14


async def periodicRecord(recordTime , speed , delayTime):
    try:
        while(1):
            await record(recordTime,speed)
            await downloadRecord()
            # burada modbusa indirme statusu yazılacak await downloadStatus()
            time.sleep(delayTime)
        return 1
    except:
        return -15

async def periodicStreamandRecord(recordTime,speedRecord,liveTime,speedStream):
    try:
        while(1):
            await record(recordTime,speedRecord)
            await downloadRecord()
            # burada modbusa indirme statusu yazılacak await downloadStatus()
            await StreamWithTime(liveTime,speedStream)
        return 1
    except:
        return -16
##############################################################################################



loop = asyncio.get_event_loop()
client = BleakClient("18:04:ED:62:5B:B6") # Adres girilmesi lazım
#client = BleakClient("18:04:ED:62:5B:AC") # Adres girilmesi lazım
