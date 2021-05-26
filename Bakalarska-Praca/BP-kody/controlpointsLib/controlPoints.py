import cv2
import numpy as np
from controlpointsLib import findAxesFile as faf

'''
# sada funkcii pre detekciu riadiacich bodov A, B
# kvoli zabraneniu duplicity kodu zdielaju rovnaku funkciu pre hladanie lokalneho minima
'''
##############################################################################################################################
'''
# funkcia spracuje obraz tak aby nasla bod A a zapisala ho do objektu
'''
def processPoint_A(canny, lane2_image, obj, center):

    windowWidth = canny.shape[1]
    windowHeight = canny.shape[0]

    #oznacenie stredu
    # vpodstate to sluzi len na kontrolu
    lane2_image[center[1] - 1, center[0]] = (255, 0, 0)
    lane2_image[center[1], center[0]] = (255, 0, 0)
    lane2_image[center[1] + 1, center[0]] = (255, 0, 0)
    lane2_image[center[1], center[0] - 1] = (255, 0, 0)
    lane2_image[center[1], center[0] + 1] = (255, 0, 0)
    # /oznacenie body

    skip = False
    leftCoord = [0, 0]
    rightCoord = [0, 0]


    # vsetky pomocne premenne
    maxDistLeft = 0
    x_l = 0
    y_l = 0
    maxDistRight = 0
    x_r = 0
    y_r = 0
    startingPosition = int(((center[0] - center[2]) * 0.3) + center[2])
    x_ended_lap = 0
    x_ended_lapR = 0
    y_ended_lap = 0

    # cyklus zacina v startovacej pozicii a pokracuje smerom hore k nulovej suradnici akoby po Y-psilonovej osi
    for y in range(startingPosition, 0, -1):
        # ak dosiahne scan svoj peak
        if canny[y, center[1]] > 240:
            #print(f"End with  {[y, center[1]]}")
            lane2_image = findLocalMin(x_l, y_l, x_r, y_r, x_ended_lap, x_ended_lapR, maxDistLeft, maxDistRight, canny, lane2_image, center, y_ended_lap, obj, -1)
            break
        y_ended_lap = y + 2
        # prehladavaj lavu a pravu stranu s tym ze kontroluj ci najdeny pixel je susedny s predch. najdenym pixelom
        for x in range(center[1], 0, -1):
            if canny[y, x] > 240:
                if y == startingPosition:
                    leftCoord = [y, x]

                elif (faf.is_neighbour(leftCoord, x, y)):
                    leftCoord = [y, x]
                    x_ended_lap = x

                    #oznacenie prejdenych bodov z lava
                    # sluzilo ako pomocny obraz pre kontrolu ci to funguje spravne
                    lane2_image[y, x] = (0, 255, 0)
                    lane2_image[y - 1, x] = (0, 255, 0)


                    #hladanie maxima z lava
                    # pouzi pomocnu funkciu na kalkulaciu vzdialenosti od stredu
                    actualDist = faf.calc_distance(x, y, center)
                    if maxDistLeft < actualDist:
                        maxDistLeft = actualDist
                        # a zapis si suradnice najvzdialenejsieho bodu
                        x_l = x
                        y_l = y
                    # /hladanie maxima z lava
                else:
                    skip = True
                break

        # to iste ale z pravej strany
        for x in range(center[1], windowWidth, 1):

            if canny[y, x] > 240:
                if y == startingPosition:
                    rightCoord = [y, x]

                elif (faf.is_neighbour(rightCoord, x, y)):
                    rightCoord = [y, x]
                    x_ended_lapR = x

                    # oznacenie prejdenych bodov z prava
                    lane2_image[y, x] = (0, 255, 0)
                    lane2_image[y - 1, x] = (0, 255, 0)
                    # /oznacenie prejdenych bodov z prava

                    #hladanie maxima z prava
                    actualDist = faf.calc_distance(x, y, center)
                    if maxDistRight < actualDist:
                        maxDistRight = actualDist
                        x_r = x
                        y_r = y
                    # /hladanie maxima z prava
                else:
                    skip = True
                break
        if skip:
            # s tym ze ak sme dosiahli koniec cyklu alebo bod nesusediaci tak sa zacne prechadzat horizontalne
            lane2_image = findLocalMin(x_l, y_l, x_r, y_r, x_ended_lap, x_ended_lapR, maxDistLeft, maxDistRight, canny, lane2_image, center, y_ended_lap, obj, -1)
            break

    # end of FOR
    return  lane2_image
