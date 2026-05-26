from flask import Flask, jsonify, Response
from flask_cors import CORS
import cv2

from shared import parking_data
from main import process_frame

app = Flask(__name__)

CORS(app)

# -----------------------------------
# API ROUTE
# -----------------------------------
@app.route('/parking-data')
def parking_data_api():

    return jsonify(parking_data)

# -----------------------------------
# VIDEO STREAM
# -----------------------------------
def generate_frames():

    while True:

        frame = process_frame()

        if frame is None:
            break

        ret, buffer = cv2.imencode('.jpg', frame)

        frame_bytes = buffer.tobytes()

        yield (
            b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' +
            frame_bytes +
            b'\r\n'
        )

# -----------------------------------
# VIDEO ROUTE
# -----------------------------------
@app.route('/video')
def video():

    return Response(
        generate_frames(),
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )

# -----------------------------------
# MAIN
# -----------------------------------
if __name__ == '__main__':

    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
        use_reloader=False
    )