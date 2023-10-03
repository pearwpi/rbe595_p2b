# Sample DJI Tello EDU code

# Illustrates the following:
#    1. states access
#    2. video feed access
#    3. control commands

# Install the following library (or download and add to sys.path)
# https://github.com/damiafuentes/DJITelloPy#djitellopy

# Example codes:
# https://github.com/damiafuentes/DJITelloPy/tree/master/examples

# DJI Tello Py library documentation:
# https://djitellopy.readthedocs.io/en/latest/tello/

# Tello UDP COMMAND documentation (used by djitellopy library):
#     [1.3](https://dl-cdn.ryzerobotics.com/downloads/tello/20180910/Tello%20SDK%20Documentation%20EN_1.3.pdf),
#     [2.0 with EDU-only commands](https://dl-cdn.ryzerobotics.com/downloads/Tello/Tello%20SDK%202.0%20User%20Guide.pdf)
#     https://djitellopy.readthedocs.io/en/latest/

#  Please note that the commands are transmitted over UDP and responses are received over UDP.
#   Sometimes command or response (ok) may not be received!
#   This code is written to handle most of such corner cases, but you may still face them!

# Ignore video decoding error!
    # non-existing PPS 0 referenced
    # non-existing PPS 0 referenced
    # decode_slice_header error
    # no frame!

# IMPORTS
import sys
import os
import cv2
import time

# sys.path.append('./DJITelloPy')
from djitellopy import Tello

# INIT TELLO CLASS
tello = Tello(retry_count=1)

# HELPERS
def takeoffHelper(tobj):
    attempt = 0
    TAKEOFF_TIMEOUT = 10
    MAX_ATTEMPT = 2
    takeoffdone = False
    while True:
        attempt += 1

        tobj.send_command_without_return("takeoff")
        start_time = time.time()

        while True:
            el_time = time.time() - start_time
            if tobj.get_distance_tof() > 60.0:
                takeoffdone = True
                print('Takeoff complete in seconds = ', el_time)
                break
            elif el_time > TAKEOFF_TIMEOUT:
                takeoffdone = False
                break
            else:
                # sleep for 1 second and check again
                time.sleep(1)
        
        if takeoffdone:
            break
        elif attempt>=MAX_ATTEMPT:
            break
            
    return takeoffdone

# THE MAIN PROGRAM
try:
    # ESTABLISH CONNECTION ------------------------------------------------------------------
    attempt = 0
    while True:
        try:
            # ENTER COMMAND MODE AND TRY CONNECTING OVER UDP
            attempt += 1
            print("Takeoff attempt ", attempt)
            tello.connect()
        except:
            print('Failed to connect or it connected but "ok" not received. Retrying...')
            if attempt > 1:
                print('Failed to connect after multiple attempts')
                exit(-1)
        else:
            # No exception 
            break

    # CHECK SENSOR READINGS------------------------------------------------------------------
    print('Altitude ', tello.get_distance_tof())
    print('Battery, ', tello.get_battery())

    # CHECK VIDEO FEED ----------------------------------------------------------------------
    tello.streamon()
    time.sleep(2)
    frame_read = tello.get_frame_read()
    time.sleep(2)
    cv2.imwrite("picture.png", frame_read.frame)

    # TAKEOFF--------------------------------------------------------------------------------
    
        #   technique 1 - Call tello.takeoff() - 
        #       in case the takeoff works but ok is not received, it will think that takeoff is incomplete
        #      tello.takeoff()

    # technique 2 - send takeoff command and dont expect a response. see if altitude crosses some preset value
    if takeoffHelper(tello) == False:
        print('takeoff failed after multiple attempts')
        exit(-1)

    count = 0
    rightVel = [30, -30, 0, 0]
    frontVel = [0, 0, 30, -30]
    wpcount = 0

    while wpcount<4:

        # READ IMAGE
        count += 1
        imgpath = f"outputs/img{count}.png"
        cv2.imwrite(imgpath, frame_read.frame)

        # SEND CONTROL ACTION
        cmd = f"rc {rightVel[wpcount]} {frontVel[wpcount]} 0 0"
        tello.send_command_without_return(cmd)

        # SLEEP / SCHEDULING LOGIC
        time.sleep(3)

        wpcount += 1

        # Send keep alive or some other command to keep tello on.
        #   Even if keep alive is sent, it can still shutdown once over heated
        # tello.send_command_without_return("keepalive")

        missionComplete = False
        if missionComplete:
            break

    tello.land()

except KeyboardInterrupt:
    # HANDLE KEYBOARD INTERRUPT AND STOP THE DRONE COMMANDS
    print('keyboard interrupt')
    tello.emergency()
    tello.emergency()
    tello.end()