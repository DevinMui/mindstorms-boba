#!/usr/bin/env python3
from ev3dev2.motor import LargeMotor, OUTPUT_A, SpeedPercent
from time import sleep

print("running")
m = LargeMotor(OUTPUT_A)
# while(True):
#     m.run_forever()
# m.on_for_rotations(SpeedPercent(75), 100)
# m.speed_sp = 1000
m.run_forever(speed_sp=1000)
# m.on(100)
while True:
    pass

print("ending")