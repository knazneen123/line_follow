import numpy as np
import cv2

BLUE  = ([100, 15, 17],[255, 50, 56])     # defining upper and lower boundaried for blue
BLACK  = ([0, 0, 0],[100, 100, 100])     # defining upper and lower boundaried for black
WHITE  = ([240, 240, 240],[255, 255, 255])     # defining upper and lower boundaried for white

gCx = 320
gCy = 160

def processImg(img):
    img = cv2.bitwise_not(img)

    lower = np.array(WHITE[0], dtype="uint8")
    upper = np.array(WHITE[1], dtype="uint8")

    mask = cv2.inRange(img, lower, upper)
    outImg = cv2.bitwise_and(img, img, mask = mask)

    return outImg

def centroid(img):
    global gCx
    global gCy
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(img, 127,255,0)
    M = cv2.moments(thresh)
    if M["m00"] != 0:

        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
    else:
        cX = gCx
        cY = gCy

    cv2.circle(img, (cX, cY), 5, (30, 40, 250), -1)
    #print (cX, cY)
    gCx = cX
    gCy = cY

    return img, gCx, gCy

def image_centre(img):
    (h,w) = img.shape[:2]   # w-width, h-height
    #cv2.circle(img, (w//2, h//2), 5, (255, 255, 255), -1)
    #return img

    return (int(w//2), int(h//2))
