import cv2
import numpy as np


'''---------------------------------------------------------------'''
'''
# vypocita do ktorej strany je DML vychylena 
'''
def calc_side_defl(obj):

    most_left = max(obj.getPointA()[0], obj.getPointB()[0])
    most_right = min(obj.getPointA()[0], obj.getPointB()[0])

    if obj.getPointC() != [0, 0, 0, 0]:
        if obj.getPointD() != [0, 0, 0, 0]:
            if obj.getPointC()[0] > most_left and obj.getPointD()[0] > most_left:
                return 'left'
            if obj.getPointC()[0] < most_right and obj.getPointD()[0] < most_right:
                return 'right'
        elif obj.getPointC()[0] > most_left:
            return 'left'
        elif obj.getPointC()[0] < most_right:
            return 'right'
    elif obj.getPointD() != [0, 0, 0, 0]:
        if obj.getPointD()[0] > most_left:
            return 'left'
        elif obj.getPointD()[0] < most_right:
            return 'right'
    return 'unknown'


'''---------------------------------------------------------------'''
'''
# vrati spomedzi bodov C a D ich najvacsiu hodnotu (ako funkcia max)
'''
def calc_deflection(obj):
    if obj.getPointC()[3] > obj.getPointD()[3]:
        return obj.getPointC()[3]
    else:
        return obj.getPointD()[3]

'''---------------------------------------------------------------'''
'''
# tu sa pocita pomer ploch lavej a pravej hemisfery pri IML a DML
'''
def calc_area(skull, rotated_image, obj, side_defl):

    #if side_defl == 'unknown':
    #    return 0
    pointA = obj.getPointA()
    pointB = obj.getPointB()
    color = (0, 203, 127)
    thickness = 1
    skull_with_IML = np.copy(skull)
    skull_with_IML = cv2.line(skull_with_IML, (pointA[0], pointA[1]), (pointB[0], pointB[1]), color, thickness)

    ###################
    total_area_left = 0
    total_area_right = 0
    total_area_ = 0
    shift_area_ = 0
    ###################
    point = obj.getPointA()

    # prechadza po IML smerom dole a prehladava lavu a pravu stranu s
    # tym ze ak narazi na lebku, ukonci pocitanie v danej hladine
    while point != obj.getPointB():

        color_left = skull_with_IML[point[1] + 1, point[0] - 1]
        color_down = skull_with_IML[point[1] + 1, point[0]]
        color_right = skull_with_IML[point[1] + 1, point[0] + 1]

        if (color_down[0] == 0 and color_down[1] == 203 and color_down[2] == 127):
            point = [point[0], point[1] + 1]
        elif (color_left[0] == 0 and color_left[1] == 203 and color_left[2] == 127):
            point = [point[0] - 1, point[1] + 1]
        elif (color_right[0] == 0 and color_right[1] == 203 and color_right[2] == 127):
            point = [point[0] + 1, point[1] + 1]

        was_ = False
        for x in range(point[0], 0, -1):
            color = skull_with_IML[point[1], x]
            if (color[0] > 250 and color[1] > 250 and color[2] > 250):
                break
            color = rotated_image[point[1], x]
            if (color[0] == 254 and color[1] == 1 and color[2] == 1) or ((color[0] == 1 and color[1] == 1 and color[2] == 255)):
                was_ = True
            if side_defl == 'right' and was_ == False:
                shift_area_ += 1
                skull_with_IML[point[1], x] = (0, 255, 255)
            total_area_ += 1
            total_area_right += 1


        was_ = False
        for x in range(point[0], skull_with_IML.shape[1]):
            color = skull_with_IML[point[1], x]
            if (color[0] > 250 and color[1] > 250 and color[2] > 250):
                break
            color = rotated_image[point[1], x]
            if (color[0] == 254 and color[1] == 1 and color[2] == 1) or ((color[0] == 1 and color[1] == 1 and color[2] == 255)):
                was_ = True
            if side_defl == 'left' and was_ == False:
                shift_area_ += 1
                skull_with_IML[point[1], x] = (0, 255, 255)
            total_area_ += 1
            total_area_left += 1

    # END OF WHILE


    print(f">> total_area_right:  {total_area_right}")
    print(f">> total_area_left:  {total_area_left}")
    print(f">> total_area_:  {total_area_}")

    # aktualne mame vypocitanu celu plochu, lavu a pravu plochu pri IML...
    # + velkost plochy medzi IML a DML

    # teraz musime pricitat posunutej ploche tu plochu deformovanu..
    ideal_ratio = str(float("{:.1f}".format(total_area_right / total_area_*100))) + " : " + str(float("{:.1f}".format(total_area_left / total_area_*100)))
    iml_sub_ratio = abs(float("{:.1f}".format(total_area_right / total_area_*100)) - float("{:.1f}".format(total_area_left / total_area_*100)))

    # rozhodne ktora strana je vychylena
    if side_defl == 'left':
        total_area_left = (total_area_left - shift_area_)
        total_area_right = (total_area_right + shift_area_)
    elif side_defl == 'right':
        total_area_left = (total_area_left + shift_area_)
        total_area_right = (total_area_right - shift_area_)
    # a zapise shifted area
    shifted_ratio = str(float("{:.1f}".format(total_area_right / total_area_*100))) + " : " + str(float("{:.1f}".format(total_area_left / total_area_*100)))

    dml_sub_ratio = abs(float("{:.1f}".format(total_area_right / total_area_*100)) - float("{:.1f}".format(total_area_left / total_area_*100)))
    percentuale_shift = float(shift_area_/total_area_*100)

    # vysledkom je posun v %, idealny pomer, pomer pri shifte, a rozdiel pomerov
    return percentuale_shift, ideal_ratio, shifted_ratio, iml_sub_ratio, dml_sub_ratio