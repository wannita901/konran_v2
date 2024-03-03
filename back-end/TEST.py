import cv2

im = cv2.imread("data/output_images/detected_fridge.jpg")
cv2.imshow("str", im)

cv2.waitKey(0)