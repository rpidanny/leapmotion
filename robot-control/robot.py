################################################################################
# Copyright (C) 2012-2013 Leap Motion, Inc. All rights reserved.               #
# Leap Motion proprietary and confidential. Not for distribution.              #
# Use subject to the terms of the Leap Motion SDK Agreement available at       #
# https://developer.leapmotion.com/sdk_agreement, or another agreement         #
# between Leap Motion and you, your company or other organization.             #
################################################################################

import Leap, sys
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture

import socket

TCP_IP = '192.168.0.108'
TCP_PORT = 5011
BUFFER_SIZE = 1

network=1


previousPitch=0
previousRoll=0

previousdata=0

rightflag=0
leftflag=0
upflag=0
downflag=0

if(network==1):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))
    s.send('danny')
        
def sendData(data):
    global previousdata
    global s
    if(data!=previousdata):
        print data
        if(network==1):
            s.send(data)
    previousdata=data
    

class SampleListener(Leap.Listener):
    def on_init(self, controller):
        print "Initialized"

    def on_connect(self, controller):
        print "Connected"

        # Enable gestures
        controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE);
        controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SCREEN_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SWIPE);

    def on_disconnect(self, controller):
        # Note: not dispatched when running in a debugger.
        print "Disconnected"

    def on_exit(self, controller):
        print "Exited"

    def on_frame(self, controller):

        global previousPitch
        global previousRoll
        global rightflag
        global leftflag
        global upflag
        global downflag
        # Get the most recent frame and report some basic information
        frame = controller.frame()

        #print "Frame id: %d, timestamp: %d, hands: %d, fingers: %d, tools: %d, gestures: %d" % (
              #frame.id, frame.timestamp, len(frame.hands), len(frame.fingers), len(frame.tools), len(frame.gestures()))

        if not frame.hands.is_empty:
            # Get the first hand
            hand = frame.hands[0]

            # Check if the hand has any fingers
            fingers = hand.fingers
            if not fingers.is_empty:
                # Calculate the hand's average finger tip position
                avg_pos = Leap.Vector()
                for finger in fingers:
                    avg_pos += finger.tip_position
                avg_pos /= len(fingers)
                #print "Hand has %d fingers, average finger tip position: %s" % (
                      #len(fingers), avg_pos)


            # Get the hand's normal vector and direction
            normal = hand.palm_normal
            direction = hand.direction
            
            # Calculate the hand's pitch, roll, and yaw angles
            pitch =direction.pitch * Leap.RAD_TO_DEG
            roll =normal.roll * Leap.RAD_TO_DEG
            yaw =direction.yaw * Leap.RAD_TO_DEG
            #print "Hand pitch: %f degrees, roll: %f degrees, yaw: %f degrees" % (
                #pitch,
                #roll,
                #yaw)
            if(((roll<10 and roll>=-25) or (roll>45 and roll <=-45)) and ((pitch<15 and pitch>-15) or (pitch>50 and pitch < -50))):
                sendData("H")
                rightflag=0
                leftflag=0
                upflag=0
                downflag=0
            else:
                if(roll >= 10 and roll<=45):
                    #left
                    #print "left"
                    leftflag=leftflag+1
                    rightflag=0
                elif(roll<-25 and roll>-45):
                    #right
                    #print "right"
                    rightflag=rightflag+1
                    leftflag=0
                #else :
                    #stop
                    #sendData("stop Roll")
                    #rightflag=0
                    #leftflag=0
                    
                if(pitch>=15 and pitch<=50):
                    #print "Up"
                    upflag=upflag+1
                    downflag=0
                elif(pitch<=-15 and pitch>=-50):
                    #print "down"
                    downflag=downflag+1
                    upflag=0
                #else :
                    #stop
                    #sendData("stop Pitch")
                    #downflag=0
                    #upflag=0



            if(rightflag==10):
                sendData("R")
                rightflag=0
            if(leftflag==10):
                sendData("L")
                leftflag=0
            if(upflag==10):
                sendData("B")
                upflag=0
            if(downflag==10):
                sendData("F")
                downflag=0


            
            #previousPitch=pitch
            #previousRoll=roll
           
        #if not (frame.hands.is_empty and frame.gestures().is_empty):
            #print ""

    def state_string(self, state):
        if state == Leap.Gesture.STATE_START:
            return "STATE_START"

        if state == Leap.Gesture.STATE_UPDATE:
            return "STATE_UPDATE"

        if state == Leap.Gesture.STATE_STOP:
            return "STATE_STOP"

        if state == Leap.Gesture.STATE_INVALID:
            return "STATE_INVALID"

def main():
    # Create a sample listener and controller
    listener = SampleListener()
    controller = Leap.Controller()

    # Have the sample listener receive events from the controller
    controller.add_listener(listener)

    # Keep this process running until Enter is pressed
    print "Press Enter to quit..."
    sys.stdin.readline()

    # Remove the sample listener when done
    controller.remove_listener(listener)
    s.close()

if __name__ == "__main__":
    main()
