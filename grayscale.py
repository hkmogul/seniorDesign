import numpy as np
import cv2

cap = cv2.VideoCapture(0)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


    picTaken = 0
    # Display the resulting frame
    cv2.imshow('frame',gray)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    if cv2.waitKey(1) == ord('s'):
        cv2.imwrite('selfie{0}.png'.format(picTaken), frame)
        picTaken +=1
        print '{0} picture taken!'.format(picTaken)
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
