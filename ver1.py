import tensorflow as tf
import numpy as np
from PIL import Image
import cv2
import time
import os
import vehcount
import matplotlib.pyplot as plt
import threading
import multiprocessing
# Load the model
model_count = tf.keras.models.load_model('model_1.h5')

path = './data/test/Accident/test4_37.jpg'
path1 = './data/test/Non Accident/test1_9.jpg'

# count the number of vehicles
def vehicles(img_path):
    
    count = vehcount.count(img_path)
    # print(count)
    return count

# accident detect
def accident(img_path):
    interpreter = tf.lite.Interpreter(model_path='tf_lite_model.tflite')
    interpreter.allocate_tensors()
    
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    interpreter.resize_tensor_input(input_details[0]['index'], (1, 250, 250, 3))
    interpreter.resize_tensor_input(output_details[0]['index'], (1, 2))
    
    im = Image.open(img_path).resize((250, 250))
    img_array = tf.keras.utils.img_to_array(im)
    img_batch = np.expand_dims(img_array, axis=0)
    
    interpreter.set_tensor(input_details[0]['index'], img_batch)
    interpreter.invoke()
    tflite_model_predictions = interpreter.get_tensor(output_details[0]['index'])
    
    # Release the interpreter (not required in some versions of TensorFlow)
    # interpreter.release()

    # print("Prediction results:", tflite_model_predictions)
    if tflite_model_predictions[0][0] > 0.5:
        # print("Accident")
        return 1
    else:
        # print('NON Accident')
        return 0

    # print(plt.imshow(im))

def count_vehicles(signal_name, img_path, stop_event):
    while not stop_event.is_set():
        count = vehicles(img_path)  # Call your vehicle counting function here
        print(f"{signal_name}: Vehicle count = {count}")
        time.sleep(2)  # Simulate vehicle counting every 2 seconds

# Function for accident detection at a signal
def detect_accident(signal_name, img_path, stop_event):
    while not stop_event.is_set():
        result = accident(img_path)  # Call your accident detection function here
        if result == 1:
            print(f"{signal_name}: Accident detected!")
        else:
            print(f"{signal_name}: No accident")
        
        time.sleep(5)

if __name__ == "__main__":
    # Define the paths to test images for accident detection
    image_paths = {
        "Signal A": "./data/test/Accident/test4_37.jpg",
        "Signal B": "./data/test/Non Accident/test1_9.jpg",
        "Signal C": "./data/test/Accident/test1_27.jpg",  # Replace with actual image paths
        "Signal D": "./data/test/Non Accident/test4_60.jpg",  # Replace with actual image paths
    }

    # Create threads for vehicle counting and accident detection for each signal
    vehicle_count_threads = []
    accident_detection_threads = []
    stop_event = multiprocessing.Event()
    for signal_name, img_path in image_paths.items():
          # Event to signal thread termination
        vehicle_count_thread = threading.Thread(target=count_vehicles, args=(signal_name, img_path, stop_event))
        accident_detection_thread = threading.Thread(target=detect_accident, args=(signal_name, img_path, stop_event))
        vehicle_count_threads.append(vehicle_count_thread)
        accident_detection_threads.append(accident_detection_thread)

    # Start all threads
    for thread in vehicle_count_threads + accident_detection_threads:
        thread.start()

    # Let threads run for some time (e.g., 10 seconds)
    time.sleep(10)

    # Signal threads to stop
    for stop_event in [threading.Event()] * len(vehicle_count_threads + accident_detection_threads):
        stop_event.set()

    # Join all threads to wait for them to complete
    for thread in vehicle_count_threads + accident_detection_threads:
        thread.join()
