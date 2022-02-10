import pymysql
import time
from dronekit import connect
#import charts
from datetime import datetime
import json
#from custom_drone import MyVehicle

vehicle = connect('COM12', wait_ready=True,baud=115200)



def armed(vehicle):
    if vehicle.armed:
        return 'armed'
    else:
        return 'disarmed'

def mode(vehicle):
    if vehicle.mode.name == 'STABILIZE':
        return '0'
    elif vehicle.mode.name == 'AUTO':
        return '3'
    elif vehicle.mode.name == 'GUIDED':
        return '4'
    elif vehicle.mode.name == 'LOITER':
        return '5'
    elif vehicle.mode.name == 'RTL':
        return '6'
    elif vehicle.mode.name == 'LAND':
        return '9'
    else:
        return vehicle.mode.name
    
def drone_message_dumper(vehicle):
    
    test_msg = {
        'Latitude': vehicle.location.global_relative_frame.lat,
        'Longitude': vehicle.location.global_relative_frame.lon,
        'Altitude': vehicle.location.global_relative_frame.alt,
        'V': vehicle.battery.voltage,
        'A': vehicle.battery.current,
        'Airspeed': vehicle.airspeed,
        'Groundspeed': vehicle.groundspeed,
        'GPSTime': '20',
        'GPSstatus': vehicle.gps_0.satellites_visible,
        'BatteryStatus': vehicle.battery.level,
        'CurrentFlightMode': mode(vehicle),
        'Motor': armed(vehicle),
          }
    return test_msg
    data2 = json.dumps(test_msg)
    print(data2)
print(drone_message_dumper(vehicle))

# 資料庫設定
db_settings = {
    "host": "127.0.0.1",
    "port": 3306,
    "user": "root",
    "password": "Kenny94095!",
    "db": "senserdata",
    "charset": "utf8"
}

try:
    # 建立Connection物件
    conn = pymysql.connect(**db_settings)
except Exception as ex:
    print(ex)

with conn.cursor() as cursor:
    for _ in range(5):
    #新增資料
        command = "INSERT INTO drone (Latitude,Longitude,Altitude,V,A,Airspeed,Groundspeed,GPSTime,GPSstatus,BatteryStatus,CurrentFlightMode,Motor) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        charts = drone_message_dumper(vehicle)
        cursor.execute(command,(charts['Latitude'],charts['Longitude'],charts['Altitude'],charts['V'],charts['A'],charts['Airspeed'],charts['Groundspeed'],charts['GPSTime'],charts['GPSstatus'],charts['BatteryStatus'],charts['CurrentFlightMode'],charts['Motor']))
        conn.commit()
        time.sleep(0.1)
for _ in range(1):
    #print(dronetime(vehicle))
    #"Latitude, Longtitude, Altitude"
    print(vehicle.location.global_relative_frame)
    #D4, D5, D6
    print(vehicle.attitude)
    #D1, D2, D3
    print(vehicle.velocity)
    #V, A, BatteryStatus
    print(vehicle.battery)
    #AirSpeed
    print(vehicle.airspeed)
    #GroundSpeed
    print(vehicle.groundspeed)
    #CurrentFlightMode
    print(vehicle.mode.name)
    #GPSStatus
    print(vehicle.gps_0)
    #Motor (report armed/disarmed)
    print(vehicle.armed)
    #waypointnumber
    print("waypoint %s " % vehicle.commands.next)
    print(vehicle.capabilities.flight_termination)
    #print(dronetime(vehicle))
    print("="*100)
    time.sleep(0.01)
 

vehicle.close()