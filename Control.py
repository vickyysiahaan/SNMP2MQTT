import json, os, inspect, traceback, sys, argparse, ast
import MyDB, MySNMP
from Initialization import *
from time import strftime,localtime

db = MyDB.DataBase()

# Get Folder Path
FolderPath = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

# Main Function
def main(args):
    try:
        DevNum = args.DeviceNo
        VarNameList = args.VarName.split(',')
        ValueList = args.Value.split(',')
    except:
        pass
    #print(AllVar)
    Write(DevNum,VarNameList,ValueList)

def Write(DevNum,keyList,valList):
    #check device
    try:
        Device_Identity = Dev_ID[DevNum-1]
    except:
        print("Device Number is not detected in list of device")
    #get device profile
    DevName = Device_Identity['Name']
    IPAddress = Device_Identity['IPAddress']
    Port = Device_Identity['SNMPPort']
    Version = Device_Identity['SNMPVersion']
    WriteComm = Device_Identity['SNMPWriteCommunity']
    Timeout = Device_Identity['Timeout']

    #connect to device
    try:
        device = MySNMP.Device(IPAddress, Port, WriteComm, Version, Timeout)
        #print("Connected to ", DevName)
    except:
        tb = traceback.format_exc()
        #print(tb)
        print("FAILED Connection to", DevName)
        
    if (len(keyList)==len(valList)):
        OIDList = []
        TypeList = []
        MulList = []
        _keyList = []
        _valList = []
        for i,key in enumerate(keyList):
            val = valList[i]
            try:
                index = AllVarName[DevNum-1].index(key)
                access = AllVar[DevNum-1][index][7]
                if access == "RW":
                    _keyList.append(AllVar[DevNum-1][index][0])
                    OIDList.append(AllVar[DevNum-1][index][1])
                    TypeList.append(AllVar[DevNum-1][index][2])
                    MulList.append(AllVar[DevNum-1][index][5])
                    if AllVar[DevNum-1][index][2] in NUMERIC:
                        _valList.append(ast.literal_eval(val)/MulList[i])
                    else:
                        _valList.append(val)
                else:
                    print(key, "OID cannot be written")
            except Exception as e:
                print(e)
                
        #print(OIDList)
        #print(MulList)
        #print(_valList)
        #print(TypeList)
        
        device.write_multiple(OIDList, _valList, TypeList)
        print("Successful")
        Data = dict(zip(_keyList,_valList))
        Timestamp = strftime("%Y-%m-%d %H:%M:%S", localtime())
        Data['Timestamp'] = Timestamp
        db.InsertData(DevNum, DevName, Data)
        db.commit()
        db.close()
        
    else:
        raise ValueError("Length of Variable Name List and Value List are different") 
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--DeviceNo", type=int, help="Device Number", default=None)
    parser.add_argument("--VarName", type=str, help="List of variable name", default=None)
    parser.add_argument("--Value", type=str, help="List of variable value", default=None)
    
    args = parser.parse_args(sys.argv[1:]);
    
    main(args);
