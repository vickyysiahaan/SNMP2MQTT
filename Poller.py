import paho.mqtt.client as mqtt
from Constants import *
from Initialization import *
from time import strftime, localtime
import json, time, os, inspect, MySNMP, traceback, gc, threading, pprint, signal, psutil
import MyDB

FolderPath = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

_FINISH = False

def get_process_memory():
    process = psutil.Process(os.getpid())
    return [process.memory_info().rss,process.memory_full_info().rss]

#print(LoggingPeriod)
db = MyDB.DataBase()

def PollerPerDevice(did,Device_Identity):
    DevName = Device_Identity['Name']
    IPAddress = Device_Identity['IPAddress']
    Port = Device_Identity['SNMPPort']
    Version = Device_Identity['SNMPVersion']
    ReadComm = Device_Identity['SNMPReadCommunity']
    WriteComm = Device_Identity['SNMPWriteCommunity']
    Timeout = Device_Identity['Timeout']
    Token = Device_Identity['AccessToken']
    mqtt_client = mqtt.Client()

    isConnected = False
    InitialState = True

    tLog0 = 0
    
    mqtt_client.username_pw_set(Token)
    Trial = 1
    while(Trial <=3):
        try:
            mqtt_client.connect(BrokerHOST, MQTTPort, 60)
            mqtt_client.loop_start()
            isConnected = True
            print("Client-%s connected to MQTT Broker" %DevName)
            break
        except:
            Trial += 1
            print("Client-%s FAILED connected to MQTT Broker" %DevName)
            time.sleep(3)
            
    while(not _FINISH):
        try:
            tPoll0 = time.time()    #begin polling time
            if InitialState:
                tLog0 = tPoll0   
            if not isConnected:
                try:
                    mqtt_client.connect(BrokerHOST, MQTTPort, 60)
                    mqtt_client.loop_start()
                    isConnected = True
                    print("Client-%s connected to MQTT Broker" %DevName)
                    break
                except:
                    Trial += 1
                    print("Client-%s FAILED connected to MQTT Broker" %DevName)
                
            try:
                device = MySNMP.Device(IPAddress, Port, ReadComm, Version, Timeout)
                print("Connected to ", DevName)
            except:
                tb = traceback.format_exc()
                #print(tb)
                print("FAILED Connection to", DevName)
                
            Data = {}
            
            ### Read Numeric Variable in Table OID
            #print("NumVarTabData")
            for dtype in NUMERIC:
                command="""
#print(Tab_%s_Var_List[did-1])
if len(Tab_%s_Var_List[did-1]) != 0:
    NumVarTabData = device.read_num_tab(Tab_%s_Var_List[did-1], Tab_%s_OID_List[did-1], Tab_%s_TotRow_List[did-1], Tab_%s_Mul_List[did-1])
    Data.update(NumVarTabData)
    #print(NumVarTabData)
                """%(dtype,dtype,dtype,dtype,dtype,dtype)
                exec(command)
            ### Read String Variable in Table OID
            #print("StrVarTabData")
            for dtype in STRING:
                command="""
#print(Tab_%s_Var_List[did-1])
if len(Tab_%s_Var_List[did-1]) != 0:
    StrVarTabData = device.read_string_tab(Tab_%s_Var_List[did-1], Tab_%s_OID_List[did-1], Tab_%s_TotRow_List[did-1])
    Data.update(StrVarTabData)
    #print(StrVarTabData)
                """%(dtype,dtype,dtype,dtype,dtype)
                exec(command)
            ### Read Numeric Variable in regular OID
            #print("NumVarData")
            for dtype in NUMERIC:
                command = """
#print(%s_Var_List[did-1])
if len(%s_Var_List[did-1]) != 0:
    NumVarData = device.read_num(%s_Var_List[did-1], %s_OID_List[did-1], %s_Mul_List[did-1])
    Data.update(NumVarData)
    #print(NumVarData)
                """%(dtype,dtype,dtype,dtype,dtype)
                exec(command)
            ### Read String Variable in regular OID
            #print("StrVarData")
            for dtype in STRING:
                command = """
#print(%s_Var_List[did-1])
if len(%s_Var_List[did-1]) != 0:
    StrVarData = device.read_string(%s_Var_List[did-1], %s_OID_List[did-1])
    Data.update(StrVarData)
    #print(StrVarData)
                """%(dtype,dtype,dtype,dtype)
                exec(command)
            tPoll1 = time.time()    #end polling time
                
            #PollingDuration = round(tPoll1-tPoll0, 2)
            PollingDuration = tPoll1-tPoll0
            Data['PollingDuration'] = PollingDuration
            Timestamp = strftime("%Y-%m-%d %H:%M:%S", localtime())
            Data['Timestamp'] = Timestamp

            #pprint.pprint(Data, width=1)
                
            with open(FolderPath + '/JSON/Data/Device%dData.json'%did, 'w') as file:
                file.write(json.dumps(Data, indent=4))

            tLog1 = tPoll1
            if InitialState or tLog1 - tLog0 >= LoggingPeriod:
                db.InsertData(did, DevName, Data)
                db.commit()
                InitialState = False
                #isAlreadyLogged = True
                print(Timestamp, ">>>", DevName, "Data are Logged")
                tLog0 = tPoll1
                    
            DataPerTopic = []
            for i in range(0,len(VarsPerTopic)):
                vals = []
                for name in VarsPerTopic[i][did-1]:
                    vals.append(Data[name])
                DataPerTopic.append(dict(zip(VarsPerTopic[i][did-1],vals)))
            #pprint.pprint(DataPerTopic, width=1)

            i = 0
            for topic in TopicList:
                if DataPerTopic[i] != {}:
                    mqtt_client.publish(topic, json.dumps(DataPerTopic[i]),0)
                    print(Timestamp, ">>>", DevName, "Data are Published in topic:", topic)
                i += 1
                
            time.sleep(PollingInterval)
            
        except KeyboardInterrupt:
            mqtt_client.loop_stop()
            print('Interrupted')
            break
        except:
            tb = traceback.format_exc()
            print(tb)
            time.sleep(PollingInterval)

class ServiceExit(Exception):
    pass

def service_shutdown(signum, frame):
    print('Caught signal %d' % signum)
    raise ServiceExit

if __name__ == '__main__':
    # Register the signal handlers
    signal.signal(signal.SIGTERM, service_shutdown)
    signal.signal(signal.SIGINT, service_shutdown)
    try:    
        threads = []
        
        for i,dev in enumerate(Dev_ID):
            threads.append(threading.Thread(target=PollerPerDevice, args=[i+1,dev]))
            threads[i].setDaemon(True)
            threads[i].start()

        while(True):
            time.sleep(0.5)
            
    except ServiceExit:
        print("finished")
        _FINISH = True
        for _thread in threads:
            _thread.join()
        print('All Thread Stopped')
        db.close()  
    except:
        tb = traceback.format_exc()
        #print(tb)
        db.close()
        
