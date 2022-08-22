"""
Author : Lukas Johnny
Date : 18/7/2022
Description : This script is used to establish the connection between RPI to Arduino using RX and TX
             Arduino : Tx --Connect -- Rpi : Rx
             Arduino : Rx --Connect -- Rpi : Tx

             Before running this code do ensure to:
             1. sudo raspi-config and enable SPI
             2. disable Serial login shell connection and enable Serial interface connection
             3. go to sudo vi /boot/config.txt -last line. Disable bluetooth using this command
             "dtoverlay=disable-bt"
             4. Reboot the Pi
             5. if ttyAMAO is not in dev, please enable_uart=1 in /boot/config too.
             6. ttyAMAO is serial protocol to connect PI and Arduino


"""
import serial
from time import sleep
import socket
from time import sleep
import numpy as np
from dronekit import *

class readdatafromArdtoRpi():

    def __init__(self):
        try:
            # Connect to Copter
            self.connection_string = '/dev/ttyAMA0,921600'
            self.vehicle = connect(self.connection_string, wait_ready=True)
            print("Virtual Copter is Ready")

        except socket.error:
            print("No server exist")

    # Connect to Arduino
    def initConnection(self,portNo, baudRate):
        try:
            ser = serial.Serial(portNo, baudRate)
            print("Device Connected")
            return ser
        except:
            print("Not connected")

    def getData(self,ser):
        try:
            data = ser.readline()
            data = data.decode("utf-8")
            data = data.split()
            data = data[0]
            return data
                 
        except:
            pass

    def getKeyboardInput(self,kp):  

        # Set into Guided Mode    
        if (kp =='g'):  
            print("Guided Mode")  
            @self.vehicle.on_attribute('mode')
            def mode_callback(self,attr_name, value):
                print(f">> Mode Updated: {value}")      
                          
            # ## We will not let the script to continue unless it changes to GUIDED
            self.vehicle.mode = VehicleMode("GUIDED")
            while not self.vehicle.mode.name == "GUIDED":
                sleep(1)
                
            if (self.vehicle.mode.name == "GUIDED"):
                if not self.vehicle.armed:
                    self.vehicle.armed = True
                
                else:
                    # Disarm if landed
                    if (self.vehicle.location.global_relative_frame.alt < self.THRESHOLD_ALT):
                        self.vehicle.armed = False
           
        elif (kp == 'h'):
            print("Stabilize Mode")
            @self.vehicle.on_attribute('mode')
            def mode_callback(self,attr_name, value):
                print(f">> Mode Updated: {value}")
                
            self.vehicle.mode = VehicleMode("STABILIZE")
            while not self.vehicle.mode.name == "STABILIZE":
                sleep(1)
                
        # Go Up
        if (kp == 'u') : #and self.vehicle.armed:
            print("Take Off")
            # if (self.vehicle.location.global_relative_frame.alt < self.THRESHOLD_ALT):
            #     takeoff_alt = 2
            #     self.vehicle.simple_takeoff(takeoff_alt)
            #     while self.vehicle.location.global_relative_frame.alt < (takeoff_alt - self.THRESHOLD_ALT):
            #         sleep(0.3)
            # else:
            #     if (self.vehicle.location.global_relative_frame.alt > self.THRESHOLD_ALT):
            #         self.vehicle.mode = VehicleMode("LAND")
        
        # Go Right
        elif (kp == 'd') : #and self.vehicle.armed:
            print("Go Right")
        #     x,y = 0.0, 2.0 
        #     yaw = self.vehicle.attitude.yaw
        #     self.engine_imp.send_global_velocity(
        #         x * np.cos(yaw) - y * np.sin(yaw),
        #         x * np.sin(yaw) + y * np.cos(yaw),
        #         0,
        #         2,      
        #     )
        #     self.engine_imp.send_global_velocity(0,0,0,1)

        # Go Left
        elif (kp == 'a') : #and self.vehicle.armed:
             print("Go Left")
        #     x,y = 0.0, -2.0 
        #     yaw = self.vehicle.attitude.yaw
        #     self.engine_imp.send_global_velocity(
        #         x * np.cos(yaw) - y * np.sin(yaw),
        #         x * np.sin(yaw) + y * np.cos(yaw),
        #         0,
        #         2,      
        #     )
        #     self.engine_imp.send_global_velocity(0,0,0,1)
            
        # Go Back
        elif (kp == 's') : #and self.vehicle.armed:
            print("Go Back")
            # x, y = -2.0, 0.0  # meters
            # yaw = self.vehicle.attitude.yaw
            # self.engine_imp.send_global_velocity(
            #     x * np.cos(yaw) - y * np.sin(yaw),
            #     x * np.sin(yaw) + y * np.cos(yaw),
            #     0,
            #     2,
            # )
            # self.engine_imp.send_global_velocity(0, 0, 0, 1)
            
        # Go Front
        elif (kp == 'w') : #and self.vehicle.armed:
            print("Go Front")
            # x, y = 2.0, 0.0  # meters
            # yaw = self.vehicle.attitude.yaw
            # self.engine_imp.send_global_velocity(
            #     x * np.cos(yaw) - y * np.sin(yaw),
            #     x * np.sin(yaw) + y * np.cos(yaw),
            #     0,
            #     2,
            # )
            # self.engine_imp.send_global_velocity(0, 0, 0, 1)

        # Land   
        elif (kp == 'q') : #and self.vehicle.armed:
            print("Land")
            # self.vehicle.channels.overrides = {}
            # self.vehicle.mode = VehicleMode("LAND")
            # self.vehicle.armed = False

        # Stop Movement
        elif (kp == 'e') : #and self.vehicle.armed:
            print("Stop movement")
            # x,y,z = 0,0,0
            # self.engine_imp.send_global_velocity(
            # x,
            # y,
            # z,
            # 2, 
            # )
            # self.engine_imp.send_global_velocity(0, 0, 0, 1)

        # Yaw Left
        elif (kp == 'l') : #and self.vehicle.armed:
            print("Yaw Left")
            #self.engine_imp.send_movement_command_YAW(-10)

        # Yaw Right
        elif (kp == 'r') : #and self.vehicle.armed:
            print("Yaw RIGHT")
            #self.engine_imp.send_movement_command_YAW(10)

        # Reset
        elif (kp =='f'):
            print("Reset Status")

    #sleep(0.25)

    
if __name__ == "__main__":
    init = readdatafromArdtoRpi()
    """use tx and rx port"""
    #ser = init.initConnection("/dev/ttyAMA0", 9600)

    """use usb connection port"""
    ser = init.initConnection("/dev/ttyUSB0", 9600)

    while True:
        receivedata = init.getData(ser)
        vals = init.getKeyboardInput(receivedata)
        #print(vals)

        
    
