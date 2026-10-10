import cv2
import mediapipe as mp
import time

#################################

wcam,hcam=640,480

pTime=0
cTime=0

lmList=[]
finger=[]
tipIds=[4,8,12,16,20]

################################

cap=cv2.VideoCapture(0)

##############################################

mpHands =mp.solutions.hands
hands=mpHands.Hands()
mpDraw =mp.solutions.drawing_utils

##############################################
while True:
    sucess ,img =cap.read()
    img=cv2.resize(img,(720,480))
    img=cv2.flip(img,1)

    # Convert frame to RGB format for processing

    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Process hand landmarks
    results = hands.process(imgRGB)

    # Check if hand landmarks are detected
    if results.multi_hand_landmarks:
        # Loop over detected hands
        for handLms in results.multi_hand_landmarks:
            # Loop over each landmark in the hand
            for id, lm in enumerate(handLms.landmark):
                # Get landmark positions in pixel coordinates
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                # Store landmark positions for further processing
                lmList.append([id,cx,cy])
###################################################################   

            # Finger tracking logic             
            if len(lmList)!=0:
                x1,y1=lmList[8][1:]
                x2,y2=lmList[12][1:]
            if lmList[tipIds[0]][1]>lmList[tipIds[0]-1][1]:
                finger.append(0)
            else:
                finger.append(1)
            for ids in range(1,5,):
                if lmList[tipIds[ids]][2]<lmList[tipIds[ids]-2][2]:
                    finger.append(1)
                else:
                    finger.append(0)
#########################################################################

            if finger[1]==0 and finger[0]==0 and finger[4]==0 and finger[2]==0 and finger[3]==0:
                cv2.putText(img,"down",(10,70),cv2.FONT_HERSHEY_PLAIN,3,(0,255,0),3)
            if (finger[1]==1 and (finger[0]==0 and finger[4]==0 and finger[2]==0 and finger[3]==0)):
                cv2.putText(img,"left",(10,70),cv2.FONT_HERSHEY_PLAIN,3,(0,255,0),3)
            if (finger[1]==1 and finger[2]==1 and (finger[4]==0 and finger[0]==0 and finger[3]==0)):
                cv2.putText(img,"right",(10,70),cv2.FONT_HERSHEY_PLAIN,3,(0,255,0),3)
            if (finger[0]==0 and finger[4]==0 and (finger[1]==1 and finger[2]==1 and finger[3]==1)):
                cv2.putText(img,"forward",(10,70),cv2.FONT_HERSHEY_PLAIN,3,(0,255,0),3)
            if (finger[0]==0 and (finger[1]==1 and finger[4]==1 and finger[2]==1 and finger[3]==1)):
                cv2.putText(img,"backward",(10,70),cv2.FONT_HERSHEY_PLAIN,3,(0,255,0),3)
            if finger[1]==1 and finger[0]==1 and finger[4]==1 and finger[2]==1 and finger[3]==1:
                cv2.putText(img,"up",(10,70),cv2.FONT_HERSHEY_PLAIN,3,(0,255,0),3)

            finger=[]
            lmList=[]
#######################################################################################################
            # Draw landmarks and connections on the frame
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)
####################################################################################################        
    # Calculate FPS
    cTime=time.time()
    fps=1/(cTime-pTime)
    pTime=cTime
#################################################################################################
    # Display the frame
    cv2.imshow("Image", img)
    # Check for 'q' key press to exit the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()