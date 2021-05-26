import cv2
import numpy as np
import math
import controlpointsLib.clusteringFile as cf



#----------------------------------------------------------------#
'''
# funkcia ktora ma vybrat z obrazu cast lebky
# dva sposoby:
                1. princip vyberu na zaklade susedov
                2. vyber na zakalde najvacsieho zhluku
'''
def select_skull(blur, lane2_image, search):
    l = np.copy(lane2_image)
    #cv2.imshow("lane2_image", lane2_image)
    reserve = 2
    most_up = 0
    most_down = 0
    most_left = blur.shape[1]
    most_right = 0

    err = search
    try:
        # prehlada kazdy pixel a ak ma vo svojom okruhu viac ako 6 pixelov rovnakej intenzity,
        # tak ho preklopi do dalsieho pomocneho obrazu
        for x in range(0, blur.shape[0] - reserve):
            for y in range(0, blur.shape[1] - reserve):
                count = 0
                lane2_image[x, y] = 0
                # if blur[x, y] == [  0, 111,   0]:
                if blur[x, y] > 250:
                    for m in range (x-1, x+reserve):
                        for n in range (y-1, y+reserve):
                            if blur[m, n] >= 230:
                                count += 1
                if count >= 7:
                    lane2_image[x, y] = (255, 255, 255)
                    if most_up == 0:
                        most_up = x
                    most_down = x
                    if most_left > y:
                        most_left = y
                    if most_right < y:
                        most_right = y
    except:
        err += 1

    color_image = lane2_image
    #-------------------------------------------------
    if (err == 1):
        try:
            # v druhom pripade zavola funkciu na zhlukovanie, da jej parametre
            # na zaklade ktorych tu lebku vyberie
            gray = cv2.cvtColor(l, cv2.COLOR_RGB2GRAY)
            blur = cv2.GaussianBlur(gray, (7, 7), 0)
            canny = cv2.Canny(blur, 0, 255)

            list_of_clusters = cf.processCSFmap(blur, canny, 240, 256, True)

            color_image = np.zeros([lane2_image.shape[1], lane2_image.shape[0], 3], dtype=np.uint8)
            color_image.fill(0)  # or img[:] = 255

            for obj in list_of_clusters[1]:
                if obj.getAmountOfPixels() > 400:
                    list = obj.returnPixels()
                    for i in list:
                        color_image[i[1], i[0]] = (255, 255, 255)
        except:
            err += 1


    if err == 2:
        print("ERR: Unable to select skull!")
        quit()

    '''if most_up > 10:
        most_up -= 10
    if most_left > 10:
        most_left -= 10
    if most_down+10 < color_image.shape[0]:
        most_down += 10
    if most_right+10 < color_image.shape[1]:
        most_right += 10'''

    # + vrati aj extremne body, na zkalade ktorych potom ostriha obraz
    return [color_image, most_up, most_down, most_left, most_right]
