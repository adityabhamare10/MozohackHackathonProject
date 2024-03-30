import cv2
import numpy as np

# Load YOLOv4 model and class labels
net = cv2.dnn.readNet("yolov4.weights", "yolov4.cfg")
classes = []
with open("coco.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]
layer_names = net.getLayerNames()
output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]

# Start video capture (replace "highway.mp4" with the path to your highway video)
cap = cv2.VideoCapture("car_driving.mp4")

while True:
    # Read a frame
    ret, frame = cap.read()
    if not ret:
        break

    # Resize frame for faster processing
    frame = cv2.resize(frame, None, fx=0.4, fy=0.8)
    height, width, channels = frame.shape

    # Detect objects using YOLOv4
    blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (416, 416), swapRB=True, crop=False)
    net.setInput(blob)
    outs = net.forward(output_layers)

    # Process detected objects
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5:
                # Detected object with confidence > 0.5
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)
                x = center_x - w // 2
                y = center_y - h // 2

                # Draw bounding box and label
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(frame, classes[class_id], (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Display frame with bounding boxes and labels
    cv2.imshow("Object Detection", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release video capture and close all windows
cap.release()
cv2.destroyAllWindows()
