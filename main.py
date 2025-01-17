import cv2
import numpy as np
import matplotlib.pyplot as plt
from KritiCXLogicDeducer import truth_table_generator as ttg
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~  gate recognition  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
img_original1 = cv2.imread('C:/Users/Kartikaeya/Desktop/projects/CircuitX/sampl_images/T7.jpg')
w, h ,_ = img_original1.shape[:: -1]
img_original = img_original1[0 + 20: h - 20, 0 +20: w - 20]
img2 = cv2.imread('C:/Users/Kartikaeya/Desktop/projects/CircuitX/sampl_images/T7.jpg')
img = img2[0 + 20: h - 20, 0 +20: w - 20]
img3 = cv2.imread('C:/Users/Kartikaeya/Desktop/projects/CircuitX/sampl_images/T7.jpg')
plt.imshow(cv2.cvtColor(img3, cv2.COLOR_RGB2HSV))
img1 = img3[0 + 20: h - 20, 0 +20: w - 20]
def identify_gate(gate_name,img,img1,gate1):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_gate = cv2.imread('C:/Users/Kartikaeya/Desktop/projects/CircuitX/sampl_images/'+str(gate_name)+'_gate1.png',0)
    w, h  = img_gate.shape[:: -1]
    if gate_name == 'and': color = (1,255,255); threshold = 0.91; gate_type = 1
    if gate_name == 'or': color = (255,1,255); threshold = 0.9; gate_type = 2
    if gate_name == 'nand': color = (255,255,1); threshold = 0.9; gate_type = 3
    if gate_name == 'nor': color = (50,50,50); threshold = 0.8; gate_type = 4
    if gate_name == 'xor': color = (200, 50, 150); threshold = 0.8; gate_type = 5
    if gate_name == 'xnor': color = (200, 50, 50); threshold = 0.9; gate_type = 6
    if gate_name == 'not': color = (20, 150, 180); threshold = 0.8; gate_type = 7
    res = cv2.matchTemplate(gray , img_gate, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res>= threshold)
    no_of_gates = 0
    for pt in zip(*loc[::-1]):
        pt1 = np.array(pt)
        m = len(gate1)
        if(m == 0): no_of_gates+= 1; gate1.append((pt[0], pt[1],pt[0] +w, pt[1] + h, (10*gate_type + no_of_gates)))
        elif(np.linalg.norm(pt1 - np.array([ gate1[m-1][0],gate1[m-1][1] ])) >= 10): no_of_gates+= 1; gate1.append((pt[0], pt[1],pt[0] +w, pt[1] + h, (10*gate_type + no_of_gates)))
        cv2.rectangle(img, pt, (pt[0]+w, pt[1]+h), color, 2)
        cv2.rectangle(img1, pt, (pt[0] + w, pt[1] + h), color, cv2.FILLED)
        cv2.putText(img, str(gate_name), (pt[0], pt[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 1)
    return img, img1, gate1

_ ,_ , gate1 = identify_gate(gate_name='and',img =  img,img1 = img1, gate1=[])
_ ,_ , gate1 = identify_gate(gate_name='or',img = img,img1 = img1, gate1= gate1)
_ ,_ , gate1 = identify_gate(gate_name='nand',img =  img,img1 = img1,gate1= gate1)
_ ,_ , gate1 = identify_gate(gate_name='nor',img = img,img1 = img1, gate1= gate1)
_ ,_ , gate1 = identify_gate(gate_name='xor', img = img,img1 = img1, gate1= gate1)
_ ,_ , gate1 = identify_gate(gate_name='xnor', img = img,img1 = img1, gate1= gate1)
img, img1, gate1 = identify_gate(gate_name='not', img = img,img1 = img1, gate1= gate1)
print(np.array(gate1))

# ~~~~~~~~~~~~~~~~~~~~ start, end point detection ~~~~~~~~~~~~~~~~~~~~~~
def identify_point(pt_color, img, point_array):
    img_pt = cv2.imread('C:/Users/Kartikaeya/Desktop/projects/CircuitX/sampl_images/' + str(pt_color)+ '_dot.png',0)
    w, h = img_pt.shape[:: -1]
    if(pt_color == 'red'): upper_bound = np.array([1,233,234]); lower_bound = np.array([0,180,170]);color = (0,0,255); threshold = 0.8; point_type = 8
    if(pt_color == 'green'): upper_bound = np.array([56,255, 235]); lower_bound = np.array([50, 180, 203]);color = (0, 255, 0); threshold = 0.8; point_type = 9
    if (pt_color == 'blue'): upper_bound = np.array([111, 255, 235]); lower_bound = np.array([108, 180, 180]);color = (255, 0, 0); threshold = 0.8; point_type = 10
    if (pt_color == 'yellow'): upper_bound = np.array([28, 255, 255]); lower_bound = np.array([26, 150, 232]);color = (0, 255, 255); threshold = 0.8; point_type = 11
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_bound, upper_bound)
    kernel = np.ones((6, 6), np.uint8)
    dilation = cv2.dilate(mask, kernel, iterations =5)
    res1 = cv2.bitwise_and(img, img, mask=dilation)
    gray = cv2.cvtColor(res1, cv2.COLOR_BGR2GRAY)
    res = cv2.matchTemplate(gray, img_pt, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= threshold)
    no_of_points = 0
    for pt in zip(*loc[::-1]):
        pt1 = np.array(pt)
        m = len(point_array)
        if (m == 0): no_of_points += 1; point_array.append((pt[0], pt[1],pt[0] +w, pt[1] + h, (10 * point_type + no_of_points)))
        elif (np.linalg.norm(pt1 - np.array([point_array[m - 1][0], point_array[m - 1][1]])) >= 10): no_of_points += 1; point_array.append((pt[0], pt[1],pt[0] +w, pt[1] + h, (10 * point_type + no_of_points)))
        cv2.rectangle(img, pt, (pt[0] + w-10, pt[1] + h-10), color, cv2.FILLED)
    return img, point_array


_, point_array = identify_point(pt_color='red', img = img1, point_array= [])
_, point_array = identify_point(pt_color='blue', img = img1, point_array= point_array)
_, point_array = identify_point(pt_color='yellow', img = img1, point_array= point_array)
_, point_array = identify_point(pt_color='green', img = img1, point_array= point_array)


# ~~~~~~~~~~~~~~~~~~~~ mask creation and dilation ~~~~~~~~~~~~~~~~~~~~~~
hsv = cv2.cvtColor(img1, cv2.COLOR_BGR2HSV)
plt.imshow(cv2.cvtColor(img1, cv2.COLOR_BGR2HSV))
lower_value = np.array([103, 90, 146])
upper_value = np.array([104, 171, 202])
lower_value1 = np.array([103,4, 124])
upper_value1 = np.array([120, 29, 160])
lower_value2 = np.array([0,0,120])
upper_value2 = np.array([75,12,159])
mask = cv2.inRange(hsv , lower_value, upper_value)
res = cv2.bitwise_and(img1, img1, mask = mask )
mask1 = cv2.inRange(hsv , lower_value1, upper_value1)
res1 = cv2.bitwise_and(img1, img1, mask = mask1 )
mask2 = cv2.inRange(hsv , lower_value2, upper_value2)
mask = mask + mask1 + mask2

kernel = np.ones((5,5), np.uint8)
dilation = cv2.dilate(mask , kernel , iterations= 2)
w, h  = dilation.shape[:: -1]

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ finding contours ~~~~~~~~~~~~~~~~~~~~~~~~~~~
contours, hierarchy = cv2.findContours(dilation , cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
cv2.drawContours(dilation, contours, -1, (110,200,50),3)
# create hull array for convex hull points
hull =[]
# calculate points for each contour
for i in range(len(contours)):
    # creating convex hull object for each contour
    hull.append(cv2.convexHull(contours[i], False))

# create an empty black image
drawing = np.zeros((dilation.shape[0], dilation.shape[1], 3), np.uint8)

# draw contours and hull points
for i in range(len(contours)):
    color_contours = (0, 255, 0)  # green - color for contours
    color = (255, 0, 0)  # blue - color for convex hull
    # draw ith contour
    cv2.drawContours(drawing, contours, i, color_contours, 1, 8, hierarchy)
    # draw ith convex hull object
    cv2.drawContours(drawing, hull, i, color, 1, 8)
for i in range(len(hull)):
    for j in range(len(hull[i])):
        for l in range(len(hull[i][j])):
             for p in range(0,1):
                cv2.circle(drawing, (hull[i][j][l][0],hull[i][j][l][1]) , 2,(0,255,255), -1)


