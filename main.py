from tkinter.filedialog import askopenfilename
import cv2
import numpy as np
from tkinter import Tk
Tk().withdraw()

#image ismini tkinter ile alma.
imageName = askopenfilename()
def returnChoosenColors():

    colors = []

    def mouseRGB(event,x,y,flags,param):

        nonlocal colors
        if event == cv2.EVENT_LBUTTONDOWN: #mouse sol buton kontrolü
            colorsB = imageChooseColor[y,x,0]
            colorsG = imageChooseColor[y,x,1]
            colorsR = imageChooseColor[y,x,2]
            colors = imageChooseColor[y,x]



    imageChooseColor = cv2.imread(imageName)#renk işlemleri
    cv2.namedWindow('mouseRGB')
    cv2.setMouseCallback('mouseRGB', mouseRGB)

    while (1):
        cv2.imshow('mouseRGB', imageChooseColor)
        if cv2.waitKey(20) & 0xFF == 27:
            break

    cv2.destroyAllWindows()

    return colors



# görseli alıyoruz
def read_image(path):
    return cv2.imread(path)

# görsele treshold uyguluyoruz
def find_mask(image,lower,upper):
    return cv2.inRange(image, lower, upper)

#görselde contour arama işlemi
def find_contours(mask):
    ( cnts, hierarchy) = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return cnts

# contour çiziyoruz
def show_contours(contours, image):
    cv2.drawContours(image, contours, -1, (0, 0, 255), 1)

    cv2.imshow("contours", image)

def get_main_contour(contours):
    copy = contours.copy()
    copy.sort(key=len, reverse=True)
    return copy[0]

def setBGR_Limits():

    #seçili görseldeki seçili renge bir miktar tolerans payı ekleyerek limitleri kaydetme
    BGR = np.array(returnChoosenColors())
    upper = BGR + 50
    lower = BGR
    for i in [0, 1, 2]:
        if BGR[i] < 50:
            lower[i] = 0
        else:
            lower[i] = BGR[i] - 50

    return lower,upper


if __name__ == "__main__":

    #alanın gerçek yüzölçümünü bulmak için verilen uydu görüntüsünün gerçek en boy ölçüleri alınır.
    height = int(input("Please enter real height of your geographic item :"))
    width  = int(input("Please enter real width of your geographic item :"))

    #renk limitleri belirleme
    lower,upper = setBGR_Limits()

    #işlemleri gerçekleştirmek için image seçimi
    image = read_image(imageName)
    mask = find_mask(image,lower,upper)
    contours = find_contours(mask)

    main_contour = get_main_contour(contours)
    show_contours([main_contour], image)

    area = cv2.contourArea(main_contour)

    #alan için hesaplama
    wid = image.shape[1]
    hgt = image.shape[0]

    areatotal = wid*hgt
    percoflake = area/areatotal * 100

    totalarea = height*width
    areaoflake = totalarea*percoflake/100
    print("total area is = ",areaoflake , "km2")

    key = cv2.waitKey(0)