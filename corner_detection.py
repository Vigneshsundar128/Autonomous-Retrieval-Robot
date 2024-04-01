import cv2
import numpy as np

# Initialize the camera
camera = cv2.VideoCapture(0)  # 0 for the default camera, change if needed

# Check if the camera is opened correctly
if not camera.isOpened():
    print("Error: Couldn't open camera.")
    exit()

while True:
    # Capture frame-by-frame
    ret, frame = camera.read()
    
    # Check if frame is empty
    if not ret:
        print("Error: Couldn't capture frame.")
        break

    # Convert frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect corners using Shi-Tomasi Corner Detector
    corners = cv2.goodFeaturesToTrack(gray, maxCorners=10, qualityLevel=0.01, minDistance=10)

    # Draw detected corners on the frame
    if corners is not None:
        corners = np.int0(corners)
        for corner in corners:
            x, y = corner.ravel()
            cv2.circle(frame, (x, y), 3, (0, 255, 0), -1)

    # Display the resulting frame
    cv2.imshow('Corner Detection', frame)
    
    # Save the filtered image
    if cv2.waitKey(1) & 0xFF == ord('s'):
        cv2.imwrite('corner_image.jpg', frame)
        print("Filtered image saved as 'corner_image.jpg'")

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close all OpenCV windows
camera.release()
cv2.destroyAllWindows()
