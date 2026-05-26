import cv2
import pickle
import cvzone
import numpy as np
import os

from shared import parking_data

# -------------------------------------------------
# VIDEO SOURCE
# -------------------------------------------------
video_path = 'carPark.mp4'

cap = cv2.VideoCapture(video_path)

# Improve streaming performance
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

# -------------------------------------------------
# LOAD PARKING POSITIONS
# -------------------------------------------------
if os.path.exists('CarParkPos'):

    with open('CarParkPos', 'rb') as f:
        posList = pickle.load(f)

else:

    print("Error: CarParkPos file not found")
    posList = []

# -------------------------------------------------
# SLOT SIZE
# -------------------------------------------------
width, height = 107, 48

# -------------------------------------------------
# GLOBAL VARIABLES
# -------------------------------------------------
available_slots = 0
occupied_slots = 0
total_slots = len(posList)
occupancy = 0

# -------------------------------------------------
# CHECK PARKING SPACE
# -------------------------------------------------
def checkParkingSpace(imgPro, img):

    global available_slots
    global occupied_slots
    global occupancy

    spaceCounter = 0

    # Loop through all slots
    for i, pos in enumerate(posList):

        x, y = pos

        # Crop parking slot area
        imgCrop = imgPro[y:y + height, x:x + width]

        # Count white pixels
        count = cv2.countNonZero(imgCrop)

        # -----------------------------------------
        # SLOT STATUS
        # -----------------------------------------
        if count < 900:

            color = (0, 255, 0)
            thickness = 5

            spaceCounter += 1

            status = "Free"

        else:

            color = (0, 0, 255)
            thickness = 2

            status = "Occupied"

        # -----------------------------------------
        # DRAW RECTANGLE
        # -----------------------------------------
        cv2.rectangle(
            img,
            pos,
            (x + width, y + height),
            color,
            thickness
        )

        # -----------------------------------------
        # SLOT NUMBER
        # -----------------------------------------
        cv2.putText(
            img,
            f'{i + 1}',
            (x + 5, y + 20),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 255),
            2
        )

        # -----------------------------------------
        # PIXEL COUNT TEXT
        # -----------------------------------------
        cvzone.putTextRect(
            img,
            str(count),
            (x, y + height - 3),
            scale=1,
            thickness=2,
            offset=0,
            colorR=color
        )

    # -------------------------------------------------
    # CALCULATIONS
    # -------------------------------------------------
    available_slots = spaceCounter

    occupied_slots = total_slots - available_slots

    if total_slots != 0:

        occupancy = round(
            (occupied_slots / total_slots) * 100
        )

    else:

        occupancy = 0

    # -------------------------------------------------
    # UPDATE SHARED DATA FOR FLASK
    # -------------------------------------------------
    parking_data["total"] = total_slots

    parking_data["occupied"] = occupied_slots

    parking_data["available"] = available_slots

    parking_data["occupancy"] = occupancy

    # -------------------------------------------------
    # TOP INFO PANELS
    # -------------------------------------------------
    cvzone.putTextRect(
        img,
        f'Free: {available_slots}/{total_slots}',
        (40, 60),
        scale=2,
        thickness=3,
        offset=10,
        colorR=(0, 200, 0)
    )

    cvzone.putTextRect(
        img,
        f'Occupied: {occupied_slots}',
        (40, 130),
        scale=2,
        thickness=3,
        offset=10,
        colorR=(0, 0, 255)
    )

    cvzone.putTextRect(
        img,
        f'Occupancy: {occupancy}%',
        (40, 200),
        scale=2,
        thickness=3,
        offset=10,
        colorR=(255, 140, 0)
    )

# -------------------------------------------------
# PROCESS FRAME FUNCTION
# -------------------------------------------------
def process_frame():

    global cap

    # Loop video continuously
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == \
       cap.get(cv2.CAP_PROP_FRAME_COUNT):

        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    # Read frame
    success, img = cap.read()

    if not success:

        print("Video frame not received")

        return None

    # -------------------------------------------------
    # IMAGE PROCESSING
    # -------------------------------------------------

    # Convert to grayscale
    imgGray = cv2.cvtColor(
        img,
        cv2.COLOR_BGR2GRAY
    )

    # Blur image
    imgBlur = cv2.GaussianBlur(
        imgGray,
        (3, 3),
        1
    )

    # Adaptive threshold
    imgThreshold = cv2.adaptiveThreshold(
        imgBlur,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV,
        25,
        16
    )

    # Median blur
    imgMedian = cv2.medianBlur(
        imgThreshold,
        5
    )

    # Dilate image
    kernel = np.ones((3, 3), np.uint8)

    imgDilate = cv2.dilate(
        imgMedian,
        kernel,
        iterations=1
    )

    # -------------------------------------------------
    # DETECTION
    # -------------------------------------------------
    checkParkingSpace(
        imgDilate,
        img
    )

    # Return processed frame
    return img