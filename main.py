import face_recog
import cv2
import threading
from imutils.video import VideoStream
import time
import Drive_Module


def thread_function(vs):
    while(True):
        frame = vs.read()
        #frame1 = vs.read()
        face_recog.recog_run(frame)
        key = cv2.waitKey(1) & 0xFF

        # Quit when 'q' key is pressed
        if key == ord("q"):
            break
    vs.stop()        
        
    
def thread_function1(video):
    count = 0
    time.sleep(2)
    Drive_Module.kick_start()
    while(count < 350):
        ret,frame = video.read()
        Drive_Module.run(frame)
        if(face_recog.recog == True):
            Drive_Module.stop()
        count += 1
    Drive_Module.stop()

    
#vs = VideoStream(usePiCamera=True).start()

video = cv2.VideoCapture(0)
video.set(cv2.CAP_PROP_FRAME_WIDTH,320) # set the width to 320 p
video.set(cv2.CAP_PROP_FRAME_HEIGHT,240) # set the height to 240 p

time.sleep(2.0)
y = threading.Thread(target=thread_function1, args=(video,))
#y.start()
flag = 0

c = 0
while c == 0:
    ret,frame = video.read()
    #frame1 = vs.read()
    face_recog.recog_run(frame)
    key = cv2.waitKey(1) & 0xFF

    # Quit when 'q' key is pressed
    if flag == 0:
        y.start()
        flag = 1
        
    if key == ord("q"):
        break


face_recog.out.release()
video.release()
cv2.destroyAllWindows()

#x = threading.Thread(target=thread_function, args=(vs,))
#x.start()