# end of FUNC

##############################################################################################################################
'''
# funkcia ktora medzi maximami hlada bod najblizsie k stredu.. to zaruci najdenie falxu
'''
def findLocalMin(x_l, y_l, x_r, y_r, x_ended_lap, x_ended_lapR, maxDistLeft, maxDistRight, canny, lane2_image, center, y_ended_lap, obj, direction):
    pointA = [0, 0]
    pointB = [0, 0]

    dest = 0
    if direction == 1:
        dest = canny.shape[0]

    smallestDist = center[0]*4
    x2 = x_ended_lapR

    # prechadza od laveho maxima k pravemu a opat kontroluje susedne pixely tentokrat ale prechadza horizontalne
    for x1 in range(x_ended_lap, x2, 1):
        if x1 >= x2:
            break
        for y in range(y_ended_lap, dest, direction):
            if canny[y, x1] > 240:
                actualDist = faf.calc_distance(x1, y, center)
                if maxDistLeft < actualDist:
                    maxDistLeft = actualDist
                    x_l = x1
                    y_l = y
                # zapisovanie prejdenych pixelov do pomocneho obrazu pre pripadnu kontrolu
                lane2_image[y, x1] = (0, 255, 0)
                lane2_image[y - 1, x1] = (0, 255, 0)
                lane2_image[y - 2, x1] = (0, 255, 0)
                lane2_image[y - 3, x1] = (0, 255, 0)
                break

        for y in range(y_ended_lap, dest, direction):
            if canny[y, x2] > 240:
                actualDist = faf.calc_distance(x2, y, center)
                if maxDistRight < actualDist:
                    maxDistRight = actualDist
                    x_r = x2
                    y_r = y
                lane2_image[y, x2] = (0, 255, 0)
                lane2_image[y - 1, x2] = (0, 255, 0)
                lane2_image[y - 2, x2] = (0, 255, 0)
                lane2_image[y - 3, x2] = (0, 255, 0)
                break
        x2 -= 1

    # az su maxima nadeje, zapise ich do pomocneho obrazu s tym ze ukazu akoby interval kde s abude hladat minimum
    cv2.line(lane2_image, (center[0], center[1]), (x_l, y_l), (36, 255, 12), thickness=1, lineType=8)
    cv2.line(lane2_image, (center[0], center[1]), (x_r, y_r), (36, 255, 12), thickness=1, lineType=8)

    # mame vybrany usek kde hladat stred
    x2 = x_ended_lapR
    dest = 0
    if direction == 1:
        dest = canny.shape[0]

    mean_dist = 0
    count = 1
    max_dist = 0

    # tu sa hlada najmensia vzdialenost co je v celku trivialna uloha... vpdostate to iste ako pri hladani maxim
    # ale najkratsiu vzdialenost
    for x in range(x_l, x_r, 1):
        for y in range(y_ended_lap, dest, direction):

            if canny[y, x] > 240:
                actualDist = faf.calc_distance(x, y, center)
                #
                mean_dist += actualDist
                count += 1
                if max_dist < actualDist:
                    max_dist = actualDist

                if smallestDist >= actualDist:
                    smallestDist = actualDist
                    # podla parametrov sa rozhoduje ci hladame horny alebo dolny falx
                    if direction == -1:
                        pointA = [x, y]
                        obj.setPointA(pointA)
                    if direction == 1:
                        pointB = [x, y]
                        obj.setPointB(pointB)
                break
    if direction == 1:
        if (mean_dist/count)-smallestDist < 3 and abs(pointB[0]-obj.getCenter()[1]) > 20:
            pointB = [obj.getCenter()[0], pointB[1]]
            obj.setPointB(pointB)
    # do pomocneho obrazu sa zakresli vzdialenost od stredu k riadiacemu bodu
    if direction == -1:
        cv2.line(lane2_image, (center[0], center[1]), (pointA[0], pointA[1]), (153, 73, 187), thickness=2, lineType=8)
    else:
        cv2.line(lane2_image, (center[0], center[1]), (pointB[0], pointB[1]), (153, 73, 187), thickness=2, lineType=8)

    #cv2.imshow("resulttttttttt", lane2_image)
    return lane2_image
