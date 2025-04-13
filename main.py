
import cv2
import numpy as np
from actions import perform_action

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)

    roi = frame[100:300, 350:550]
    cv2.rectangle(frame, (350, 100), (550, 300), (0, 255, 0), 5)

    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    lower_skin = np.array([0, 20, 70], dtype=np.uint8)
    upper_skin = np.array([20, 255, 255], dtype=np.uint8)

    mask = cv2.inRange(hsv, lower_skin, upper_skin)
    mask = cv2.dilate(mask, np.ones((3, 3), np.uint8), iterations=4)
    mask = cv2.GaussianBlur(mask, (5, 5), 100)

    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        max_contour = max(contours, key=cv2.contourArea)
        hull = cv2.convexHull(max_contour, returnPoints=False)
        defects = cv2.convexityDefects(max_contour, hull)

        if defects is not None:
            count_defects = 0
            for i in range(defects.shape[0]):
                s, e, f, d = defects[i, 0]
                start = tuple(max_contour[s][0])
                end = tuple(max_contour[e][0])
                far = tuple(max_contour[f][0])
                a = np.linalg.norm(np.array(end) - np.array(start))
                b = np.linalg.norm(np.array(far) - np.array(start))
                c = np.linalg.norm(np.array(end) - np.array(far))
                angle = np.arccos((b**2 + c**2 - a**2) / (2*b*c)) * 57
                if angle <= 90:
                    count_defects += 1
                    cv2.line(roi, start, far, [0, 255, 0], 2)  # Rouge, épaisseur 2
                    cv2.line(roi, far, end, [0, 255, 0], 2) 

            font = cv2.FONT_HERSHEY_SIMPLEX
            text = f"Doigts: {count_defects + 1}"  # Afficher les doigts levés (count_defects + 1)
            cv2.putText(roi, text, (10, 30), font, 1, (255, 0, 0), 2, cv2.LINE_AA)  

            perform_action(count_defects + 1,roi)

    cv2.imshow("Main", frame)
    k = cv2.waitKey(10)
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()
