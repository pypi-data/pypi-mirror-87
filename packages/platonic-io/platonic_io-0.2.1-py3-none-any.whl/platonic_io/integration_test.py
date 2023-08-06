import cv2.cv2 as cv2
import numpy as np
import pytesseract


def ratioCheck(area, width, height):
    ratio = float(width) / float(height)
    if ratio < 1:
        ratio = 1 / ratio
    if (area < 1063.62 or area > 73862.5) or (ratio < 3 or ratio > 6):
        return False
    return True


# ratioCheck(area = 1, width = 1)


# img = cv2.imread("test_frame.png")
img = cv2.imread("blur.png")
img = cv2.medianBlur(img, 5)

# imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
# imgHue, imgSaturation, imgValue = cv2.split(imgHSV)
# imgThresh = cv2.adaptiveThreshold(imgValue, 255.0, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
# cv2.THRESH_BINARY_INV, ADAPTIVE_THRESH_BLOCK_SIZE, cv2.ADAPTIVE_THRESH_WEIGHT)
# cv2.imshow('test', imgThresh)
# cv2.waitKey(0)
# img = cv2.resize(img, (620, 480))
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # convert to grey scale
# gray = cv2.bilateralFilter(gray, 13, 15, 15)
edged = cv2.Canny(img, 40, 150)
cv2.imshow("sad", edged)
cv2.waitKey(0)
# _, thresh = cv2.threshold(gray, 110, 255, cv2.THRESH_BINARY)
thresh = cv2.adaptiveThreshold(
    gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2
)

cv2.imshow("sad", thresh)
cv2.waitKey(0)
# cv2.imshow("img", gray)

contours, hierarchy = cv2.findContours(
    edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE
)
mask = np.zeros(img.shape, np.uint8)

# cv2.drawContours(mask, contours, -1, 255)
# for i, contour in enumerate(contours):
#     rect = cv2.minAreaRect(contour)
#     box = cv2.boxPoints(rect)
#     box = np.int0(box)
#     print('asdad', box)
#     cv2.drawContours(img,[box],0,(255,255,255),3)
#     cv2.imshow("m", mask)
#     cv2.waitKey(1)
# exit(0)
if contours:
    contour_area = [cv2.contourArea(c) for c in contours]
    max_cntr_index = np.argmax(contour_area)
    max_cnt = contours[max_cntr_index]
    max_cntArea = contour_area[max_cntr_index]
    x, y, w, h = cv2.boundingRect(max_cnt)
    # if not ratioCheck(max_cntArea,w,h):
    #     return thresh,None
    final_img = edged[y : y + h, x : x + w]
    original_cropped = img[y : y + h, : x + w]
    # return final_img,[x,y,w,h]
# mask = np.zeros(gray.shape, np.uint8)

text = pytesseract.image_to_string(final_img)

print(text)
cv2.imshow("img", final_img)
cv2.waitKey(0)
cv2.imshow("img", original_cropped)
cv2.waitKey(0)
cv2.imwrite("result.png", original_cropped)
