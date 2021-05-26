# imports
import cv2
import time
import numpy as np
from controlpointsLib import findAxesFile
import controlpointsLib.controlPoints as cp
import  objectDataStorage.objectStorage as os
import controlpointsLib.clusteringFile as cf
import controlpointsLib.cpSelector as selector
import detector_seq.resultCalc as resC
from tkinter import *

global rotated_image

'''--------------------------------------------------------------------------------------------------------------'''
'''
# 'hlavna' funkcia ktora riadi chod detekcie a kvantifikacie, zapisuje do vystupneho pola text a udaje z vycislenia
'''

def click(image, tfield, size, search, lang, output_text):

    start = time.time()
    print(f" ## Time started!")

    # skopiruje sa obraz
    rotated_image = np.copy(image)


    print(f">> Rotujem obraz")

    try:
        # spusti sa autorotacia na zaklade vybraneho parametra
        rotated_image = findAxesFile.auto_rotation(rotated_image, search)
    except:
        # v opacnom pripade ak dojde k zlyhaniu, vyhodi program chybovu hlasku
        if lang == 'svk':
            tfield.insert(INSERT, f">> chyba: zlyhanie spracovania obrazu!\n")
            tfield.insert(INSERT, f">> skuste opacny druh prehladavania!\n")
        else:
            tfield.insert(INSERT, f">> error: image processing failed!\n")
            tfield.insert(INSERT, f">> try other variation od searching!\n")
        return image
    '''-------------------------------------------------------------'''

    # pomocne obrazy a objekt kde sa uskladnia riadiace body
    lane2_image = np.copy(rotated_image)
    gray = cv2.cvtColor(lane2_image, cv2.COLOR_RGB2GRAY)
    blur = cv2.GaussianBlur(gray, (7,7),0)
    obj = os.ObjectStore()

    print(f">> Detekujem lebku")

    try:
        # vyberie sa obalst lebky z blur obrazu
        res = findAxesFile.select_skull(blur, lane2_image, search)
    except:
        if lang == 'svk':
            tfield.insert(INSERT, f">> chyba: zlyhanie spracovania obrazu!\n")
        else:
            tfield.insert(INSERT, f">> error: image processing failed!\n")
        return image



    lane2_image = res[0]
    # obraz sa oseka podla hranicnych bodov
    rotated_image = rotated_image[res[1]:res[2], res[3]:res[4]]
    lane2_image = lane2_image[res[1]:res[2], res[3]:res[4]]
    skull = np.copy(lane2_image)

    '''-------------------------------------------------------------'''

    print(f">> Hladam stred")

    canny = cv2.Canny(lane2_image, 0, 255)
    try:
        # najdenie stredu vycentrovaneho obrazu
        center = findAxesFile.move_to_center(canny)
    except:
        if lang == 'svk':
            tfield.insert(INSERT, f">> chyba: zlyhanie spracovania obrazu!\n")
        else:
            tfield.insert(INSERT, f">> error: image processing failed!\n")
        return image

    # CSF mapa mozgu
    print(f">> Generujem CSF mapu")

    try:
        # vytvori sa CSF mapa ktora sa nasledne spracuje tak aby sme dostali intenzity farieb ako parametre zhlukovania
        csf_image = cp.CSFmap(rotated_image, canny, center)
        gray = cv2.cvtColor(csf_image, cv2.COLOR_RGB2GRAY)
        csf_image = cv2.GaussianBlur(gray, (7, 7), 0)
        color = cf.select_param_color_ventricles(csf_image)
        color_limiter = findAxesFile.color_scheme_comparator(rotated_image, color[0])
    except:
        if lang == 'svk':
            tfield.insert(INSERT, f">> chyba: zlyhanie spracovania obrazu!\n")
        else:
            tfield.insert(INSERT, f">> error: image processing failed!\n")
        return image

    '''-------------------------------------------------------------'''
    print(f">> vygenerovana farba:  {color_limiter}")
    print(f">> najtmavsia farba:  {color[0]}")

    print(f">> Generujem clustre")

    try:
        # potom sa CSF mapa spracuje kde dojde k zhlukovaniu
        list_of_cluster_center = cf.processCSFmap(csf_image, canny, color[0], color_limiter+10, False)
    except:
        if lang == 'svk':
            tfield.insert(INSERT, f">> chyba: zlyhanie spracovania obrazu!\n")
        else:
            tfield.insert(INSERT, f">> error: image processing failed!\n")
        return image



    obj.setCenter(center)

    #spracovanie horneho a dolneho falxu
    print(f">> Detekujem horny a dolny falx")

    try:
        # potom sa vyhladaju riadiace body A a B
        lane2_image = cp.processPoint_A(canny, lane2_image, obj, center)
        lane2_image = cp.processPoint_B(canny, lane2_image, obj, center)
    except:
        if lang == 'svk':
            tfield.insert(INSERT, f">> detekcia zlyhala!\n")
        else:
            tfield.insert(INSERT, f">> detection failed!\n")
        return image
    '''-------------------------------------------------------------'''

    # ak nedojde k ziadnej chybe, z kandidatov na riadiace body C a D sa vyberu najvhodnejsi kandidati

    selector.select_potential_points(skull, list_of_cluster_center, obj)

    # teraz mame urcene (predpokaldame) vsetky riadiace body A,B,C,D

    # v ppripade ze A alebo B nie su urcene, nemozme dalej pokracovat a ukoncime program
    if obj.getPointA() == 0 and obj.getPointB() == 0:
        if lang == 'svk':
            tfield.insert(INSERT, f">> CHYBA: riadiace body sa nenasli!")
        else:
            tfield.insert(INSERT, f">> ERROR: no control points founded!")
        return image



    # ak A a B mame urcene, vykreslime IML
    rotated_image = cp.linefullIML(obj, rotated_image)  # vykreslenie midliny
    # a taktiez DML
    rotated_image = cp.linefullDML(obj, rotated_image)


    rotated_image = cp.pointDraw(obj.getPointA()[0], obj.getPointA()[1], rotated_image)  # vykreslenie bodu A do obrazka
    rotated_image = cp.pointDraw(obj.getPointB()[0], obj.getPointB()[1], rotated_image)  # vykreslenie bodu B do obrazka


    '''--------------------------------------------------------------------------------------------------------------'''

    side_defl = resC.calc_side_defl(obj)
    print(f">> side_defl: {side_defl}")

    px_size = abs(res[3] - res[4])
    px_shift = resC.calc_deflection(obj)
    # na zaklade sirky lebky, krajnych bodov sa vycisli max posun v milimetroch
    mm_shift = float(float(px_shift) / float(px_size) * float(size))
    print(f">> px_size: {px_size}")
    print(f">> px_shift: {px_shift}")
    print(f">> mm_shift: {mm_shift}")

    # plocha
    dml_better = False
    try:
        percentage = resC.calc_area(skull, rotated_image, obj, side_defl)
        # ak sa stane to, zeby pomer LH a PH vysiel lepsi pri DML, je to vypisane do textoveho pola
        if float(percentage[4]) < float(percentage[3]):
            dml_better = True
    except:
        if lang == 'svk':
            tfield.insert(INSERT, f">> vypocet velkosti plochy zlyhal!\n")
        else:
            tfield.insert(INSERT, f">> area ratio calculation failed!\n")

    # ak sa nenajde ani bod C ani bod D tak sa to ukonci tu
    if obj.getPointC() == [0, 0, 0, 0] and obj.getPointD() == [0, 0, 0, 0]:
        if lang == 'svk':
            tfield.insert(INSERT, f">> detekcia zlyhala!\n")
        else:
            tfield.insert(INSERT, f">> detection failed!\n")
    else:
        try:
            if lang == 'svk':
                tfield.insert(INSERT, f">> maximalna odchylka:  %.2f " % (mm_shift))
            else:
                tfield.insert(INSERT, f">> maximum deflection:  %.2f " % (mm_shift))
            tfield.insert(INSERT, f"mm\n")
            output_text += "shift:  %.2f " % (mm_shift) + "mm\n"
        except:
            if lang == 'svk':
                tfield.insert(INSERT, f">> maximalnu odchylku nemozno vypocitat!\n")
            else:
                tfield.insert(INSERT, f">> maximum deflection unable unable to calculate!\n")
            output_text += "shift:  NF \n"

        if dml_better == True:
            if lang == 'svk':
                tfield.insert(INSERT, f">> vyhodnotenie pomeru : DML je lepsie ako IML\n")
            else:
                tfield.insert(INSERT, f">> ratio comaparsion: DML better then IML\n")
            output_text += "ratio result better \n"
        tfield.pack()


    try:
        if percentage[0] != 0:
            if lang == 'svk':
                tfield.insert(INSERT, f">> percentualna odchylka:  %.2f " % (percentage[0]))
            else:
                tfield.insert(INSERT, f">> percentual deflection:  %.2f " % (percentage[0]))
            tfield.insert(INSERT, f"%\n")
            tfield.pack()
            output_text += "defl_percentage:  %.2f " % (percentage[0]) + "%\n"

        tfield.insert(INSERT, f">> IPS (R:L): {percentage[1]}\n")
        tfield.insert(INSERT, f">> DPS (R:L): {percentage[2]}\n")
        tfield.pack()
        output_text += "IAR:  " + percentage[1] + "\n"
        output_text += "DAR:  " + percentage[2] + "\n"
    except:
        if lang == 'svk':
            tfield.insert(INSERT, f">> percentualnu odchylku nemozno vypocitat\n")
        else:
            tfield.insert(INSERT, f">> percentual deflection unable to calculate!\n")
        tfield.pack()
        output_text += "defl_percentage: NF\n"

    if mm_shift:
        tfield.insert(INSERT, f"________________________________________\n")
        if mm_shift < 5:
            tfield.insert(INSERT, f">> shift <5mm OK\n")
        elif mm_shift < 10:
            if lang == 'svk':
                tfield.insert(INSERT, f">> shift >5mm !! VYSTRAHA !!\n")
            else:
                tfield.insert(INSERT, f">> shift >5mm !! ALERT !!\n")
        elif mm_shift < 15:
            if lang == 'svk':
                tfield.insert(INSERT, f">> shift >10mm !! VYSTRAHA !!\n")
            else:
                tfield.insert(INSERT, f">> shift >10mm !! ALERT !!\n")
        elif mm_shift >= 15:
            if lang == 'svk':
                tfield.insert(INSERT, f">> shift >15mm !! VYSTRAHA !!\n")
            else:
                tfield.insert(INSERT, f">> shift >15mm !! ALERT !!\n")
        tfield.insert(INSERT, f"________________________________________\n")


    end = time.time()
    print(f"#Duration time: %.2f sec" % (end - start))
    print(f" ## Time ended!")
    cv2.waitKey(0)


    return rotated_image, mm_shift, output_text

