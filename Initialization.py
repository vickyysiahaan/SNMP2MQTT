from time import localtime, strftime
import json, time, os, inspect
from Constants import *

FolderPath = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

#MQTT Conf
with open(FolderPath + '/JSON/Config/MQTTConfig.json') as json_data:
    MQTT = json.load(json_data)
    #Create variable with name and value based in key and value in MQTT dictionary
    locals().update(MQTT)
#print(MQTT)

#Etc Conf
with open(FolderPath + '/JSON/Config/etc.json') as json_data:
    etc = json.load(json_data)
    #Create variable with name and value based in key and value in etc dictionary
    locals().update(etc)
#print(etc)

#Devices Identity
with open(FolderPath + '/JSON/Config/DevicesIdentity.json') as json_data:
    DevID = json.load(json_data)
DevNum = len(list(DevID.keys()))
Dev_ID = list(DevID.values())
#print(Dev_ID)

#### Classify variables based on their mqtt publish topic ####
VarsPerTopic = []
for i in range(0,len(TopicList)):
    VarsPerTopic.append([])
    for j in range(0, DevNum):
        VarsPerTopic[i].append([])

#Variables Identity
AllVar = list()
AllVarName = list()
for i in range(1,DevNum+1):
    with open(FolderPath + '/JSON/Config/Device%dVariables.json' %i) as json_data:
        Var=json.load(json_data)
        VarID = list(Var.values())
        VarNum = len(VarID)

        _VarID = list()
        AllVarName.append([])
        for j in range(0,VarNum):
            varid = list(VarID[j].values())
            _VarID.append(varid)
            varTopic = varid[6]
            varName = varid[0]
            for topic in varTopic:
                VarsPerTopic[topic-1][i-1].append(varName)
            AllVarName[i-1].append(varName)
        AllVar.append(_VarID)
#print(AllVar)
#print(AllVarName)
#print(VarsPerTopic)
        
#### Classify variables based on their oid type and data type ####
## Initialization ##
# All Numeric Variables in Table OID
for dtype in NUMERIC:
    command = """
Tab_%s_Var_List = list()
Tab_%s_OID_List = list()
Tab_%s_TotRow_List = list()
Tab_%s_Mul_List = list()
"""%(dtype,dtype,dtype,dtype)
    exec(command)

# All String Variables in Table OID
for dtype in STRING:
    command = """
Tab_%s_Var_List = list()
Tab_%s_OID_List = list()
Tab_%s_TotRow_List = list()
"""%(dtype,dtype,dtype)
    exec(command)

# All Numeric Variables in regular OID
for dtype in NUMERIC:
    command = """
%s_Var_List = list()
%s_OID_List = list()
%s_Mul_List = list()
"""%(dtype,dtype,dtype)
    exec(command)

# All String Variables in regular OID
for dtype in STRING:
    command = """
%s_Var_List = list()
%s_OID_List = list()
"""%(dtype,dtype)
    exec(command)

## Start to fill blank lists above ##
for i in range(0,DevNum):
    # All Numeric Variables in Table OID
    for dtype in NUMERIC:
        command = """
Tab_%s_Var_List.append(list())
Tab_%s_OID_List.append(list())
Tab_%s_TotRow_List.append(list())
Tab_%s_Mul_List.append(list())
"""%(dtype,dtype,dtype,dtype)
        exec(command)

    # All String Variables in Table OID
    for dtype in STRING:
        command = """
Tab_%s_Var_List.append(list())
Tab_%s_OID_List.append(list())
Tab_%s_TotRow_List.append(list())
"""%(dtype,dtype,dtype)
        exec(command)

    # All Numeric Variables in regular OID
    for dtype in NUMERIC:
        command = """
%s_Var_List.append(list())
%s_OID_List.append(list())
%s_Mul_List.append(list())
"""%(dtype,dtype,dtype)
        exec(command)

    # All String Variables in regular OID
    for dtype in STRING:
        command = """
%s_Var_List.append(list())
%s_OID_List.append(list())
"""%(dtype,dtype)
        exec(command)

    for j in range(0,len(AllVar[i])):
        VarName = AllVar[i][j][0]
        OID = AllVar[i][j][1]
        DataType = AllVar[i][j][2]
        isTable = AllVar[i][j][3]
        TotalRow = AllVar[i][j][4]
        Multiplier = AllVar[i][j][5]
        Access = AllVar[i][j][7]

        if isTable:
            if DataType in NUMERIC:
                command = """
Tab_%s_Var_List[i].append(VarName)
Tab_%s_OID_List[i].append(OID)
Tab_%s_TotRow_List[i].append(TotalRow)
Tab_%s_Mul_List[i].append(Multiplier)
"""%(DataType,DataType,DataType,DataType)
                exec(command)
            elif DataType in STRING:
                command = """
Tab_%s_Var_List[i].append(VarName)
Tab_%s_OID_List[i].append(OID)
Tab_%s_TotRow_List[i].append(TotalRow)
"""%(DataType,DataType,DataType)
                exec(command)
        else:
            if DataType in NUMERIC:
                command = """
%s_Var_List[i].append(VarName)
%s_OID_List[i].append(OID)
%s_Mul_List[i].append(Multiplier)
"""%(DataType,DataType,DataType)
                exec(command)
            elif DataType in STRING:
                command = """
%s_Var_List[i].append(VarName)
%s_OID_List[i].append(OID)
"""%(DataType,DataType)
                exec(command)

'''
#For Debugging
# Numeric Variable in Table OID    
print("\nAll Numeric Variables in Table OID")
for dtype in NUMERIC:
    print("===",dtype,"===")
    command = """
print(Tab_%s_Var_List)
print(Tab_%s_OID_List)
print(Tab_%s_TotRow_List)
print(Tab_%s_Mul_List)
"""%(dtype,dtype,dtype,dtype)
    exec(command)

# String Variable in Table OID
print("\nAll String Variables in Table OID")
for dtype in STRING:
    print("===",dtype,"===")
    command = """
print(Tab_%s_Var_List)
print(Tab_%s_OID_List)
print(Tab_%s_TotRow_List)
"""%(dtype,dtype,dtype)
    exec(command)

# Numeric Variable in regular OID
print("\nAll Numeric Variables in regular OID")
for dtype in NUMERIC:
    print("===",dtype,"===")
    command = """
print(%s_Var_List)
print(%s_OID_List)
print(%s_Mul_List)
"""%(dtype,dtype,dtype)
    exec(command)

# String Variable in regular OID
print("\nAll String Variables in regular OID")
for dtype in STRING:
    print("===",dtype,"===")
    command = """
print(%s_Var_List)
print(%s_OID_List)
"""%(dtype,dtype)
    exec(command)
'''

#print("Initialization Finished")
