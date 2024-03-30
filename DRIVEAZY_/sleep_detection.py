import cv2
import cvzone
from cvzone.FaceMeshModule import FaceMeshDetector
from cvzone.PlotModule import LivePlot
import time
import pygame
alarm_played = False

cap = cv2.VideoCapture('sleep_detect5.mp4')
detector = FaceMeshDetector(maxFaces=1)

plotY = LivePlot(640, 360, [20, 50], invert=True)

# pointList = [22, 23, 24, 26, 110, 157, 158, 159, 160, 161, 130, 243]
pointList1 = [33, 7, 163, 144, 145, 153, 154, 155, 133, 173, 157, 158, 159, 160, 161, 246]
pointList2 = [362, 382, 381, 380, 374, 373, 390, 249, 263, 466, 388, 387, 386, 385, 384, 398]
# lower lips middle is 14
# lower_lips = [61, 146, 91, 181, 84, 17, 314, 405, 321, 375, 291, 308, 324, 318, 402, 317, 14, 87, 178, 88, 95]
lower_lips = [61, 14, 13, 291]
# right,left = 61, 291
# upper lips middle is 13
# upper_lips = [185, 40, 39, 37, 0, 267, 269, 270, 409, 415, 310, 311, 312, 13, 82, 81, 42, 183, 78]

ratioList = []
StatusOfDriver = ""
color = (255, 0, 255)
sleep_start_time = None
sleep_duration_threshold = 3
yawn_count=0

pygame.init()
alarm_sound = pygame.mixer.Sound("alarm.mp3")
while True:

    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES,0)

    success, img = cap.read()
    # img, faces = detector.findFaceMesh(img)
    img, faces = detector.findFaceMesh(img, draw=False)
    # -->   to hide FaceMesh

    if faces:
        lips = faces[0]
        for low in lower_lips:
            cv2.circle(img, lips[low], 5, color, cv2.FILLED)

        # for up in upper_lips:
        #     cv2.circle(img, lips[up], 5, color, cv2.FILLED)

        mouthleft = lips[61]
        mouthup = lips[13]
        mouthdown = lips[14]
        mouthright = lips[291]

        distVer, _ = detector.findDistance(mouthup, mouthdown)
        distHor, _ = detector.findDistance(mouthleft, mouthright)

        ratiodist = (int((distVer / distHor) * 100))
        print(ratiodist)
        if ratiodist > 50:
            yawn_count += 1

        cv2.line(img, mouthup, mouthdown, (0, 200, 0), 3)
        cv2.line(img, mouthleft, mouthright, (0, 200, 0), 3)


    if faces:
        face = faces[0]
        # for id in pointList1:
        #     cv2.circle(img, face[id], 5, color, cv2.FILLED)
        #
        # for id1 in pointList2:
        #     cv2.circle(img, face[id1], 5, color, cv2.FILLED)

        leftUp = face[159]
        leftDown = face[23]
        leftLeft = face[130]
        leftRight = face[243]





        lengthVer, _ = detector.findDistance(leftUp, leftDown)
        lengthHor, _ = detector.findDistance(leftLeft, leftRight)

        # cv2.line(img, leftUp, leftDown, (0, 200, 0), 3)
        # cv2.line(img, leftLeft, leftRight, (0, 200, 0), 3)

        ratio = (int((lengthVer/lengthHor)*100))
        if ratio < 35:
            if sleep_start_time is None:
                sleep_start_time = time.time()
            else:
                sleep_duration = time.time() - sleep_start_time
                if sleep_duration >= sleep_duration_threshold  or (yawn_count % 3 == 0 and yawn_count != 0):
                    color = (255, 0, 0)
                    StatusOfDriver = "Sleeping"
                    if not alarm_played:
                        alarm_sound.play()
                        alarm_played = True
                else:
                    StatusOfDriver = f"Eyes Closed ({sleep_duration:.1f}s)"

        else:
            color = (255, 0, 0)
            sleep_start_time = None
            StatusOfDriver = "Not-Sleeping"
            if alarm_played:
                alarm_sound.stop()
                alarm_played = False

        cvzone.putTextRect(img, StatusOfDriver, (50,100)
                           ,colorR = color)

        ratioList.append(ratio)
        if(len(ratioList))>10:
            ratioList.pop(0)
        ratioAvg = sum(ratioList)/len(ratioList)

        imgPlot = plotY.update(ratioAvg,color)
        img = cv2.resize(img, (640, 360))
        imgStack = cvzone.stackImages([img, imgPlot], 1, 1)

    else:
        img = cv2.resize(img, (640, 360))
        imgStack = cvzone.stackImages([img, img], 1, 1)

    cv2.imshow("Image", imgStack)
    cv2.waitKey(50)