#----------------------------------------------------------------#
'''
# funkcia ktora najde stred lebky

'''
def move_to_center(canny):
    windowWidth = canny.shape[1]
    windowHeight = canny.shape[0]
    leftCoord = 0
    rightCoord = windowWidth
    upCoord = 0
    downCoord = windowHeight

    # ----------------------------- for width
    # prechadzaj dolava a doprava a meraj vzdialenost, potom sa posun do jej stredu
    for x in range(windowWidth // 2, 0, -1):
        if canny[windowHeight // 2, x] > 250:
            leftCoord = x
            break

    for x in range(windowWidth // 2, canny.shape[1], 1):
        if canny[windowHeight // 2, x] > 250:
            rightCoord = x
            break

    distanceM = rightCoord - leftCoord
    x_center = distanceM//2 + leftCoord

    # ----------------------------- for height
    # pto iste pre vysku, meraj vzdialenost a posun sa do stredu
    for y in range(windowHeight // 2, 0, -1):
        if canny[y, x_center] > 250:
            upCoord = y
            break

    for y in range(windowHeight // 2, windowWidth, 1):
        if canny[y, x_center] > 250:
            downCoord = y
            break
    distanceM = downCoord - upCoord
    y_center = distanceM // 2 + upCoord


    return [x_center,y_center, upCoord, downCoord]

#----------------------------------------------------------------#
'''
# pomocna funkcia pre funkciu vyberu lebky, kde su parametrami odovzdane 
# suradnice a ona skontrolujeci spolu susedia... vracia boolean

'''
def is_neighbour(primaryCoord, x, y):
    result = False

    y_p = primaryCoord[0]
    x_p = primaryCoord[1]

    #print(f"Compare coordinate actual {[x, y]} with primary {[x_p, y_p]}")

    if abs(x-x_p) <= 7 and  abs(x-x_p) >= 0 and abs(y-y_p) <= 7 and  abs(y-y_p) >= 0:
        result = True
    return result

#----------------------------------------------------------------#
'''
# funkcia ktora pocita vzdialenost pytagorovou vetou medzi dvoma bodmi

'''
def calc_distance(x, y, center):
    x_dist = abs(center[0] - x)
    y_dist = abs(center[1] - y)
    return (math.sqrt(x_dist**2  + y_dist**2))

#----------------------------------------------------------------#
'''
# pomocna funkcia ktora zrotuje obraz na zaklade uhla ktory je vypocitany vo funkcii autorotacie

'''
def rotate_image(image, angle):
  image_center = tuple(np.array(image.shape[1::-1]) / 2)
  rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
  result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
  return result

#----------------------------------------------------------------#
'''
# zlozitejsia funkcia, ktora na zaklade ploch kvadrantov
# v lebke porovnava velkosti a podla toho pocita uhol
# rotuje pomocny obraz a nie vysledny z dovodu degradacie kvality obrazu

'''

def auto_rotation(image, search):
    image_org = np.copy(image)

    ideal = False
    center = [0,0]
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    blur = cv2.GaussianBlur(gray, (7, 7), 0)
    res = select_skull(blur, image, search)
    skull_image = res[0]
    canny = cv2.Canny(skull_image, 0, 255)
    pre_center = [image.shape[0], image.shape[1]]

    # vyhlada stred lebky a prepise stred na stred obrazy canny
    while pre_center != center:
        pre_center = center
        center = move_to_center(canny)

    angle = 0
    i = 0


    # vyzera nebezpecne ale k zacykleniu nedojde
    while ideal == False:

        size = (int)((canny.shape[0] * canny.shape[1])/1000)

        distance_left = 0
        distance_right = 0
        # vyrataj velkost ploch laveho horneho a praveho horneho kvadrantu
        for y in range(center[1], 0, -20):
            pre_center[1] = y
            if canny[y, center[0]] > 240 or center[2] > y:
                break
            for x in range(center[0], 0, -1):
                if canny[y, x] > 240:
                    distance_left += calc_distance(x, y, pre_center)
                    break

            for x in range(center[0], canny.shape[1]-1, 1):
                if canny[y, x] > 240:
                    distance_right += calc_distance(x, y, pre_center)
                    break

        # porovnaj s tym ze ich velkosti musia byt  +- 10%
        if abs(distance_right - distance_left)/size < 0.10:
            ideal = True
        else:
            if distance_left > distance_right:
                skull_image = rotate_image(skull_image, -1)
                angle -= 1
            else:
                skull_image = rotate_image(skull_image, 1)
                angle += 1

        canny = cv2.Canny(skull_image, 0, 255)
        pre_center = [image.shape[0], image.shape[1]]

        # opat nakalibruj stred lebky
        while pre_center != center:
            pre_center = center
            center = move_to_center(canny)

        i += 1

    image_org = rotate_image(image_org, angle)
    return image_org
#----------------------------------------------------------#
'''
# funkcia ktora ma najst hornu hranicu vyhladavacej intenzity
# neskor pouzitu ako parameter pre hladanie zhlukov

'''
def color_scheme_comparator(image, min_color):
    colors = []
    image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    result = min_color+20

    # prehlada kazdy pixel obrazu a nasledne spracuje
    for y in range(0, image.shape[0]):
        for x in range(0, image.shape[1]):
            if image[y, x] < 3 or 252 < image[y, x]:
                continue
            was_c = False
            # uklada si pocet pixelov v jendotlivych intenzitach
            for c in colors:
                if (image[y, x] == c[0]):
                    was_c = True
                    c[1] +=1
                    break
            if was_c == False:
                colors.append([image[y, x], 1])

    # toto bolo pouzite pre generovanie csv-cka a histogramu
    '''file_write = open('res.csv', 'w')
    for c in colors:
        file_write.write("{};{}\n".format(c[0], c[1]))
        #print(f" c:  {c}")
    file_write.close()'''

    # v intervale 50 az 120 rob to, ze ak je rozdiel hodnot vo vzdialensoti 20 7x vacsi tak pokaldaj to za HH
    for c1 in colors:
        for c2 in colors:
            if c1[0] < 120 and c2[0] < 120 and c1[0] > 50 and c2[0] > 50:
                if c2[0]-20 == c1[0]:
                    if c1[1] < c2[1]:
                        if c1[1]*7 < c2[1]:
                            result = c1[0]
                            return result


    return  result