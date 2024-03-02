import cv2
import base64
import requests

# Function to capture image from webcam and send to backend
def capture_and_send_image():
    # Access the webcam
    cap = cv2.VideoCapture(0)

    # Capture a frame
    ret, frame = cap.read()

    # Convert the image to base64
    _, img_encoded = cv2.imencode('.jpg', frame)
    image_data = base64.b64encode(img_encoded)

    # Send image data to backend
    url = 'http://127.0.0.1:5000/detect_image'  # Replace with the actual backend server IP address
    payload = {'image': image_data.decode('utf-8')}
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, json=payload, headers=headers)

    # Check response status
    if response.status_code == 200:
        print('Image uploaded successfully')
    else:
        print('Failed to upload image')

    # Release the webcam
    cap.release()

# Capture and send image when the script is executed
capture_and_send_image()
