import cv2
import numpy as np
from picamera import PiCamera
from io import BytesIO

classifier = cv2.HOGDescriptor()
classifier.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())


def cv2Camera():
    cap = cv2.VideoCapture(1)
    cap.set(3, 640)
    cap.set(4, 480)
    
    if cap.isOpened():
        print('[!] Loading video...')
    else:
        print('[!] Failed to load video...')
        cap.release()

    while cap.isOpened():
        ret, frame = cap.read()

        if ret:
            frame = cv2.resize(frame, None, fx=0.5, fy=0.5,
                               interpolation=cv2.INTER_LINEAR)
            grayscale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # (regions, _) = classifier.detectMultiScale(grayscale, winStride=(4, 4), padding=(8, 8), scale=1.05)

            # for (x, y, w, h) in regions:
                # cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 175, 125), 2)

            cv2.imshow('frame', frame)
            
            if cv2.waitKey(1) == ord('q'):
                break

        else:
            print('[!] Could not load frame...')
            break
        
    cap.release()
    cv2.destroyAllWindows()
        
        
def piCamera():
    camera = PiCamera()
    camera.resolution = (320, 240)
    camera.framerate = 24

    while True:
        frame = np.empty((240 * 320 * 3,), dtype=np.uint8)
        camera.capture(frame, 'bgr')
        frame = frame.reshape((240, 320, 3))

        # frame = cv2.resize(image, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_LINEAR)
        # grayscale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        (regions, _) = classifier.detectMultiScale(frame, winStride=(4, 4),
                                                   padding=(8, 8), scale=1.0)

        for (x, y, w, h) in regions:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 175, 125), 2)

        cv2.imshow('frame', frame)


if __name__ == '__main__':
    cv2Camera()