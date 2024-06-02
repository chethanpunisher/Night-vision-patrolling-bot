from imutils.video import VideoStream
from imutils.video import FPS
import face_recognition
import imutils
import pickle
import time
import cv2
from multiprocessing import Process, Queue

flag = True
# Load face encodings
encodingsP = "encodings.pickle"
data = pickle.loads(open(encodingsP, "rb").read())
face_cascade_path = 'haarcascade_frontalface_default.xml'
face_cascade = cv2.CascadeClassifier(face_cascade_path)
recog = False

fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi', fourcc, 20.0, (320, 240))
# Initialize video stream
#vs = VideoStream(usePiCamera=True).start()
#time.sleep(2.0)

# Start FPS counter
fps = FPS().start()

# Set number of processes for multiprocessing
NUM_PROCESSES = 4  # Adjust this based on the number of CPU cores available

# Function for face recognition
def recognize_faces(frame, locations, results):
    encodings = face_recognition.face_encodings(frame, locations)
    names = []
    for encoding in encodings:
        matches = face_recognition.compare_faces(data["encodings"], encoding)
        name = "Unknown"
        if True in matches:
            recog = True
            matchedIdxs = [i for (i, b) in enumerate(matches) if b]
            counts = {}
            for i in matchedIdxs:
                name = data["names"][i]
                counts[name] = counts.get(name, 0) + 1
            name = max(counts, key=counts.get)
        names.append(name)
    results.put(names)

# Multiprocessing function
def multiprocessing_func(frame, locations, results):
    processes = []
    for i in range(NUM_PROCESSES):
        process = Process(target=recognize_faces, args=(frame, locations[i::NUM_PROCESSES], results))
        processes.append(process)
        process.start()
    for process in processes:
        process.join()

# Loop over frames from the video stream
def recog_run(frame1):
    #frame = vs.read()
    frame = imutils.resize(frame1, width=400)  # Resize frame for faster processing
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Find all face locations in the frame
    #faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    #print(faces)
    locations = face_recognition.face_locations(gray, model="hog")
    if flag:
        print(locations)
        
    # Only process faces if any are found
    if locations:
        results = Queue()
        multiprocessing_func(frame, locations, results)
        names = []
        for _ in range(NUM_PROCESSES):
            names.extend(results.get())

        # Display the results
        for (top, right, bottom, left), name in zip(locations, names):
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            y = top - 15 if top - 15 > 15 else top + 15
            cv2.putText(frame, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)

    out.write(frame)
    # Display the frame
    cv2.imshow("Facial Recognition", frame)


    # Update FPS counter
    fps.update()

# Stop the timer and display FPS information
fps.stop()
print("[INFO] Elapsed time: {:.2f}".format(fps.elapsed()))
print("[INFO] Approx. FPS: {:.2f}".format(fps.fps()))

# Cleanup
cv2.destroyAllWindows()