#end of FUNC

##############################################################################################################################
'''
# uplne to iste ako pri spracovani bodu A, ale z hladiska zbytocneho komplikovania to s parametrami
# a zneprehliadnutia kodu som to rozdelil na osobitne casi pretoze tych parametrov by bolo velmi vela
'''
def processPoint_B(canny, lane2_image, obj, center):

    windowWidth = canny.shape[1]
    windowHeight = canny.shape[0]


    skip = False
    leftCoord = [0, 0]
    rightCoord = [0, 0]


    maxDistLeft = 0
    x_l = 0
    y_l = 0
    maxDistRight = 0
    x_r = 0
    y_r = 0
    # startovacia pozicia sa tu pocita zlozitejsie ale stale je to 70% medzi stredom a hranicou lebky
    startingPosition = int((windowHeight-center[0]-center[2]-(windowHeight - center[3])) * (1-0.3) + (center[0]+center[2]))

    x_ended_lap = 0
    x_ended_lapR = 0
    y_ended_lap = 0

    for y in range(startingPosition, windowHeight, 1):
        # ak dosiahne scan svoj peak
        if canny[y, center[1]] > 240:
            lane2_image = findLocalMin(x_l, y_l, x_r, y_r, x_ended_lap, x_ended_lapR, maxDistLeft, maxDistRight, canny, lane2_image, center, y_ended_lap, obj, 1)
            break
        y_ended_lap = y - 2
        for x in range(center[1], 0, -1):
            if canny[y, x] > 240:
                if y == startingPosition:
                    leftCoord = [y, x]

                elif (faf.is_neighbour(leftCoord, x, y)):
                    leftCoord = [y, x]
                    x_ended_lap = x

                    #oznacenie prejdenych bodov z lava
                    lane2_image[y, x] = (0, 255, 0)
                    lane2_image[y - 1, x] = (0, 255, 0)
                    # /oznacenie prejdenych bodov z lava

                    #hladanie maxima z lava
                    actualDist = faf.calc_distance(x, y, center)
                    if maxDistLeft < actualDist:
                        maxDistLeft = actualDist
                        x_l = x
                        y_l = y
                    # /hladanie maxima z lava
                else:
                    skip = True
                break

        for x in range(center[1], windowWidth, 1):

            if canny[y, x] > 240:
                if y == startingPosition:
                    rightCoord = [y, x]

                elif (faf.is_neighbour(rightCoord, x, y)):
                    rightCoord = [y, x]
                    x_ended_lapR = x

                    # oznacenie prejdenych bodov z prava
                    lane2_image[y, x] = (0, 255, 0)
                    lane2_image[y - 1, x] = (0, 255, 0)
                    # /oznacenie prejdenych bodov z prava

                    #hladanie maxima z prava
                    actualDist = faf.calc_distance(x, y, center)
                    if maxDistRight < actualDist:
                        maxDistRight = actualDist
                        x_r = x
                        y_r = y
                    # /hladanie maxima z prava
                else:
                    skip = True
                break
        if skip:
            lane2_image = findLocalMin(x_l, y_l, x_r, y_r, x_ended_lap, x_ended_lapR, maxDistLeft, maxDistRight, canny, lane2_image, center, y_ended_lap, obj, 1)
            break

    # end of FOR
    return  lane2_image
# end of FUNC

################################################################################
import math
'''
# tato funkcia je pouzita z tejto stranky "https://stackoverflow.com/questions/51908563/dotted-or-dashed-line-with-python-pillow"
# vpodtstate je to usecka medzi bodmi A a B, az hladiska vypoctu zbytocna, ale pekne rozbrazovala prerusovanou ciarou
# tu idealnu usecku... kedze CV2 nema nikde prerusovanu line, treba si ju naprogramovat
'''

