from AirTrafficControl import *
import keyboard as kp

class guided_no_gps:
    def __init__(self):
        self.copter = Tower()
        self.copter.USB = "127.0.0.1:14551"
        self.copter.BAUDRATE = 115200
        self.copter.initialize()
        print("Copter Initialized !")

        self.vehicle = StandardAttitudes()

        self.mode_t = 0
        self.mode_l = 0
        self.mode_s = 0

    def getKeyboardInput(self):
        if kp.is_pressed('t'):
            self.mode_t +=1
            if self.mode_t < 2:     
                print("Vehicle Mode: Takeoff")
                self.copter.takeoff(15)
                self.mode_l = 0

        elif kp.is_pressed('h'):
            print("Vehicle Mode: Hover")
            self.copter.hover()
        
        elif kp.is_pressed('l'):
            self.mode_l +=1
            if self.mode_l < 2:
                print("Vehicle Mode: Land")
                self.copter.land()
                self.mode_t = 0

        elif kp.is_pressed('w'):
            print("Vehicle Mode: Forward")
            self.vehicle.forward

        elif kp.is_pressed('s'):
            print("Vehicle Mode: Backward")
            self.vehicle.backward
        
        elif kp.is_pressed('a'):
            print("Vehicle Mode: Left")
            self.vehicle.left

        elif kp.is_pressed('d'):
            print("Vehicle Mode: Right")
            self.vehicle.right
        
if __name__ == "__main__":
    init = guided_no_gps()
    while True:
        init.getKeyboardInput()