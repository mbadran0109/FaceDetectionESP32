import cv2
import numpy as np
import face_recognition
import os
import urllib.request
import serial
import time

# Arduino setup
arduino = serial.Serial(port='COM14', baudrate=9600, timeout=0.1)

# Define the `write_read` function
def write_read(x):
    try:
        arduino.write(bytes(x, 'utf-8'))
        time.sleep(0.05)
        data = arduino.readline()
        return data.decode('utf-8').strip()  # Decode bytes to string
    except Exception as e:
        return f"Error: {e}"

# Face recognition setup
path = r'D:\PSC\arduino\RAWFace Detection\image_folder'
url='http://192.168.202.224/capture'
images = []
classNames = []
myList = os.listdir(path)

# Load and encode images
for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])

def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

encodeListKnown = findEncodings(images)
print("Encoding Complete")

# Camera loop
while True:
    img_resp = urllib.request.urlopen(url)
    imgnp = np.array(bytearray(img_resp.read()), dtype=np.uint8)
    img = cv2.imdecode(imgnp, -1)
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    facesCurFrame = face_recognition.face_locations(imgS)
    encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

    led_state = "0"  # Default: No action

    for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
        matchIndex = np.argmin(faceDis)

        if matches[matchIndex]:
            name = classNames[matchIndex].upper()
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

            if name == "OMAR ESLAM":
                led_state = "3"  # Command to open servo 1 to 90 degrees
            elif name == "MAHA":
                led_state = "4"  # Command to open servo 2
            elif name == "ABOROKAYA":
                led_state = "5"  # Command to open servo 3
            elif name == "MALAK":
                led_state = "6"  # Command to open servo 4
            else:
                led_state = "1"  # Recognized face, turn on green LED
        else:
            # If a face is detected but not recognized
            led_state = "2"  # Unrecognized face, turn on red LED

    # Send command to Arduino
    arduino_response = write_read(led_state)
    print(f"Command Sent: {led_state}, Arduino Response: {arduino_response}")

    cv2.imshow('ESP32', img)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break

cv2.destroyAllWindows()