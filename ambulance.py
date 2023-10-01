import cv2
print(cv2.__version__)

def tru_condi():
	print("True")
	return True

cascade_src = './cascade.xml'
video_src = './amb.png'
#video_src = 'dataset/video2.avi'

import cv2

def is_ambulance_detected(video_src):
    cascade_src = './cascade.xml'
    car_cascade = cv2.CascadeClassifier(cascade_src)
    cap = cv2.imread(video_src)  # You may want to capture frames from a video source, not imread

    # Convert the image to grayscale
    gray = cv2.cvtColor(cap, cv2.COLOR_BGR2GRAY)

    # Detect ambulances of different sizes in the input image
    ambulances = car_cascade.detectMultiScale(gray, 1.1, 5)

    # Check if at least one ambulance is detected
    if len(ambulances) > 0:
        return True
    else:
        return False

# Example usage
# result = is_ambulance_detected(video_src)

# if result:
#     print("Ambulance detected!")
# else:
#     print("No ambulance detected.")

	

