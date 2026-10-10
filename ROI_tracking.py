import cv2
import sys
import cv2.legacy

# Set up tracker.
tracker_types = ['BOOSTING', 'MIL','KCF', 'TLD', 'MEDIANFLOW', 'CSRT', 'MOSSE']
tracker_type = tracker_types[5]
# Read video
#video = cv2.VideoCapture("http://192.168.1.36:8000/stream.mjpg")
video = cv2.VideoCapture(0)
video.set(3,640) # set Width
video.set(4,480) # set Height
# Set the buffer size to 1 to reduce latency
video.set(cv2.CAP_PROP_BUFFERSIZE, 1)

relative_x =0
relative_y =0

# Create a legacy tracker based on the tracker type
def create_tracker(tracker_type):
    if tracker_type == 'BOOSTING':
        return cv2.legacy.TrackerBoosting_create()
    if tracker_type == 'MIL':
        return cv2.legacy.TrackerMIL_create()
    if tracker_type == 'KCF':
        return cv2.legacy.TrackerKCF_create()
    if tracker_type == 'TLD':
        return cv2.legacy.TrackerTLD_create()
    if tracker_type == 'MEDIANFLOW':
        return cv2.legacy.TrackerMedianFlow_create()
    if tracker_type == 'CSRT':
        return cv2.legacy.TrackerCSRT_create()
    if tracker_type == 'MOSSE':
        return cv2.legacy.TrackerMOSSE_create()



# Initialize the tracker
tracker = create_tracker(tracker_type)



# Exit if video not opened.
if not video.isOpened():
    print("Could not open video")
    sys.exit()

# Read first frame.
ok, frame = video.read()
if not ok:
    print('Cannot read video file')
    sys.exit()

# Define an initial bounding box
bbox = (287, 23, 86, 320)

# Uncomment the line below to select a different bounding box
bbox = cv2.selectROI(frame, False)

# Initialize tracker with first frame and bounding box
ok = tracker.init(frame, bbox)

# Get the size of the video frame
height, width, _ = frame.shape

# Calculate the center of the frame
center_of_frame = (width // 2, height // 2)

def track():
    while True:
        # Read a new frame
        ok, frame = video.read()
        if not ok:
            break

        # Start timer
        timer = cv2.getTickCount()

        # Update tracker
        ok, bbox = tracker.update(frame)

        # Calculate Frames per second (FPS)
        fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer);

        # Draw a red point at the center of the frame
        cv2.circle(frame, center_of_frame, radius=5, color=(0, 0, 255), thickness=-1)

        # Draw bounding box
        if ok:
            # Tracking success
            p1 = (int(bbox[0]), int(bbox[1]))
            p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
            cv2.rectangle(frame, p1, p2, (255,0,0), 2, 1)

            # Calculate the center of the bounding box
            center_of_box = (int(bbox[0] + bbox[2] / 2), int(bbox[1] + bbox[3] / 2))

            # Draw a green point at the center of the bounding box
            cv2.circle(frame, center_of_box, radius=5, color=(0, 255, 0), thickness=-1)

            # Calculate the coordinates of the center of the box relative to the center of the frame
            relative_x = center_of_box[0] - center_of_frame[0]
            relative_y = center_of_frame[1] - center_of_box[1]  # Inverting y to make the top-left corner the origin

            # Display the relative coordinates on the frame
            cv2.putText(frame, f"Box Center: ({relative_x}, {relative_y})", (center_of_box[0] + 10, center_of_box[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (50, 170, 50), 1)
        else:
            # Tracking failure
            cv2.putText(frame, "Tracking failure detected", (100,80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)

        # Display tracker type on frame
        cv2.putText(frame, tracker_type + " Tracker", (100,20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50),2)

        # Display FPS on frame
        cv2.putText(frame, "FPS : " + str(int(fps)), (100,50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50), 2)

        # Display result
        cv2.imshow("Tracking", frame)
        return (relative_x,relative_y)
        # Exit if ESC pressed
        k = cv2.waitKey(1) & 0xff
        if k == 27 : break

    video.release()
    cv2.destroyAllWindows()
track()