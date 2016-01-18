#!/usr/bin/python
# -*- coding: utf-8 -*-

from sys import argv

#Defining the input and output files

script, in_file, to_file = argv

#Opening the input file to be processed

msg_paxlst = open(in_file)
my_string = msg_paxlst.read()

#Defining the segment separator

ServiceCharacters_Pos_end = my_string.find('UNB', 0, len(my_string))
DataElement_Separator_Pos = my_string.find('UNA', 0, ServiceCharacters_Pos_end)

print("Service characters identification :")

if DataElement_Separator_Pos < 0:
    DataElement_Separator = '+'
    ComponentDataElement_Separator = ':'
    Segment_Terminator = "'"
    print("- Data Element separator is default : "+DataElement_Separator)
    print("- Compoenent Data Element separator is default : "+ComponentDataElement_Separator)
    print("- Segment terminator is defined : "+Segment_Terminator)
else:
    DataElement_Separator = my_string[DataElement_Separator_Pos+4:DataElement_Separator_Pos+5]
    ComponentDataElement_Separator = my_string[DataElement_Separator_Pos+3:DataElement_Separator_Pos+4]
    Segment_Terminator = my_string[DataElement_Separator_Pos+8:DataElement_Separator_Pos+9]
    print("- Data Element separator is defined : "+DataElement_Separator)
    print("- Compoenent Data Element separator is defined : "+ComponentDataElement_Separator)
    print("- Segment terminator is defined : "+Segment_Terminator)

#XXX_SGT Defines the segment sequence containing the information

APT_Dep_SGT = 'LOC' + DataElement_Separator +'125'
APT_Arr_SGT  = 'LOC' + DataElement_Separator +'87'
CieFlightNum_SGT  = 'TDT' + DataElement_Separator +'20'
DateTime_Dep_SGT = 'DTM' + DataElement_Separator + '189'
DateTime_Arr_SGT = 'DTM' + DataElement_Separator + '232'

#XXX_POS Defines the position of the searched information

APT_Dep_Pos = my_string.find(APT_Dep_SGT, 0, len(my_string))+8
APT_Arr_Pos = my_string.find(APT_Arr_SGT, 0, len(my_string))+7
Cie_Pos = my_string.find(CieFlightNum_SGT, 0, len(my_string))+7
FlightNum_Pos_beg = my_string.find(CieFlightNum_SGT, 0, len(my_string))+10
FlightNum_Pos_end = my_string.find(DataElement_Separator, FlightNum_Pos_beg, len(my_string))
DateTime_Dep_Pos = my_string.find(DateTime_Dep_SGT, 0, len(my_string))+8
DateTime_Arr_Pos = my_string.find(DateTime_Arr_SGT, 0, len(my_string))+8

#Defines the variables of the searched information

APT_Dep = my_string[APT_Dep_Pos:APT_Dep_Pos+3]
APT_Arr = my_string[APT_Arr_Pos:APT_Arr_Pos+3]
Cie = my_string[Cie_Pos:Cie_Pos+2]
FlightNum = my_string[FlightNum_Pos_beg:FlightNum_Pos_end]
Date_Dep = my_string[DateTime_Dep_Pos:DateTime_Dep_Pos+10]
Date_Arr = my_string[DateTime_Arr_Pos:DateTime_Arr_Pos+10]
DayMonth_Dep = Date_Dep[2:4]+'/'+Date_Dep[4:6]
Time_Dep = Date_Dep[6:8]+':'+Date_Dep[8:10]

#Define the type of the message API-P or API-C

TypeMSG_SGT = 'BGM' + DataElement_Separator
TypeMSG_Pos = my_string.find(TypeMSG_SGT, 0, len(my_string))+4
TypeMSG_Num = my_string[TypeMSG_Pos:TypeMSG_Pos+3]

if TypeMSG_Num == "250":
    TypeMSG = 'API-C'
    TypeMSG_CNT = "41"
    TypeMSG_FR = "membres d'equipage"
else:
    TypeMSG = 'API-P'
    TypeMSG_CNT = "42"
    TypeMSG_FR = "passagers"

#Print the results with this structure: EK76 CDG-DXB 27/12 21:25 API-C
print("\nFlight information :")
print(Cie + FlightNum+" "+APT_Dep+"-"+APT_Arr+" "+DayMonth_Dep+" "+Time_Dep+" "+TypeMSG)


#Bonus: Define the amout of passenger in the flight

PaxNum_SGT = 'CNT' + DataElement_Separator + TypeMSG_CNT
PaxNum_Pos_Beg = my_string.find(PaxNum_SGT, 0, len(my_string))+7
PaxNum_Pos_End = my_string.find(Segment_Terminator, PaxNum_Pos_Beg, len(my_string))
PaxNum = my_string[PaxNum_Pos_Beg:PaxNum_Pos_End]

print("Nombre de "+TypeMSG_FR+" prevus dans le message : "+PaxNum)

#Bonus: Define the amout of passenger in the sending (part)

PaxID_SGT = 'NAD' + DataElement_Separator
PaxID_NUM = str(my_string.count(PaxID_SGT)-1)
print("Nombre de "+TypeMSG_FR+" contenus dans l'envoi: "+PaxID_NUM+"\n")

#Bonus : Process many edifact files in one csv : formatting

DayMonthYear_Dep = Date_Dep[2:4]+'/'+Date_Dep[4:6]+'/20'+Date_Dep[:2]
Time_Dep = Date_Dep[6:8]+':'+Date_Dep[8:10]

DayMonthYear_Arr = Date_Arr[2:4]+'/'+Date_Arr[4:6]+'/20'+Date_Arr[:2]
Time_Arr = Date_Arr[6:8]+':'+Date_Arr[8:10]

#Displaying the format to be printed in the csv file

print("Cie" + "\t" + "FlightNum" + "\t" + "APT_Dep" + "\t" + "Date_Dep" + "\t" + "Time_Dep" + "\t" + "APT_Arr" + "\t" + "Date_Arr" + "\t" + "Time_Arr" + "\t" + "TypeMSG")
print("\n")
print(Cie + "\t" + FlightNum + "\t" + APT_Dep + "\t" +DayMonthYear_Dep + "\t" + Time_Dep + "\t" + APT_Arr + "\t" + DayMonthYear_Arr + "\t" + Time_Arr + "\t" + TypeMSG)

#Defining the variables to be printed in the csv file

target_header = "Cie" + "\t" + "FlightNum" + "\t" + "APT_Dep" + "\t" + "Date_Dep" + "\t" + "Time_Dep" + "\t" + "APT_Arr" + "\t" + "Date_Arr" + "\t" + "Time_Arr" + "\t" + "TypeMSG" + "\n"
target_content = Cie + "\t" + FlightNum + "\t" + APT_Dep + "\t" +DayMonthYear_Dep + "\t" + Time_Dep + "\t" + APT_Arr + "\t" + DayMonthYear_Arr + "\t" + Time_Arr + "\t" + TypeMSG

#Opening the target file and printing the variables

target = open(to_file, 'w')
target.write(target_header)
target.write(target_content)

#Closing the opened files

target.close()
msg_paxlst.close()