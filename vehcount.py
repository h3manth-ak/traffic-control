# import cv2
# import numpy as np

# # Load YOLOv3 model with pre-trained weights and configuration file
# net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")

# # Load COCO class names (80 classes including "car" and "truck")
# classes = []
# with open("coco.names", "r") as f:
#     classes = f.read().strip().split("\n")

# # Load image
# image = cv2.imread("image.jpeg")
# height, width, _ = image.shape

# # Create a blob from the image (416x416 is the input size for YOLOv3)
# blob = cv2.dnn.blobFromImage(image, 1/255.0, (416, 416), swapRB=True, crop=False)

# # Set the input to the YOLOv3 network
# net.setInput(blob)

# # Get layer names and output layers
# layer_names = net.getLayerNames()
# output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]

# # Run forward pass to get detections
# detections = net.forward(output_layers)

# # Initialize variables to count vehicles
# vehicle_count = 0

# # Loop through the detections and count vehicles
# for detection in detections:
#     for obj in detection:
#         scores = obj[5:]
#         class_id = np.argmax(scores)
#         confidence = scores[class_id]
        
#         # Check if the detection belongs to a vehicle class (e.g., car, truck)
#         if confidence > 0.5 and classes[class_id] in ["car", "truck", "motorcycle", "bicycle"]:
#             # If any vehicle is detected, count it
#             vehicle_count += 1

# # Print the total number of vehicles
# print("Total number of vehicles detected:", vehicle_count)

# # Display the image with bounding boxes around vehicles
# for obj in detections:
#     for obj in obj:
#         scores = obj[5:]
#         class_id = np.argmax(scores)
#         confidence = scores[class_id]
        
#         # Check if the detection belongs to a vehicle class (e.g., car, truck)
#         if confidence > 0.5 and classes[class_id] in ["car", "truck", "motorcycle", "bicycle"]:
#             # Get coordinates of the bounding box
#             center_x = int(obj[0] * width)
#             center_y = int(obj[1] * height)
#             w = int(obj[2] * width)
#             h = int(obj[3] * height)
            
#             # Calculate coordinates of the top-left corner
#             x = int(center_x - w / 2)
#             y = int(center_y - h / 2)
            
#             # Draw bounding box and label on the image
#             cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
#             cv2.putText(image, "Vehicle", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

# # Display the image with bounding boxes
# cv2.imshow("Vehicle Detection", image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()



import cv2
import numpy as np

def count(path):
# Load YOLOv3 model with pre-trained weights and configuration file
    net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")
    print(path)
    # Load image
    image = cv2.imread(path)
    height, width, _ = image.shape

    # Create a blob from the image (416x416 is the input size for YOLOv3)
    blob = cv2.dnn.blobFromImage(image, 1/255.0, (416, 416), swapRB=True, crop=False)

    # Set the input to the YOLOv3 network
    net.setInput(blob)

    # Get layer names and output layers
    layer_names = net.getLayerNames()
    output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]

    detections = net.forward(output_layers)

    # Initialize a variable to count all objects
    # Initialize a variable to count all objects
    object_count = 0
    conf_threshold = 0.25  # Adjust this threshold as needed

    # Initialize lists to store bounding boxes and confidence scores
    boxes = []
    confidence_scores = []

    # Loop through the detections and count all objects
    for detection in detections:
        for obj in detection:
            scores = obj[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > conf_threshold:
                # If any object is detected, count it
                object_count += 1
                # Get coordinates of the bounding box
                center_x = int(obj[0] * width)
                center_y = int(obj[1] * height)
                w = int(obj[2] * width)
                h = int(obj[3] * height)
                # Calculate coordinates of the top-left corner
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)
                # Append bounding box and confidence score to lists
                boxes.append([x, y, x + w, y + h])
                confidence_scores.append(confidence)
    # print(object_count)
    ## Apply non-maximum suppression to eliminate redundant detections
    nms_indices = cv2.dnn.NMSBoxes(boxes, confidence_scores, conf_threshold, 0.4)

    # Print the total number of objects after NMS
    # print("Total number of objects detected after NMS:", len(nms_indices))
    obj_count=len(nms_indices);
    # Display the image with bounding boxes around objects
    for idx in nms_indices:
        # Get the index value directly
        x, y, x2, y2 = boxes[idx]
        confidence = confidence_scores[idx]
        
        # Draw bounding box on the image
        cv2.rectangle(image, (x, y), (x2, y2), (0, 255, 0), 2)
        label = f"Confidence: {confidence:.2f}"
        cv2.putText(image, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Display the image with bounding boxes
    # cv2.imshow("Object Detection", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return obj_count

# count('img.jpg')