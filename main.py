import sys , time 
sys.path.append('../')
from manageSCD import testPeriodic , loop , setStartValuesModbus , periodicTime , setModeSelection , connect , disconnect , startToggle , stopToggle , setSensorsEnables , getSTEResultNotifyNoTime ,setOutputDataRates
import automatePairing as a
import threading
from modbusServer import run_async_server 
from modbusManagement import mainLoopAPI
import asyncio 

# sudo iptables -t nat -A PREROUTING -p tcp --dport 502 -j REDIRECT --to-ports 5020 



""" Automate Pairing Thread - Start"""
def automate_pairing():
    agent = a.Agent(a.bus, a.AGENT_PATH)
    agnt_mngr = a.dbus.Interface(a.bus.get_object(a.BUS_NAME, a.AGNT_MNGR_PATH),
                               a.AGNT_MNGR_IFACE)
    agnt_mngr.RegisterAgent(a.AGENT_PATH, a.CAPABILITY)
    agnt_mngr.RequestDefaultAgent(a.AGENT_PATH)

    adapter = a.Adapter()
    global mainloop  
    mainloop = a.GLib.MainLoop()
    try:
        mainloop.run()
    except KeyboardInterrupt:
        agnt_mngr.UnregisterAgent(a.AGENT_PATH)
        mainloop.quit()   

t1 = threading.Thread(target= automate_pairing)
t1.start()
"""
t2 = threading.Thread(target= run_async_server)
t2.start()
"""

time.sleep(3)
"""
loop.run_until_complete(connect())
loop.run_until_complete(setModeSelection(True))
loop.run_until_complete(disconnect())

"""


def t3():
    loop.run_until_complete(connect())
    loop.run_until_complete(stopToggle())
    loop.run_until_complete(setSensorsEnables(b'\xf0'))
    loop.run_until_complete(setSensorsEnables(b'\x01'))
    loop.run_until_complete(setOutputDataRates(b'\x00'))


    loop.run_until_complete(startToggle())
    c2 = 0
    while(1):
        print(c2)
        loop.run_until_complete(getSTEResultNotifyNoTime())
        c2 +=1
        loop.run_until_complete(asyncio.sleep(1.0))
    loop.run_until_complete(disconnect())
    print("takıldı")
    
t2 = threading.Thread(target= t3)
t2.start()


mainloop.quit()  
"""
while(1):
    print("Deneme")
#testPeriodic
mainloop.quit()  

"""




