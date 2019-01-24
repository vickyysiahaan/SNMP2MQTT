import json, struct, math
import numpy as np
from Constants import *
from easysnmp import Session

dataPerAccess = 22

class Device():
    def __init__(self, IPaddress, Port, Community, Version, Timeout):        
        self.dev = Session(hostname=IPaddress, remote_port=Port, community=Community, version=Version, timeout=Timeout)
        
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ READ METHODS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    #Method to numeric variable from regular OID
    def read_num(self, VarNameList, OIDList, MultiplierList):
        # Arguments:
        # VarNameList       :   list of variable name
        # OIDList           :   list of variable OID address
        # MultiplierList    :   list of multiplier
        # Return            :   dictionary of variable name and its value
        
        self.values = []

        self.operation = math.ceil(len(OIDList)/dataPerAccess)
        i = 0
        for opr in range(self.operation):
            try: 
                data = self.dev.get(oids[i:i+dataPerAccess])
            except:
                data = self.dev.get(oids[i:])

            for item in data:
                self.values.append(int(item.value))

            i += dataPerAccess

        for i in range(0, len(self.values)):
            self.values[i] = round(self.values[i]*MultiplierList[i],3) 
        
        self.Result = dict(zip(VarNameList, self.values))
        return self.Result

    #Method to string variable from regular OID
    def read_string(self, VarNameList, OIDList):
        # Arguments:
        # VarNameList       :   list of variable name
        # OIDList           :   list of variable OID address
        # Return            :   dictionary of variable name and its value
        
        self.values = []

        self.operation = math.ceil(len(OIDList)/dataPerAccess)
        i = 0
        for opr in range(self.operation):
            try: 
                data = self.dev.get(oids[i:i+dataPerAccess])
            except:
                data = self.dev.get(oids[i:])

            for item in data:
                self.values.append(str(item.value))

            i += dataPerAccess
        
        self.Result = dict(zip(VarNameList, self.values))
        return self.Result

    #Method to string variable from Table OID
    def read_num_tab(self, VarNameList, OIDList, rowList, MultiplierList):
        # Arguments:
        # VarNameList       :   list of variable name
        # OIDList           :   list of variable OID address
        # rowList           :   list of total row that we want to get from table column (max repetition in getBulk operation)
        # MultiplierList    :   list of multiplier
        # Return            :   dictionary of variable name and its value
        
        self.values = []
        self.Result = {}
        i = 0
        for oid in OIDList:
            data = self.dev.get_bulk(oid, max_repetitions=rowList[i])

            j=1
            for item in data:
                self.Result[VarNameList[i]+"_%d"%j]=round(int(item.value)*MultiplierList[i],3)
                j += 1
            i += 1

        return self.Result

    #Method to string variable from Table OID
    def read_string_tab(self, VarNameList, OIDList, rowList):
        # Arguments:
        # VarNameList       :   list of variable name
        # OIDList           :   list of variable OID address
        # rowList           :   list of total row that we want to get from table column (max repetition in getBulk operation)
        # Return            :   dictionary of variable name and its value
        
        self.values = []
        self.Result = {}
        i = 0
        for oid in OIDList:
            data = self.dev.get_bulk(oid, max_repetitions=rowList[i])

            j=1
            for item in data:
                self.Result[VarNameList[i]+"_%d"%j]=str(item.value)
                j += 1
            i += 1

        return self.Result
    
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ WRITE METHODS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    # Method to write a value in single OID
    def write(self, OID, value):
        # Arguments:
        # OID   :   object identifier of a variable
        # value :   value that you want to write in the OID

        self.dev.set(registerAddress, value)

    # Method to write values in multiple OIDs
    def write_multiple(self, OIDList, valueList):
        # Arguments:
        # OIDList   :   list of object identifier
        # valueList :   list of value

        oid_val = list(zip(OIDList,valueList))
        self.dev.set_multiple(oid_val)
    
