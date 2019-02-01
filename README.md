What you need to know:
1. I assume you: 
	- have a basic knowledge about SNMP (if you are a beginner, iReasoning MIB Browser might be an useful tool for you to learn this)
	- use python3.6 or later.

   Python modules needed:
	- easysnmp
	- numpy
	- MySQLdb
	- paho.mqtt
	- pprint
	- psutil
   
   based on my experience, easysnmp cannot be installed in windows, I recommend you to use Linux OS.

2. This program also requires MySQL database to be installed.
   Name, username, and the password of the database can be set in MyDB.py
   
3. SNMP devices and their OIDs that want to be read can be configured through JSON files in directory JSON/Config

   a. DevicesIdentity.json 
      contains information about devices identity.
      - Name			: Name of the device
      - IPAddress		: device ip address
      - SNMPPort		: snmp port of the device
      - SNMPVersion		: snmp version of the device
      - SNMPReadCommunity	: read community
      - SNMPWriteCommunity	: write community
      - AccessToken		: mqtt username (for authentication with mqtt broker),
      - Timeout			: timeout limit for the device
	  
	  
   b. MQTTConfig.json 
      contains settings for mqtt communication and polling interval.
      - PollingInterval	: interval of devices data polling 
      - BrokerHOST		: mqtt broker address
      - MQTTPort		: mqtt broker port
      - TopicList		: mqtt topic list. for example: ["v1/devices/me/telemetry", "v1/devices/me/attributes"]
	
	
   c. DeviceVariables.json
      contains list of variables in each device with its OID, Datatype, etc.
      - Name 		: 	name of the variable
      - OID  		: 	Object identifier of the variable
      - Datatype	: 	"INTEGER", "INTEGER32", "UINTEGER", "OCTETSTRING", "OID", "IPADDRESS"
      - isTable	: 	1 >> if the oid is in table oid, 0 >> if the oid is in regular oid (not in a table)
      - TotalRow	: 	number of row that want to be read in the OID (this is a maxrepetition in GetBulk operation)
      - Multiplier	: 	Value of this variable will be multiplied with this value (if you need numerical data processing)
      - PublishTopic	: 	mqtt topic index in TopicList. The variable value will be published on this topic.
      - Access	:	R  >> for read-only OID, RW >> for read-write OID
	
	
4. To begin data polling, just run the Poller.py. The program will automatically publish the data to mqtt topic periodically, based on the polling interval. The result can also be seen in JSON/Result


5. Device control (SNMP Set) via MQTT is still in development. But you can do SNMP set operation via  Control.py directly.

   Run this command:
   
   python3.6 Control.py --DeviceNo [Device_Number_Index] --VarName [List_of_variable] --Value [List_of_Value]
   
   Device_Number_Index 	==> device index (based on the order in DevicesIdentity)
   
   List_of_variable		==> list of variable that want to be set
   
   List_of_Value		==> list of desired value of each variable
   
   for example:
   
   python3.6 Control.py --DeviceNo 1 --VarName acInputOverVoltageValue,acInputUnderVoltageValue --Value 250.4,178.5
   
   this command will set acInputOverVoltageValue to 250.4 and acInputUnderVoltageValue to 178.5
   


# SNMP2MQTT
