#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      JeongHyeon
#
# Created:     11-05-2018
# Copyright:   (c) JeongHyeon 2018
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import sys
import cv2
import numpy as np
import ballTextMasker


windowH = 720
cover = windowH//3
mainShowArea = windowH - cover

ix, iy = -1,-1
drawing = False
mode = 'RECT'
modeTmp = 'RECT'
showMask = False
img = []
maskedImg = []
origin = []
noChanged=[]
back = []
mask = []
maskBack = []
maskTemp = []
maskForClear=[]
rad = 10
color = (255,255,255)
maskColor = (0,0,255)

def textDelete(event, x,y, flags, param):
    global ix, iy, drawing, img, origin, back, mask, maskBack, maskTemp, mode, rad, color, maskColor, maskForClear, noChanged

    trace = []


    if event == cv2.EVENT_LBUTTONDOWN:
        if mode == 'RECT':
            ix = x
            iy = y
        elif mode == 'DRAW' or mode == 'MANUAL':
            maskTemp = np.zeros(mask.shape,np.uint8)
            cv2.circle(img,(x,y),rad,color,-1)
            cv2.circle(maskTemp,(x,y),rad,maskColor,-1)
        elif mode == 'ERASE':
            maskForClear = np.full(mask.shape,255,np.uint8)
            #cv2.circle(img,(x,y),rad,(0,0,0),-1)
            cv2.circle(maskForClear,(x,y),rad,(0,0,0),-1)
        drawing = True
    elif event == cv2.EVENT_MOUSEMOVE:
        if mode == 'RECT':
            if drawing == True:
                img = origin.copy()
                cv2.rectangle(img,(ix,iy),(x,y),(255,0,0),1) # fixed mask color
        elif mode == 'DRAW' or mode == 'MANUAL':
            if drawing == True:
                cv2.circle(img,(x,y),rad,color,-1)
                cv2.circle(maskTemp,(x,y),rad,maskColor,-1)
        elif mode == 'ERASE':
            if drawing == True:
                cv2.circle(maskForClear,(x,y),rad,(0,0,0),-1)
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False

        if mode == 'RECT':
            img = origin.copy()
            textFinder= ballTextMasker.BalloonCleaner()
            if ix < x:
                x1 = ix
                x2 = x
            else:
                x1 = x
                x2 = ix
            if iy < y:
                y1 = iy
                y2 = y
            else:
                y1 = y
                y2 = iy
            maskBack = mask.copy()
            maskTemp, img[y1:y2+1,x1:x2+1] = textFinder.cleanBalloon(img[y1:y2+1,x1:x2+1])
            mask[y1:y2 + 1, x1:x2 + 1] = cv2.add(mask[y1:y2+1,x1:x2+1],maskTemp)
            back = origin.copy()
            origin = img.copy()
        elif mode == 'DRAW':
            if color[0] > 128:
                imgTemp = cv2.bitwise_not(origin)
            else:
                imgTemp = origin.copy()
            maskBack = mask.copy()
            back = origin.copy()
            origin = img.copy()
            maskTemp = cv2.bitwise_and(imgTemp,maskTemp)
            mask = cv2.add(mask,maskTemp)
        elif mode == 'MANUAL':
            maskBack = mask.copy()
            back = origin.copy()
            origin = img.copy()
            mask = cv2.add(mask,maskTemp)
        elif mode == 'ERASE':
            maskBack = mask.copy()
            maskBack = mask.copy()
            back = origin.copy()
            origin = img.copy()
            mask = cv2.bitwise_and(mask, maskForClear)
            gmask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
            fmask = cv2.threshold(gmask, 10, 255, cv2.THRESH_BINARY)[1]
            bmask = cv2.bitwise_not(fmask)
            fg = cv2.bitwise_and(img, img, mask=fmask)
            bg = cv2.bitwise_and(noChanged, noChanged, mask=bmask)
            img = cv2.add(fg,bg)
            maskForClear = np.full(mask.shape,255,np.uint8)
    elif event == cv2.EVENT_RBUTTONDOWN:
        if mode == 'DRAW' or mode == 'MANUAL':
            color = (img[y,x]).tolist()
            print('mode DRAW  rad = '+str(rad)+" color is ",color)






