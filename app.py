from flask import Flask, render_template, Response, jsonify
import cv2
import tensorflow as tf
import numpy as np
from keras.preprocessing.image import img_to_array

app = Flask(__name__)

error_message = None
camera = None
face_cascade = cv2.CascadeClassifier('haarcascades/haarcascade_frontalface_default.xml')

SmileCNN_model = tf.keras.models.load_model('cnn_model\SmileCNN.h5')

results = {
    'prob_smiling':-1
    }

def generate_frames():
    global results
    while True:

        # read frames by camera
        success, frame = camera.read()
        if not success:
            break
        else:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30,30), flags=cv2.CASCADE_SCALE_IMAGE)
            font = cv2.FONT_HERSHEY_SIMPLEX
            results = {
                'prob_smiling':-1
            }
            for (x, y, w, h) in faces:
                roi = gray[y:y+h, x:x+w]
                roi = cv2.resize(roi, (28, 28))
                roi = roi.astype("float")/255.0
                roi = img_to_array(roi)
                roi = np.expand_dims(roi, axis=0)
                temp = roi[0]                
                temp  = temp.reshape(1, 28, 28, 1)
                actual = SmileCNN_model.predict(temp)
                pred = 0
                if actual > 0.5:
                    pred = 1
                else:
                    pred = 0
                # (notSmiling, smiling) = SmileCNN_model.predict(temp)
                (notSmiling, smiling) = (1-pred,pred)
                label = "Smiling :)" if smiling > notSmiling else "Not Smiling :("
                color = (0, 255, 0) if smiling > notSmiling else (0, 0, 255)
                cv2.putText(frame,label,(10,400), font, 2, color, 2, cv2.LINE_AA)
                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
                results = {
                    'prob_smiling':(float)(actual[0][0])
                }
                break
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield(b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/get_results')
def get_results():
    return jsonify(results)

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/run')
def run():
    global error_message, camera
    camera = cv2.VideoCapture(0)
    if not camera.isOpened():
        error_message = "Error: Unable to access the camera."
        return render_template('run.html', error_message = "Error: Unable to access the camera.")
    return render_template('run.html')


if __name__ == '__main__':
    app.run(debug=True)
