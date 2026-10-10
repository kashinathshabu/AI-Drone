#import faceDetection as face
#import direction
#from FaceDetection import faceDetection as face
import ROI_tracking as track

def face_track():

    while True:
        x,y=face.face_track()
        print("x",x ,"y",y)
        if x<0:
            direction.d_t_left()
        if x>0:
            direction.d_t_right()
        if y<0:
            direction.d_m_foreward()
        if y>0:
            direction.d_m_backward()


def roi_tarck():
    while True:
        x,y=track.track()
        print("x",x,"y",y)
        if y<100 or y>100:
            if y<100:
                direction.d_m_foreward()
            if y>100:
                direction.d_m_backward()
        elif x<100 or x>100:
            if x<100:

                direction.d_t_left()
            if x>100:
                direction.d_t_right()


roi_tarck()
#face_track()