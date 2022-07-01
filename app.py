import cv2
import numpy as np
from flask import Flask, render_template, Response

app = Flask(__name__)
classifier = cv2.HOGDescriptor()
classifier.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
cap = cv2.VideoCapture(0)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


def gen_frames():
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
            (regions, _) = classifier.detectMultiScale(grayscale, winStride=(4, 4),
                                                       padding=(8, 8), scale=1.05)

            for (x, y, w, h) in regions:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 175, 125), 2)

            success, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

        else:
            print('[!] Could not load frame...')
            break


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)
