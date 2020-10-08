import cv2
import numpy
import pyautogui
import PIL
from math import ceil
from brains import *
import os

# os.system('mode con: cols=75 lines=35')


def classifyRowCol(coords):
    x, y = coords
    vIntercept, vGradient, vSpacing, vOffset = 360, 1.80645, 118, 65
    hIntercept, hSpacing, hOffset = 15, 58, 38
    row, col = -1, -1
    for i in range(11):
        if y < hIntercept + i * hSpacing + hOffset:
            row = i+1
            break
    for i in range(11):
        if y < ceil((vIntercept + i * vSpacing + vOffset) + (-vGradient * x)):
            col = i+1
            break

    return row, col

if __name__ == '__main__':
    windowpt = pyautogui.locateOnScreen('data/6.png')
    if windowpt is None:
        print('Gold not found!')
    else:
        while True:
            boundaries = (windowpt[0]-345, windowpt[1]-300, windowpt[0]+370, windowpt[1]+325)
            boardImage = numpy.array(PIL.ImageGrab.grab(bbox=boundaries))
            colouredImage = cv2.cvtColor(boardImage, cv2.COLOR_BGR2RGB)
            #boardImage = cv2.cvtColor(boardImage, cv2.COLOR_BGR2RGB)
            #cv2.imshow('boardImage',boardImage)
            #cv2.waitKey(0)
            boardGrey = cv2.cvtColor(boardImage, cv2.COLOR_BGR2GRAY)

            # template = cv2.imread('data/quicksilver.png', 0)
            # template = cv2.imread('data/mors.png', 0)
            # template = cv2.imread('data/vitae.png', 0)
            template = cv2.imread('data/salt.png', 0)
            # template = cv2.imread('data/fire.png', 0)
            templateList = (('data/quicksilver.png',    (96, 96, 96),           'Q'),
                            ('data/quicksilver2.png',   (96, 96, 96),           'Q'),
                            ('data/quicksilver3.png',   (96, 96, 96),           'Q'),
                            ('data/mors.png',           (0, 0, 0),              'M'),
                            ('data/vitae.png',          (255, 255, 255),        'V'),
                            ('data/vitae2.png',         (255, 255, 255),        'V'),
                            ('data/vitae3.png',         (255, 255, 255),        'V'),
                            ('data/salt.png',           (96, 164, 244),         '?'),
                            ('data/salt2.png',          (96, 164, 244),         '?'),
                            ('data/air.png',            (255, 204, 103),        'A'),
                            ('data/air2.png',           (255, 204, 103),        'A'),
                            ('data/air3.png',           (255, 204, 103),        'A'),
                            ('data/air4.png',           (255, 204, 103),        'A'),
                            ('data/air5.png',           (255, 204, 103),        'A'),
                            ('data/air6.png',           (255, 204, 103),        'A'),
                            ('data/air7.png',           (255, 204, 103),        'A'),
                            ('data/air8.png',           (255, 204, 103),        'A'),
                            ('data/air9.png',           (255, 204, 103),        'A'),
                            ('data/fire.png',           (0, 0, 255),            'B'),
                            ('data/fire2.png',          (0, 0, 255),            'B'),
                            ('data/fire3.png',          (0, 0, 255),            'B'),
                            ('data/water.png',          (255, 0, 0),            'C'),
                            ('data/water2.png',         (255, 0, 0),            'C'),
                            ('data/water3.png',         (255, 0, 0),            'C'),
                            ('data/water4.png',         (255, 0, 0),            'C'),
                            ('data/earth.png',          (0, 255, 0),            'D'),
                            ('data/earth2.png',         (0, 255, 0),            'D'),
                            ('data/earth3.png',         (0, 255, 0),            'D'),
                            ('data/1.png',              (51, 0, 102),           1),
                            ('data/2.png',              (51, 0, 102),           2),
                            ('data/3.png',              (51, 0, 102),           3),
                            ('data/4.png',              (51, 0, 102),           4),
                            ('data/5.png',              (51, 0, 102),           5),
                            ('data/6.png',              (51, 0, 102),           6))

            board = createEmptyBoard()

            for t in templateList:
                template = cv2.imread(t[0], 0)
                w, h = template.shape[::-1]

                res = cv2.matchTemplate(boardGrey, template, cv2.TM_CCOEFF_NORMED)
                threshold = 0.90
                loc = numpy.where(res >= threshold)
                for pt in zip(*loc[::-1]):
                    cv2.rectangle(colouredImage, pt, (pt[0] + w, pt[1] + h), t[1], 2)
                    # print(str(t[2]) + ' found at position ' + str(classifyRowCol(pt)))
                    #print(pt)
                    updateBoard(board, t[2], classifyRowCol(pt))

            vIntercept, vGradient, vSpacing, vOffset = 360, 1.80645, 118, 65
            hIntercept, hSpacing, hOffset = 15, 58, 38
            # for i in range(11):
            #     cv2.line(colouredImage, (0, vIntercept + i * vSpacing + vOffset),
            #              (ceil((vIntercept + i * vSpacing + vOffset) / vGradient), 0),
            #              (0, 0, 0), 2)
            #     cv2.line(colouredImage, (0, hIntercept + hSpacing * i + hOffset),
            #              (1000, hIntercept + hSpacing * i + hOffset),
            #              (0, 0, 0), 2)
            #
            # for i in range(11):
            #     cv2.line(colouredImage, (0, vIntercept + i * vSpacing),
            #              (ceil((vIntercept + i * vSpacing) / vGradient), 0),
            #              (203, 192, 255), 2)
            #     cv2.line(colouredImage, (0, hIntercept + hSpacing * i),
            #              (1000, hIntercept + hSpacing * i),
            #              (203, 192, 255), 2)

            # cv2.imshow('Atom locations', colouredImage)
            # cv2.waitKey(0)
                # printBoard(board)
            pyautogui.PAUSE = 0.05
            if validBoard(board):
                print('Valid solution, attempting solve...')
                solution = solve(initState(board), 0)[0]
                if solution:
                    pyautogui.PAUSE = 0.025
                    pyautogui.moveTo(x=windowpt[0], y=windowpt[1])
                    pyautogui.click(x = windowpt[0], y= windowpt[1])
                    for solutionPair in solution:
                        pyautogui.moveTo(x = windowpt[0] - 345 + ceil(((hIntercept + (solutionPair[0][0]-1) * hSpacing) - vIntercept - (solutionPair[0][1]-1)*vSpacing)/-vGradient),
                                         y = windowpt[1] - 300 + hIntercept + (solutionPair[0][0]-1) * hSpacing)
                        pyautogui.mouseDown()
                        pyautogui.mouseUp()
                        pyautogui.moveTo(x = windowpt[0] - 345 + ceil(((hIntercept + (solutionPair[1][0]-1) * hSpacing) - vIntercept - (solutionPair[1][1]-1)*vSpacing)/-vGradient),
                                         y = windowpt[1] - 300 + hIntercept + (solutionPair[1][0]-1) * hSpacing)
                        pyautogui.mouseDown()
                        pyautogui.mouseUp()
            print('Invalid board! Creating new board')
            pyautogui.moveTo(x = windowpt[0] - 300, y = windowpt[1] + 400)
            pyautogui.mouseDown()
            pyautogui.PAUSE = 5
            pyautogui.mouseUp()


        # colourBounds = (('fireVisible', numpy.array([110, 50, 50]), numpy.array([130, 255, 255])),
        #                 ('???', numpy.array([30, 40, 67]), numpy.array([32, 45, 75])),
        #                 ('waterVisible', numpy.array([20, 50, 50]), numpy.array([35, 255, 255])),
        #                 ('blue', numpy.array([110, 80, 40]), numpy.array([102, 255, 255])))
        # hsvImage = cv2.cvtColor(boardImage, cv2.COLOR_BGR2HSV)
        # i=1

        # mask = cv2.inRange(hsvImage, colourBounds[i][1], colourBounds[i][2])
        # cv2.imshow('mask', mask)
        # cv2.waitKey(0)
