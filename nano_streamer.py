import cv2
import numpy as np
import time, struct, os, serial
import threading
from flask import Response, Flask

import detect_color as dt
import raspi_motor_driver as rp


# Image frame sent to the Flask object
global video_frame
video_frame = None

#pid variables
Kp = 1
Kd = 1
RIGHT_MAX_SPEED = 254
LEFT_MAX_SPEEED = 254
RIGHT_BASE_SPEED = 150
LEFT_BASE_SPEED = 150
lastError = 0
# Use locks for thread-safe viewing of frames in multiple browsers
global thread_lock 
thread_lock = threading.Lock()

Motor1 = {'input1': 18, 'input2': 16}
Motor2 = {'input1': 13, 'input2': 15}

# Create the Flask object for the application
app = Flask(__name__)
ser = serial.Serial('/dev/ttyACM0',115200, timeout=1)
ser.flush()
def captureFrames():
    global video_frame, thread_lock    
    #vehicle = rp.Vehicle(Motor1, Motor2)
    lastError = 0
    # Video capturing from OpenCV
    #video_capture = cv2.VideoCapture(GSTREAMER_PIPELINE, cv2.CAP_GSTREAMER)
    video_capture = cv2.VideoCapture(0)
    #frameI = cv2.imread("/home/pi/Desktop/image1.jpg")
    while True and video_capture.isOpened():
        return_key, frame = video_capture.read()
        if not return_key:
            break
        cv2.imshow('window',frame)
        # Create a copy of the frame and store it in the global variable,
        # with thread safe access
        frame = cv2.resize(frame, (640, 480))
        #cv2.imwrite("/home/pi/Desktop/img.jpg", frame)
        frame = dt.processImg(frame)
        frame, x, y = dt.centroid(frame)
        cX, cY = dt.image_centre(frame)
        #cX cY are setpoints and X Y are current value
        #code for pid
        errX = cX - x      # if the vehicle moved on right side of line the linein the camera will go to the left side of the centroid so cX>x
        motorSpeed = Kp * errX + Kd * (errX - lastError)
        lastError = errX
        rightMotorSpeed = RIGHT_BASE_SPEED - motorSpeed
        leftMotorSpeed = LEFT_BASE_SPEED + motorSpeed
        #print(errX)
        #print(leftMotorSpeed, rightMotorSpeed)
        #cv2.imshow("frame", frame)

        #print(motorSpeed)
        #cv2.circle(frame, (cX, cY), 4, (255,30,40), -1)
        dist = np.sqrt([(cX - x)**2+(cY - y)**2])
        print(int(dist[0]))
        #print(int(dist))
        if (int(dist[0]) < 400):
            
            leftMotorSpeed = 140
            rightMotorSpeed = 140
        else:
            leftMotorSpeed = 0
            rightMotorSpeed = 0
        send_data= str(leftMotorSpeed)+"#"+str(rightMotorSpeed)+"#\n"
        ser.write(send_data.encode("UTF-8"))
        line = ser.readline().decode("UTF-8").rstrip()
        print(line)
        with thread_lock:
            video_frame = frame.copy()
        
        key = cv2.waitKey(30) & 0xff
        if key == 27:
            break

    video_capture.release()
    cv2.destroyWindow("window")    
def encodeFrame():
    global thread_lock
    while True:
        # Acquire thread_lock to access the global video_frame object
        with thread_lock:
            global video_frame
            if video_frame is None:
                continue
            return_key, encoded_image = cv2.imencode(".jpg", video_frame)
            if not return_key:
                continue

        # Output image as a byte array
        yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + 
            bytearray(encoded_image) + b'\r\n')

@app.route("/")
def streamFrames():
    return Response(encodeFrame(), mimetype = "multipart/x-mixed-replace; boundary=frame")

# check to see if this is the main thread of execution
if __name__ == '__main__':

    # Create a thread and attach the method that captures the image frames, to it
    process_thread = threading.Thread(target=captureFrames)
    process_thread.daemon = True

    # Start the thread
    process_thread.start()

    # start the Flask Web Application
    # While it can be run on any feasible IP, IP = 0.0.0.0 renders the web app on
    # the host machine's localhost and is discoverable by other machines on the same network 
    app.run("0.0.0.0", port="8000")
