import cv2
import numpy as np

cap = cv2.VideoCapture(0)

while True:
    _, frame = cap.read()
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Red color
    low_red = np.array([0, 52, 20])
    high_red = np.array([15, 255, 255])
    red_mask = cv2.inRange(hsv_frame, low_red, high_red)
    red = cv2.bitwise_and(frame, frame, mask=red_mask)
    
    # Blue color
    low_blue = np.array([94, 80, 2])
    high_blue = np.array([126, 255, 255])
    blue_mask = cv2.inRange(hsv_frame, low_blue, high_blue)
    blue = cv2.bitwise_and(frame, frame, mask=blue_mask)
    
    # Every color except white
    low = np.array([0, 52, 2])
    high = np.array([126, 255, 255])
    mask = cv2.inRange(hsv_frame, low, high)
    result = cv2.bitwise_and(frame, frame, mask=mask)
    
    cv2.imshow("Frame", frame)
    cv2.imshow("Red", red)
    cv2.imshow("Blue", blue)
    cv2.imshow("Result", result)

    key = cv2.waitKey(1)
    if key == 27:
        break
    elif key == ord('s'):
        cv2.imwrite('frame_image.jpg', frame)
        print("Image captured and saved as 'frame_image.jpg'")
    elif key == ord('r'):
        cv2.imwrite('red_image.jpg', red)
        print("Image captured and saved as 'red_image.jpg'")
    elif key == ord('b'):
        cv2.imwrite('blue_image.jpg', blue)
        print("Image captured and saved as 'blue_image.jpg'")
    elif key == ord('a'):
        cv2.imwrite('result_image.jpg', result)
        print("Image captured and saved as 'result_image.jpg'")            
        
cap.release()
cv2.destroyAllWindows()
