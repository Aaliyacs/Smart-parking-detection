import cv2
import pickle
import os

# -----------------------------
# SLOT SIZE
# -----------------------------
width, height = 107, 48

# File where parking positions are stored
file_path = 'CarParkPos'

# -----------------------------
# LOAD SAVED POSITIONS
# -----------------------------
if os.path.exists(file_path):
    with open(file_path, 'rb') as f:
        posList = pickle.load(f)
else:
    posList = []


# -----------------------------
# MOUSE CLICK FUNCTION
# -----------------------------
def mouseClick(events, x, y, flags, params):
    global posList

    # LEFT CLICK → ADD PARKING SLOT
    if events == cv2.EVENT_LBUTTONDOWN:
        posList.append((x, y))

    # RIGHT CLICK → REMOVE SLOT
    elif events == cv2.EVENT_RBUTTONDOWN:

        for i, pos in enumerate(posList):

            x1, y1 = pos

            # Check if mouse click is inside rectangle
            if x1 < x < x1 + width and y1 < y < y1 + height:
                posList.pop(i)
                break

    # MIDDLE CLICK → PRINT SLOT POSITION
    elif events == cv2.EVENT_MBUTTONDOWN:

        for i, pos in enumerate(posList):
            x1, y1 = pos

            if x1 < x < x1 + width and y1 < y < y1 + height:
                print(f"Slot {i+1}: {pos}")

    # SAVE POSITIONS
    with open(file_path, 'wb') as f:
        pickle.dump(posList, f)


# -----------------------------
# CREATE WINDOW
# -----------------------------
cv2.namedWindow("Parking Slot Picker")
cv2.setMouseCallback("Parking Slot Picker", mouseClick)


# -----------------------------
# MAIN LOOP
# -----------------------------
while True:

    # LOAD IMAGE
    img = cv2.imread('carParkImg.png')

    # Safety check
    if img is None:
        print("Error: carParkImg.png not found")
        break

    # DRAW ALL PARKING SLOTS
    for i, pos in enumerate(posList):

        x, y = pos

        # Draw rectangle
        cv2.rectangle(
            img,
            (x, y),
            (x + width, y + height),
            (255, 0, 255),
            2
        )

        # Slot number
        cv2.putText(
            img,
            str(i + 1),
            (x + 5, y + 25),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 255),
            2
        )

    # INSTRUCTIONS PANEL
    cv2.rectangle(img, (10, 10), (420, 120), (0, 0, 0), -1)

    cv2.putText(
        img,
        "LEFT CLICK  : Add Slot",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (0, 255, 0),
        2
    )

    cv2.putText(
        img,
        "RIGHT CLICK : Remove Slot",
        (20, 70),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (0, 0, 255),
        2
    )

    cv2.putText(
        img,
        "Press Q to Exit",
        (20, 100),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 255, 0),
        2
    )

    # SHOW TOTAL SLOTS
    cv2.putText(
        img,
        f"Total Slots: {len(posList)}",
        (850, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (255, 255, 255),
        2
    )

    # SHOW WINDOW
    cv2.imshow("Parking Slot Picker", img)

    # EXIT
    key = cv2.waitKey(1)

    if key == ord('q'):
        break


# -----------------------------
# CLOSE WINDOWS
# -----------------------------
cv2.destroyAllWindows()