import numpy as np
import  objectDataStorage.clusterStore as cs

'''-----------------------------------------------------------------------------------------'''
'''
# spracuje CSF mapu s tym ze spusta metodu zhlukovania, vrati zoznam stredov zhlukov + vsetky zhluky
'''
def processCSFmap(csf_image, canny, index_min, index_max, is_white):
    print('-|', end='')

    color_image = np.stack((canny,)*3, axis=-1)
    c_check_image = np.copy(color_image)
    list_pixel_processed = []
    clusters = []
    clusters.append(cs.clusterStore(0, 0))

    # prechadza vsetky pixely v obraze
    for x in range(1, csf_image.shape[1] - 2):
        for y in range(1, csf_image.shape[0] - 2):
            # podla zadaneho parametra sa pyta ci je pixel bielej intenzity
            if (pixelWhite(csf_image, x, y) == is_white):
                # a ci pixel patri do intenzity intervalu ktory bol prideleny funkcii v parametroch
                if index_min < csf_image[y, x] and csf_image[y, x] < index_max:
                    # nasledne sa spusti metoda zhlukovania ktora je popisana nizsie
                    res = clustering(x, y, csf_image, c_check_image, list_pixel_processed, clusters, index_min, index_max)

                    list_pixel_processed = res[1]
                    clusters = res[2]

    limiter = canny.shape[0] * canny.shape[1]
    limiter *= 0.0025
    list_of_cluster_center = []
    color_image = np.stack((canny,) * 3, axis=-1)
    # tu sa vsetky zhluky prepisu do noveho zoznamu s velkostnym kriteriom zhluku
    for obj in clusters:
        if obj.getAmountOfPixels() > 1:
            l = obj.returnPixels()

            for item in l:
                color_image[item[1], item[0]] = (210, 0, 0)
            [x, y] = obj.center_of_cluster()
            list_of_cluster_center.append([x, y])

            # toto sluzi na zakreslenie do pomocneho obrazu v kt. sa kontroluju zhluky
            for j in range(x - 2, x + 3):
                for i in range(y - 2, y + 3):
                    color_image[i, j] = (254, 254, 0)


    print('|-')
    #cv2.imshow("csf_img", color_image)  #<<<<<<<<<<<

    return list_of_cluster_center, clusters


'''-----------------------------------------------------------------------------------------'''
'''
# trivialna funkcia ktora vracia boolean ci je pixel biely
'''
def pixelWhite(img, x, y):
    if img[y, x] > 250:
        return True
    else:
        return False

'''-----------------------------------------------------------------------------------------'''
'''
# skontroluje sa ci je pixel uz spracovany zhlukovanim a ak nie, znamena to ze sa nasiel novy zhluk
'''
def clustering(x, y, csf_image, c_check_image, lpp, clusters, index_min, index_max):
    is_clustered = False

    for item in lpp:
        if item == [x, y]:
            is_clustered = True
            break

    if is_clustered == False:
        print('|', end='')
        # priradi sa mu novy cluster
        clusters.append(cs.clusterStore(x, y))
        # a spusti prehladavanie susednych pixelov
        res = cluster_help_func(csf_image, c_check_image, x, y, clusters, index_min, index_max)
        clusters = res[0]
        lpp = lpp + res[1]
        c_check_image = res[2]

    return c_check_image, lpp, clusters

'''-----------------------------------------------------------------------------------------'''
'''
# prehladavanie pixelov funguje tak, ze prejde kazdeho suseda, pyta sa ci je spracovany a prideluje do 
# pomocneho obrazu (nie do listu z hladiska optimalizacie) 
# konci ked sa aktualny spracuvavany pixel nachadza na konci zoznamu zhluku, cize uz nie je ziaden dalsi na spracovanie
'''
def cluster_help_func(csf_image, c_check_image, x, y, cluster, index_min, index_max):

    list_used_pixels = []
    clust = cluster[len(cluster)-1]
    iterator = 0

    # nezacykli sa
    while True:

        # prehladavaj susedne pixely
        for j in range(x - 2, x + 3):
            for i in range(y - 2, y + 3):
                try:
                    # ak sa nachadza v danej intenzite tak pokracuj
                    if index_min < csf_image[i, j] and csf_image[i, j] < index_max:
                        append = True
                        color = c_check_image[i, j]
                        # ak je pixel spracovany tak nastav prpeinac na false aby sa pixel nezapisal
                        if (color[0] == 230 and color[1] == 170 and color[2] == 0):
                            append = False

                        if append == True:
                            # pridaj do zoznamu pouzitych, pridaj do zhluku a do pomocneho obrazu zaznac
                            c_check_image[i, j] = [230, 170, 0]
                            list_used_pixels.append([j,i])
                            clust.addPixel(j, i)
                except:
                    return cluster, list_used_pixels, c_check_image


        # ak je aktualny pixel posledny buducich spracuvavanych tak ukonc to
        if [x, y] == clust.getLast():
            break
        else:
            # v inaksom pripade bude aktualny pixel dalsi v zozname
            iterator += 1
            x = list_used_pixels[iterator][0]
            y = list_used_pixels[iterator][1]

    # END OF WHILE

    # ak je zhluk mensi ako zadany pocet tak do predbezne zmaz
    if clust.getAmountOfPixels() < 400:
        del cluster[-1]

    return cluster, list_used_pixels, c_check_image

'''-----------------------------------------------------------------------------------------'''
'''
# prehlada CSF obraz a vrati najtmavsi pixel + stredu hodnotu pixelov
'''
def select_param_color_ventricles(csf_image):
    min_color = 255
    mean_color = 0
    i = 0

    for x in range(0, csf_image.shape[1] - 1):
        for y in range(0, csf_image.shape[0] - 1):
            if csf_image[y, x] < min_color:
                min_color = csf_image[y, x]
            if 0 < csf_image[y, x] and csf_image[y, x] < 255:
                mean_color += csf_image[y, x]
                i += 1

    mean_color = (int)(mean_color / i)
    return min_color, mean_color