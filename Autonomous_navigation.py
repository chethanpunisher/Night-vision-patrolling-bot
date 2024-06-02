import cv2
import numpy as np
import time
import RPi.GPIO as GPIO

def sumOfMatrix(N, M, mat):
    # Initialize sum = 0 to store sum
    # of each element
    Sum = 0

    # Traverse in each row
    for i in range(N):
        # Traverse in column of that row
        for j in range(M):
            # Add element in variable sum
            Sum += mat[i][j]

    # Return sum of matrix
    return Sum

def forward():
    # Steering Motor Control
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.HIGH)


    # Throttle Motors Control
    GPIO.output(in3, GPIO.HIGH)
    GPIO.output(in4, GPIO.LOW)

    
def back():
        # Steering Motor Control
    GPIO.output(in1, GPIO.HIGH)
    GPIO.output(in2, GPIO.LOW)


    # Throttle Motors Control
    GPIO.output(in3, GPIO.LOW)
    GPIO.output(in4, GPIO.HIGH)

def right():
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.HIGH)


    # Throttle Motors Control
    GPIO.output(in3, GPIO.LOW)
    GPIO.output(in4, GPIO.LOW)

def left():
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.LOW)


    # Throttle Motors Control
    GPIO.output(in3, GPIO.HIGH)
    GPIO.output(in4, GPIO.LOW)
    

GPIO.setwarnings(False)
# Steering Motor Pins
steering_enable = 22 # Physical Pin 15
in1 = 17 # Physical Pin 11
in2 = 27 # Physical Pin 13

#Throttle Motors Pins
throttle_enable = 25 # Physical Pin 22
in3 = 23 # Physical Pin 16
in4 = 24 # Physical Pin 18

GPIO.setmode(GPIO.BCM) # Use GPIO numbering instead of physical numbering
GPIO.setup(in1, GPIO.OUT)
GPIO.setup(in2, GPIO.OUT)
GPIO.setup(in3, GPIO.OUT)
GPIO.setup(in4, GPIO.OUT)
GPIO.setup(throttle_enable, GPIO.OUT)
GPIO.setup(steering_enable, GPIO.OUT)

steering = GPIO.PWM(steering_enable, 1000) # set the switching frequency to 1000 Hz
steering.stop()

throttle = GPIO.PWM(throttle_enable, 1000) # set the switching frequency to 1000 Hz
throttle.stop()

forward()

time.sleep(1)

count = 0;

#throttle.start(100) # starts the motor at 25% PWM signal-> (0.25 * battery Voltage) - driver's loss
#steering.start(100) # starts the motor at 100% PWM signal-> (1 * Battery Voltage) - driver's loss

time.sleep(0.1)

#throttle.start(70) # starts the motor at 25% PWM signal-> (0.25 * battery Voltage) - driver's loss
#steering.start(70) # starts the motor at 100% PWM signal-> (1 * Battery Voltage) - driver's loss
#time.sleep(1)

def kick_start():
    throttle.start(100) # starts the motor at 25% PWM signal-> (0.25 * battery Voltage) - driver's loss
    steering.start(100) # starts the motor at 100% PWM signal-> (1 * Battery Voltage) - driver's loss

    time.sleep(0.1)


def stop():
    throttle.stop()
    steering.stop()


def run(frame):
    
    #ret,frame = video.read()
    #frame = cv2.flip(frame, -1)
    time.sleep(0.01)
    
      # Load the image
    #image = cv2.imread("img2 (3).jpg")
    image = frame
    # Define the coordinates of the region to crop (top-left and bottom-right)
    x1, y1, x2, y2 = 105, 211, 242, 240  # Example coordinates

    # Crop the region of interest from the image
    cropped_image = image[y1:y2, x1:x2]

    # Convert the cropped image to grayscale
    gray_image = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)

    # Apply binary thresholding
    _, binary_image = cv2.threshold(gray_image, 215, 255, cv2.THRESH_BINARY)
    #print(len(binary_image[0]))
    n = len(binary_image)
    m = int(len(binary_image[0])/2)
    l = int(sumOfMatrix(n,m,binary_image)/2000)
    #print(l)

    n1 = int(len(binary_image)/2)
    m1 = len(binary_image[0])
    r = int(sumOfMatrix(n1,m1,binary_image)/2000)
    
    #print(r)
    print(l-r)
    # Display the original, cropped, and binary images
    #cv2.imshow("Original Image", image)
    #cv2.imshow("Cropped Image", cropped_image)
    cv2.imshow("Binary Image", binary_image)
    t = 0
    if((l-r)>0 or (l-r)<-0):
        t = (l-r)/2
    if((l-r)>40):
        t = 40/2

    if((l-r)<-40):
        t = -40/2
    cv2.imshow("original",frame)
    #cv2.imwrite('img2.jpg',frame)
    throttle.start(50-t) # starts the motor at 25% PWM signal-> (0.25 * battery Voltage) - driver's loss
    steering.start(50+t) # starts the motor at 100% PWM signal-> (1 * Battery Voltage) - driver's loss
    #count+=1

    # break

    
    
    


    
        
        
        
        

