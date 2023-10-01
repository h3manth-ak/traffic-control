import tensorflow as tf
import numpy as np
from PIL import Image
import cv2
import time
import os
import vehcount 
import matplotlib.pyplot as plt
import operator
import ambulance
import smtplib

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
app=FastAPI()



num=1
# Load the model
model_count = tf.keras.models.load_model('model_1.h5')
interpreter = tf.lite.Interpreter(model_path = 'tf_lite_model.tflite')

origins = [
    "http://localhost",
    "http://localhost:8000"
    "http://localhost:8080",
    "http://localhost:3000/"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




counts = {'A': {'count': 0, 'priority': 0},
          'B': {'count': 0, 'priority': 0},
          'C': {'count': 0, 'priority': 0},
          'D': {'count': 0, 'priority': 0}}


@app.get("/")

def get_max_count_kunu(): 
    global num

        # Replace this with your shedule() function logic
    arr= shedule()

    # arr=[max_count,kunu]
    # Rest of your shedule() logic...
    print(arr)
    # return {"max_count": max_count, "kunu": kunu}
    return arr

def send_email():
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login("test49415@gmail.com", "wzgd jdol rinh uatq")
    subject = 'Accident Alert'
    body = 'Accident has been detected '
    message = f'Subject: {subject}\n\n{body}'
    s.sendmail("test49415@gmail.com", "vaishnavvijayan25@gmail.com", message)
    s.quit()
# count the number of vehicles
def vehicles(img_path,traffic):

    count=vehcount.count(img_path)
    counts[traffic]['count'] = count
    print(f'{traffic}:count={count}')
    return count


# accident detect
def accident(img_path,traffic):
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    interpreter.resize_tensor_input(input_details[0]['index'], (1, 250, 250,3))
    interpreter.resize_tensor_input(output_details[0]['index'], (1, 2))
    interpreter.allocate_tensors()
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    im=Image.open(img_path).resize((250,250))
    img_array = tf.keras.utils.img_to_array(im)
    img_batch = np.expand_dims(img_array, axis=0)
    interpreter.set_tensor(input_details[0]['index'], img_batch)
    interpreter.invoke()
    tflite_model_predictions = interpreter.get_tensor(output_details[0]['index'])
    # print("Prediction results:", tflite_model_predictions)
    if tflite_model_predictions[0][0] > 0.5:
        print(traffic +" : Accident")
        send_email()
        return True
        
    else:
        print(traffic + ' : NON Accident')
        return False

    # print(plt.imshow(im))
# traffic_signals={"Signal A": "./data/test/Accident/test4_37.jpg",
#         "Signal B": "./data/test/Non Accident/test1_9.jpg",
#         "Signal C": "./data/test/Accident/test1_27.jpg",  # Replace with actual image paths
#         "Signal D": "./data/test/Non Accident/test4_60.jpg",  # Replace with actual image paths}
# }


def is_ambulance(img_src,traffic):
    result = ambulance.is_ambulance_detected(img_src)
    if result:
        print(traffic + ": Ambulance detected!")
        return 1
    else:
        return 0







print(counts)

def shedule():
    
    global num  # Declare num as a global variable
    
    path = f'./result/A/{num}.jpg'
    path1 = f'./result/B/{num}.jpg'
    path2 = f'./result/C/{num}.jpg'
    path3 = f'./result/D/{num}.jpg'
    
    path4 = f'./result/accident/A/{num}.jpg'
    path5 = f'./result/accident/B/{num}.jpg'
    path6 = f'./result/accident/C/{num}.jpg'
    path7 = f'./result/accident/D/{num}.jpg'
    
    path8 = f'./result/Ambulance/A/{num}.jpg'
    path9 = f'./result/Ambulance/B/{num}.jpg'
    path10 = f'./result/Ambulance/C/{num}.jpg'
    path11 = f'./result/Ambulance/D/{num}.jpg'
    
    if num < 16:
        num += 1
    else:
        num = 1
        
    kunu=""
    # accident(path,"A")
    vehicles(path,"A")
    # accident(path1,"B")
    vehicles(path1,"B")
    # accident(path2,"C")
    vehicles(path2,"C")
    # accident(path3,"D")
    vehicles(path3,"D")

    


    
    

    if(accident(path4,"A")):
        kunu="A"
    elif(accident(path5,"B")):
        kunu="B"
    elif(accident(path6,"C")):
        kunu="C"
    elif(accident(path7,"D")):
        kunu="D"
    
    if(is_ambulance(path8,"A")):
        return "A",kunu
    elif(is_ambulance(path9,"B")):
        return "B",kunu
    elif(is_ambulance(path10,"C")):
        return "C",kunu
    elif(is_ambulance(path11,"D")):
        return "D",kunu




    max_traffic = max(counts.items(), key=lambda x: x[1]['count'])[0]
    print(max_traffic)
    max_priority = max(counts.items(), key=lambda x: x[1]['priority'])[0]
    print(max_priority)


    consideration_list=[]

    consideration_list.append(max_priority);

    for i in counts:
        if(i!=max_priority):
            if(abs(counts[i]['priority']-counts[max_priority]['priority'])<=1):
                consideration_list.append(i)
        
    print(consideration_list)

    # counts_in_consideration = [counts[key]['count'] for key in consideration_list]
    max_count_key = max(consideration_list, key=lambda key: counts[key]['count'])
    print(max_count_key)

    counts[max_count_key]['priority'] =0
    for i in counts:
        if(i!=max_count_key):
            counts[i]['priority'] +=1

    # print(counts)
    print(kunu)

    arr=[max_count_key,kunu]
    print(arr)
    return arr

get_max_count_kunu()

# shedule()