def main(srcpath,dstpath) :
    global img, maskedImg, origin, back, mask, maskBack, drawing, mode, rad , color, showMask, maskColor, maskForClear, noChanged
    Image=cv2.imread(srcpath,cv2.IMREAD_COLOR)
    Mask = np.zeros(Image.shape,np.uint8)
    roiNum = 1
    reset = False
    color = (255,255,255)
    mode = 'RECT'
    print('mode RECT')
    while True:
        if Image.shape[0] <= mainShowArea*(roiNum-1):
            break
        elif Image.shape[0] > mainShowArea*roiNum + cover:
            img = Image[mainShowArea*(roiNum-1):mainShowArea*roiNum + 1 + cover]
            mask = Mask[mainShowArea*(roiNum-1):mainShowArea*roiNum + 1 + cover]
        else:
            img = Image[mainShowArea*(roiNum-1):]
            mask = Mask[mainShowArea*(roiNum-1):]
        noChanged = img.copy()
        origin = img.copy()
        back = origin.copy()
        maskForClear = np.full(mask.shape,255,np.uint8)
        cv2.namedWindow('image')
        cv2.setMouseCallback('image',textDelete)
        while True:
            if showMask:
                m = cv2.bitwise_and(mask,maskForClear)
                gmask = cv2.cvtColor(m, cv2.COLOR_BGR2GRAY)
                fmask = cv2.threshold(gmask, 10, 255, cv2.THRESH_BINARY)[1]
                bmask = cv2.bitwise_not(fmask)
                fg = cv2.bitwise_and(mask, mask, mask=fmask)
                bg = cv2.bitwise_and(img, img, mask=bmask)
                maskedImg = cv2.add(fg,bg)
                cv2.imshow('image',maskedImg)
            else:
                cv2.imshow('image',img)
            #cv2.imshow('mask',mask)
            k = cv2.waitKey(1) & 0xFF

            if k == ord('s') and mode != 'ERASE':
                if showMask:
                    showMask = False
                    print("mask invisible")
                else:
                    showMask = True
                    print("mask visible")

            if k == 27:
                cv2.destroyAllWindows()
                if Image.shape[0] > mainShowArea*roiNum + cover:
                    Image[mainShowArea*(roiNum-1):mainShowArea*roiNum + 1 + cover] = origin
                    Mask[mainShowArea*(roiNum-1):mainShowArea*roiNum + 1 + cover] = mask
                else:
                    Image[mainShowArea*(roiNum-1):] = origin
                    Mask[mainShowArea*(roiNum-1):] = mask
                break
            elif k == 26 or k == ord('u'):
                origin = back.copy()
                img = origin.copy()
                mask = maskBack.copy()
            elif k == ord('q'):
                rad = 10
                mode = 'RECT'
                return 'q'
            elif k == 114:
                cv2.destroyAllWindows()
                reset = True
                rad = 10
                mode = 'RECT'
                break
            elif k == ord('m') and drawing == False:
                if mode == 'RECT':
                    mode = 'DRAW'
                    print('mode DRAW  rad = '+str(rad)+" color is ",color )
                    # ---- now DRAW mode! ----
                    maskColor = (0,0,255) # DRAW mode default color: RED
                elif mode == 'DRAW':
                    mode = 'MANUAL'
                    print('mode MANUAL  rad = '+str(rad)+" color is ",color)
                    # ---- now MANUAL mode! ----
                    maskColor = (255,0,0) # MANUAL mode default color: BLUE
                elif mode == 'MANUAL':
                    mode = 'RECT'
                    print('mode RECT')
            elif k == ord('e') and drawing == False:
                if mode == 'ERASE':
                    showMask = False
                    mode = modeTmp
                    print('return to ',mode)
                else:
                    showMask = True
                    modeTmp = mode
                    mode = 'ERASE'
                    print('MASK CLEAR MODE')
            elif k == ord('1') and drawing == False and mode != 'RECT':
                maskColor = (0,0,255)
                print('mask color is [RED]: Text on Easy Background')
            elif k == ord('2') and drawing == False and mode != 'RECT':
                maskColor = (0,255,0)
                print('mask color is [GREEN]: Font Text on Hard Background')
            elif k == ord('3') and drawing == False and mode != 'RECT':
                maskColor = (255,0,0)
                print('mask color is [BLUE]: Sound Effect, Handwritten text')
            elif k == 43 and drawing == False and (mode == 'DRAW' or mode == 'MANUAL' or mode == 'ERASE'):
                if rad < 30:
                    rad += 1
                    print('mode DRAW  rad = '+str(rad)+" color is ",color)
            elif k == 45 and drawing == False and (mode == 'DRAW' or mode == 'MANUAL' or mode == 'ERASE'):
                if rad > 1:
                    rad -= 1
                    print('mode DRAW  rad = '+str(rad)+" color is ",color)




        if reset == True:
            main(srcpath,dstpath)
            return -1
        roiNum += 1

    cleanName = dstpath + "_clean.png"
    maskName = dstpath + "_mask.png"

    cv2.imwrite(cleanName,Image)
    cv2.imwrite(maskName,Mask)




if __name__ == "__main__" :
    main(sys.argv[1])
