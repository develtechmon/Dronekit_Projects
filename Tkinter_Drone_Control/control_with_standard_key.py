import imp
import time
from dronekit import *
from pymavlink import mavutil

# -- Importing Tkinter : sudo apt-get install python-tk or pip install tk
import tkinter as tk

# -- Connect to the vehicle
print("Connecting")

# Local SITL Connection
#vehicle = connect('127.0.0.1:14550',wait_ready=True)

# Office Connection
vehicle = connect('10.60.217.30:14553',wait_ready=True)

print("Virtual Copter is ready")

# -- Setup the flying speed
gnd_speed = 0.5 # [m/s]

#-- Define arm and takeoff
def arm_and_takeoff(altitude):

   while not vehicle.is_armable:
      print("waiting to be armable")
      time.sleep(1)

   print("Arming motors")
   vehicle.mode = VehicleMode("GUIDED")
   vehicle.armed = True

   while not vehicle.armed: time.sleep(1)

   print("Taking Off")
   vehicle.simple_takeoff(altitude)

   while True:
      v_alt = vehicle.location.global_relative_frame.alt
      print(">> Altitude = %.1f m"%v_alt)
      if v_alt >= altitude - 1.0:
          print("Target altitude reached")
          break
      time.sleep(1)
      
 #-- Define the function for sending mavlink velocity command in body frame
def set_velocity_body(vehicle, vx, vy, vz):
    """ Remember: vz is positive downward!!!
    http://ardupilot.org/dev/docs/copter-commands-in-guided-mode.html
    
    Bitmask to indicate which dimensions should be ignored by the vehicle 
    (a value of 0b0000000000000000 or 0b0000001000000000 indicates that 
    none of the setpoint dimensions should be ignored). Mapping: 
    bit 1: x,  bit 2: y,  bit 3: z, 
    bit 4: vx, bit 5: vy, bit 6: vz, 
    bit 7: ax, bit 8: ay, bit 9:
    
    
    """
    msg = vehicle.message_factory.set_position_target_local_ned_encode(
            0,
            0, 0,
            mavutil.mavlink.MAV_FRAME_BODY_NED,
            0b0000111111000111, #-- BITMASK -> Consider only the velocities
            0, 0, 0,        #-- POSITION
            vx, vy, vz,     #-- VELOCITY
            0, 0, 0,        #-- ACCELERATIONS
            0, 0)
    vehicle.send_mavlink(msg)
    vehicle.flush()
    
    
def rotate(vehicle, direction, rotation_angle):
    msg = vehicle.message_factory.command_long_encode(
            0, 0,    # target system, target component
            mavutil.mavlink.MAV_CMD_CONDITION_YAW, #command
            0, #confirmation
            rotation_angle,  # param 1, yaw in degrees
            5,          # param 2, yaw speed deg/s
            direction,          # param 3, direction -1 ccw, 1 cw
            True, # param 4, 1 - relative to current position offset, 0 - absolute, angle 0 means North
            0, 0, 0)    # param 5 ~ 7 not used

    vehicle.send_mavlink(msg)
    vehicle.flush()

#-- Key event function
def key(event):
    if event.char == event.keysym: #-- standard keys
        if event.keysym == 'r':
            print("r pressed >> Set the vehicle to RTL")
            vehicle.mode = VehicleMode("RTL")  
        elif event.keysym == 'w':
            set_velocity_body(vehicle, gnd_speed, 0, 0)       
        elif event.keysym == 's':
            set_velocity_body(vehicle,-gnd_speed, 0, 0)     
        elif event.keysym == 'a':
            set_velocity_body(vehicle, 0, -gnd_speed, 0)      
        elif event.keysym == 'd':
            set_velocity_body(vehicle, 0, gnd_speed, 0)
        
    else: #-- non standard keys
        if event.keysym == 'Up':
            #- Takeoff
            arm_and_takeoff(10)
        elif event.keysym == 'Left':
            rotate(vehicle, -1, 10)
        elif event.keysym == 'Right':
            rotate(vehicle, 1, 10)
    
if __name__ == "__main__":
    #- Read the keyboard with tkinter
    root = tk.Tk()
    print(">> Control the drone with the arrow keys. Press r for RTL mode")
    root.bind_all('<Key>', key)
    root.mainloop()