def linedashed(obj, img):
    dashlen = 5
    ratio = 4
    x0 = obj.getPointA()[0]
    y0 = obj.getPointA()[1]
    x1 = obj.getPointB()[0]
    y1 = obj.getPointB()[1]
    dx=x1-x0 # delta x
    dy=y1-y0 # delta y
    # check whether we can avoid sqrt
    if dy==0: len=dx
    elif dx==0: len=dy
    else: len=math.sqrt(dx*dx+dy*dy) # length of line
    xa=dx/len # x add for 1px line length
    ya=dy/len # y add for 1px line length
    step=dashlen*ratio # step to the next dash
    a0=0
    while a0<len:
        a1=a0+dashlen
        if a1>len: a1=len
        cv2.line(img, (int(x0+xa*a0), int(y0+ya*a0)), (int(x0+xa*a1), int(y0+ya*a1)), color=(1, 255, 0), thickness=1, lineType=-1)
        a0+=step

    return img

'''
# pomocna funkcia na zakreslenie line-y medzi riadiacimi bodmi A a B
'''
def linefullIML(obj, img):
    start_point = (obj.getPointA()[0], obj.getPointA()[1])
    end_point = (obj.getPointB()[0], obj.getPointB()[1])
    color = (0, 254, 0)
    thickness = 1
    cv2.line(img, start_point, end_point, color, thickness)
    return img

'''
# funkcia ktora zakresli deformovanu line-u medzi riadiacimi bodmi s tym ze kontroluje ci vobec tie body su nastavene
'''
def linefullDML(obj, img):
    start_point = (obj.getPointA()[0], obj.getPointA()[1])
    mid_pointC = (obj.getPointC()[0], obj.getPointC()[1])
    mid_pointD = (obj.getPointD()[0], obj.getPointD()[1])
    end_point = (obj.getPointB()[0], obj.getPointB()[1])
    color = (254, 1, 1)
    thickness = 2
    if (mid_pointC == (0,0) and mid_pointD == (0,0)):
        cv2.line(img, start_point, end_point, color, thickness)
    elif(mid_pointC == (0,0)):
        cv2.line(img, start_point, mid_pointD, color, thickness)
        cv2.line(img, mid_pointD, end_point, color, thickness)
        img = pointDraw(obj.getPointD()[0], obj.getPointD()[1], img)
    elif(mid_pointD == (0,0)):
        cv2.line(img, start_point, mid_pointC, color, thickness)
        cv2.line(img, mid_pointC, end_point, color, thickness)
        img = pointDraw(obj.getPointC()[0], obj.getPointC()[1], img)
    else:
        cv2.line(img, start_point, mid_pointC, color, thickness)
        cv2.line(img, mid_pointC, mid_pointD, color, thickness)
        cv2.line(img, mid_pointD, end_point, color, thickness)
        img = pointDraw(obj.getPointC()[0], obj.getPointC()[1], img)
        img = pointDraw(obj.getPointD()[0], obj.getPointD()[1], img)

    return img


'''
# zakresli bodik do obrazu ako kruzok aby bolo vidno kde sa ten bod nachadza
'''
def pointDraw(x, y, img):
    radius = 3
    cv2.circle(img, (x, y), radius, (1, 1, 255), 3)
    return img


################################################################################
'''
# spracuje vstupny obraz tak, ze prechadza obraz a pokial narazi v canny obraze na lebky tak preklopuje biele pixely
# takto eliminuje vsetky nepodstatne pixely mimo lebky
'''
def CSFmap(image, canny, center):
    csf_image = np.copy(image)
    direction = -1
    step = -1

    # musi to prejst 2x kedze v lebke a konkretne pri falxoch su zahyby ktore by dobabrali obraz..
    for invert in range(2):
        for y in range(center[1], direction, step):
            left_was = False
            right_was = False
            for x in range(center[0], 0, -1):
                if left_was:
                    csf_image[y, x] = (255, 255, 255)
                    continue
                csf_image[y, x] = image[y,x]
                if canny[y, x] > 240:
                    csf_image[y, x] = (255, 255, 255)
                    left_was = True

            for x in range(center[0], canny.shape[1] - 1, 1):
                if right_was:
                    csf_image[y, x] = (255, 255, 255)
                    continue
                csf_image[y, x] = image[y, x]
                if canny[y, x] > 240:
                    csf_image[y, x] = (255, 255, 255)
                    right_was = True

        direction = canny.shape[0]
        step = 1

    return csf_image
################################################################################
