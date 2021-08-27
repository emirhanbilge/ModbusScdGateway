import sys , time 
sys.path.append('../')
import automatePairing as a
import threading
from modbusServer import run_async_server 
from modbusManage import GatewayTh 

# sudo iptables -t nat -A PREROUTING -p tcp --dport 502 -j REDIRECT --to-ports 5020  port yönlendirme




# connect disconnect olması için clientin asynchronous dosyasında değiştirdim. Buraya modbus TCPServer üzerinden gidip çalıştığı threadin içerisindeki fonksyonu değiştirdim

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
""" Automate Pairing Thread - End"""


"""     Modbus Server Running            """
t2 = threading.Thread(target= run_async_server)
t2.start()
time.sleep(3)


"""     Modbus SCD GATE            """
t3 = threading.Thread(target= GatewayTh)
t3.start()


"""     Computer Control  """
while(1):
    time.sleep(3)
#testPeriodic

mainloop.quit()  






