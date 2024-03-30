import cv2
import numpy as np

 
net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")
classes = []
with open("coco.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]
layer_names = net.getLayerNames()
output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]
 
cap = cv2.VideoCapture('car_driving.mp4')

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
     
    frame = cv2.resize(frame, None, fx=0.8, fy=0.8)
    height, width, channels = frame.shape

     
    blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(output_layers)

    
    nearest_human = None
    nearest_vehicle = None

     
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5:
                 
                if class_id == 0:
                     
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)
                     
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)
                     
                    if nearest_human is None or w * h > nearest_human[2] * nearest_human[3]:
                        nearest_human = (x, y, w, h)
                elif class_id == 2:
                     
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)
                     
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)
                    
                    if nearest_vehicle is None or w * h > nearest_vehicle[2] * nearest_vehicle[3]:
                        nearest_vehicle = (x, y, w, h)

     
    if nearest_human is not None:
        x, y, w, h = nearest_human
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(frame, classes[0].capitalize(), (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    if nearest_vehicle is not None:
        x, y, w, h = nearest_vehicle
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cv2.putText(frame, classes[2].capitalize(), (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

     
    cv2.imshow("Detection", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
