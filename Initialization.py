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
for i in range(1,DevNum+1):
    with open(FolderPath + '/JSON/Config/Device%dVariables.json' %i) as json_data:
        Var=json.load(json_data)
        VarID = list(Var.values())
        VarNum = len(VarID)

        _VarID = list()
        for j in range(0,VarNum):
            varid = list(VarID[j].values())
            _VarID.append(varid)
            varTopic = varid[6]
            varName = varid[0]
            for topic in varTopic:
                VarsPerTopic[topic-1][i-1].append(varName)
        AllVar.append(_VarID)
#print(AllVar)
#print(VarsPerTopic)
        
#### Classify variables based on their oid type and data type ####
## Initialization ##
# Numeric Variable in Table OID
Tab_Num_Var_List = list()
Tab_Num_OID_List = list()
Tab_Num_TotRow_List = list()
Tab_Num_Mul_List = list()

# String Variable in Table OID
Tab_Str_Var_List = list()
Tab_Str_OID_List = list()
Tab_Str_TotRow_List = list()

# Numeric Variable in regular OID
Num_Var_List = list()
Num_OID_List = list()
Num_Mul_List = list()

# String Variable in regular OID
Str_Var_List = list()
Str_OID_List = list()

## Start to fill blank lists above ##
for i in range(0,DevNum):
    # Numeric Variable in Table OID
    Tab_Num_Var_List.append(list())
    Tab_Num_OID_List.append(list())
    Tab_Num_TotRow_List.append(list())
    Tab_Num_Mul_List.append(list())

    # String Variable in Table OID
    Tab_Str_Var_List.append(list())
    Tab_Str_OID_List.append(list())
    Tab_Str_TotRow_List.append(list())

    # Numeric Variable in regular OID
    Num_Var_List.append(list())
    Num_OID_List.append(list())
    Num_Mul_List.append(list())

    # String Variable in regular OID
    Str_Var_List.append(list())
    Str_OID_List.append(list())
    
    for j in range(0,len(AllVar[i])):
        VarName = AllVar[i][j][0]
        OID = AllVar[i][j][1]
        DataType = AllVar[i][j][2]
        isTable = AllVar[i][j][3]
        TotalRow = AllVar[i][j][4]
        Multiplier = AllVar[i][j][5]

        
        if isTable:
            if DataType == NUMERIC:
                Tab_Num_Var_List[i].append(VarName)
                Tab_Num_OID_List[i].append(OID)
                Tab_Num_TotRow_List[i].append(TotalRow)
                Tab_Num_Mul_List[i].append(Multiplier)
            elif DataType == STRING:
                Tab_Str_Var_List[i].append(VarName)
                Tab_Str_OID_List[i].append(OID)
                Tab_Str_TotRow_List[i].append(TotalRow)
        else:
            if DataType == NUMERIC:
                Num_Var_List[i].append(VarName)
                Num_OID_List[i].append(OID)
                Num_Mul_List[i].append(Multiplier)
            elif DataType == STRING:
                Str_Var_List[i].append(VarName)
                Str_OID_List[i].append(OID)

#For Debugging
# Numeric Variable in Table OID
'''
print("\nNumeric Variable in Table OID")
print(Tab_Num_Var_List)
print(Tab_Num_OID_List)
print(Tab_Num_TotRow_List)
print(Tab_Num_Mul_List)

# String Variable in Table OID
print("\nString Variable in Table OID")
print(Tab_Str_Var_List)
print(Tab_Str_OID_List)
print(Tab_Str_TotRow_List)

# Numeric Variable in regular OID
print("\nNumeric Variable in regular OID")
print(Num_Var_List)
print(Num_OID_List)
print(Num_Mul_List)

# String Variable in regular OID
print("\nString Variable in regular OID")
print(Str_Var_List) 
print(Str_OID_List)
'''
