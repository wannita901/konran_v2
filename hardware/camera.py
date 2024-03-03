import cv2
import base64
import requests

# Function to capture image from webcam and send to backend
def capture_and_send_image():
    # Access the webcam
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_BRIGHTNESS, 5) # only for sirian's computer because my webcam is fucked.
    cap.set(cv2.CAP_PROP_SATURATION, 5)

    # Capture a frame
    ret, frame = cap.read()

    # Convert the image to base64
    _, img_encoded = cv2.imencode('.jpg', frame)
    image_data = base64.b64encode(img_encoded)

    
    # Release the webcam
    cap.release()

    # Send image data to backend
    url = 'http://ec2-3-106-231-109.ap-southeast-2.compute.amazonaws.com:5000/detect_image'  # Replace with the actual backend server IP address
    # url = "http://localhost:5000/detect_image"
    payload = {'image': image_data.decode('utf-8')}
    headers = requests.utils.default_headers()
    headers.update(
        {
            'Content-Type': 'application/json',
            'User-Agent': 'My User Agent 1.0'

        }
    )
    response = requests.post(url, json=payload, headers=headers)

    # Check response status
    if response.status_code == 200:
        print('Image uploaded successfully')
    else:
        print('Failed to upload image')


def test():
    url = 'http://ec2-13-236-116-118.ap-southeast-2.compute.amazonaws.com:5000/detect_image'
    # url = "http://127.0.0.1:5000/detect_image"
    files = { 'media': open('placeholder.png', 'rb')}
    payload = {'image': image_data.decode('utf-8')}
    headers = requests.utils.default_headers()
    headers.update(
        {
            'Content-Type': 'application/json',
            'User-Agent': 'My User Agent 1.0'

        }
    )
    response = requests.post(url, json=payload, headers=headers)

    requests.post(url, files=files, headers=headers)

# Capture and send image when the script is executed
capture_and_send_image()
# test()