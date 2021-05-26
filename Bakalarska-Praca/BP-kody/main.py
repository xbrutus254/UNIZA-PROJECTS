# imports
import cv2
import tkinter
from tkinter import *
from tkinter import PhotoImage
import PIL.Image, PIL.ImageTk
import PIL
import detector_seq.runCode as rc
from tkinter import filedialog as fd


#----------------------------------------------------------------
ja = 0
jb = 0
size = 150
searching = 0
language = 'svk'
'''----------------------------------------------------------------------------------'''
'''
# tato funkcia spracuje nacitany obraz podla zadanych paramterov
    ktore si uzivatel naklikal s tym ze vypise vysledky do platna
    a vrati vysledny obraz s deformovanou krivkou 

'''
def call_seq():
    global tfield
    global img
    global mm_shift
    global searching
    global path
    global output_text
    output_text = "path: " + str(path) + "\n"
    print(f">> searching: {searching}")
    res = rc.click(image, tfield, size, searching, language, output_text)
    img = res[0]
    mm_shift = res[1]

    output_text = res[2]

    scale = float(450 / img.shape[0])
    width = int(img.shape[1] * scale)
    global disp_image
    disp_image = cv2.resize(img, (width, 450))
    global photo
    photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(disp_image))
    canvas1.create_image(12, 12, image=photo, anchor=tkinter.NW)
'''----------------------------------------------------------------------------------'''
'''
# funkcia ulozi vysledky posunu do suboru aj s nazvom obrazu

'''

def saveData():
    global output_text
    file_write = open('res.txt', 'a')
    file_write.write("{}\n".format(output_text))
    file_write.close()
'''----------------------------------------------------------------------------------'''
'''
# tato funkcia ulozi vysledny obraz s deformovanou krivkou do suboru

'''
def saveImage():
    try:
        global disp_image
        global path

        w = path.split("/")
        path = ""
        for wrd in w:
            if wrd != w[-1] and wrd != w[-2]:
                path = path + wrd + "/"
        path += "results/" + w[-1].split(".")[0] + "RESULT.png"
        '''#########################'''
        print(f"path: {path}")

        topLeftCornerOfText = (3, 20)
        font = cv2.FONT_HERSHEY_PLAIN
        fontScale = 1
        fontColor = (1, 255, 1)
        lineType = 1
        try:
            global mm_shift
            shft = 'SHFT %.2f mm' % (mm_shift)

            cv2.putText(disp_image, shft,
                        topLeftCornerOfText,
                        font,
                        fontScale,
                        fontColor,
                        lineType)
            cv2.imwrite(path, disp_image)
            '''#########################'''
        except:
            tfield.insert(INSERT, f">> shift = NF\n")
            tfield.pack()
    except:
        tfield.insert(INSERT, f">> path = NF\n")
        tfield.pack()
'''----------------------------------------------------------------------------------'''
'''
# funkcia ktora ponukne uzivatelovi nastavit sirku leby v milimetroch pre spravne
    vycislenie posunu

'''
def setSizeSkull():

    def submit():
        global size
        size = T.get("1.0", "end-1c")
        print(size)
        filewin.destroy()

    filewin = Toplevel(window, bg='cyan')
    filewin.title("MLS. size")
    T = Text(filewin, height = 2, width = 25)
    global language
    if language == 'svk':
        l = tkinter.Label(filewin, text="Vloz sirku lebky (mm) :", bg='cyan')
    else:
        l = tkinter.Label(filewin, text="Set size of skull (mm):", bg='cyan')
    l.config(font=("Courier", 14))
    b1 = tkinter.Button(filewin, text="OK", command=submit, bg='orange')
    l.pack()
    T.pack()
    b1.pack()
'''----------------------------------------------------------------------------------'''
'''
# funkcia ktora ma za ulohu prepnut sposob vyhladavania pomocou platna
    kde si uzivatel vyberie sposob prehladavania

'''
def deepSearch():
    def change_val_quick():
        global searching
        searching = 0
        filewin.destroy()

    def change_val_deep():
        global searching
        searching = 1
        filewin.destroy()


    filewin = Toplevel(window)
    filewin.title("MLS. deep search")
    filewin.geometry("200x80")

    global searching
    if(searching == 0):
        is_on_1 = 0
        is_on_2 = 1
    else:
        is_on_1 = 1
        is_on_2 = 0

    var = IntVar()
    R1 = tkinter.Radiobutton(filewin, text="Quick Founder", variable=var, value=is_on_1, command=change_val_quick, bg='cyan')
    R1.pack(anchor=W)

    R2 = tkinter.Radiobutton(filewin, text="Deep Founder (takes long time)", variable=var, value=is_on_2, command=change_val_deep, bg='cyan')
    R2.pack(anchor=W)
'''----------------------------------------------------------------------------------'''
'''
# funkcia ktora zobrazí menu s informaciami o pouzivani aplikacie

'''
def infoCanvas():

    infoC = Toplevel(window, bg='cyan')
    infoC.title("how to..")
    infoC.geometry("500x400")

    global language
    if language == 'svk':
        label = tkinter.Label(infoC, text = "\n\n\n1. File -> Open - otvorte obraz ktory chcete spracovat\n"
                                    "\n2. File -> Set skull size - nastavte sirku lebky [mm] (inac bude nastavena na 15mm)\n"
                                    "\n3. Stlacte tlacidlo PROCESS - spracovanie trva niekolko sekund\n"
                                    "\n4. Do textoveho pola sa vypisu informacie o posune\n"
                                    "\n5. Spracovane udaje mozno ulozit cez File->Save data\n"
                                    "\n6. Taktiez je mozne ulozit vysledny obraz cez File->Save image\n"
                                    "\n7. V pripade ze je detekcia nepresna alebo neucinna, je mozne skusit"
                                    "\n   to este raz s File->DeepSearching->Deep Founder", bg='cyan')
    else:
        label = tkinter.Label(infoC, text="\n\n\n1. File -> Open - open the image you want to process\n"
                                      "\n2. File -> Set skull size - set skull size [mm] (otherwise it will be set to 15mm)\n"
                                      "\n3. Press the PROCESS button - processing takes a few seconds\n"
                                      "\n4. The shift information is displayed in the text field\n"
                                      "\n5. Processed data can be saved via File-> Save data\n"
                                      "\n6. It is also possible to save the resulting image via File-> Save image\n"
                                      "\n7. If the detection is inaccurate or ineffective, it is possible to try"
                                      "\n   it again with File-> DeepSearching-> Deep Founder", bg='cyan')
    label.pack()
'''----------------------------------------------------------------------------------'''
'''
# funkcia ktora zobrazi platno s informaciami o autorovi

'''
def author():
    infoC = Toplevel(window, bg='cyan')
    infoC.title("autor..")
    infoC.geometry("300x180")

    global language
    if language == 'svk':
        label = tkinter.Label(infoC, text="\n\n\n1. Autor: Drab Jozef - ccc7.com@gmail.com\n"
                                          "\n2. Bakalarska praca - FRI UNIZA 2021\n"
                                          "\n3. V spolupraci so Siemens Healthineers AG", bg='cyan')
    else:
        label = tkinter.Label(infoC, text="\n\n\n>> Autor: Drab Jozef - ccc7.com@gmail.com\n"
                                          "\n>> Bachelor thesis - FRI UNIZA 2021\n"
                                          "\n>> In cooperation with Siemens Healthineers AG", bg='cyan')
    label.pack()

'''----------------------------------------------------------------------------------'''
'''
# funkcia ktora zobrazi nove paltno pre vyber jazyka z ponuk slovensky/anglicky

'''
def setLanguage():
    def change_val_svk():
        global language
        language = 'svk'
        #filewin.destroy()

    def change_val_eng():
        global language
        language = 'eng'
        #filewin.destroy()


    filewin = Toplevel(window, bg='cyan')
    filewin.title("MLS. language")
    filewin.geometry("200x80")


    global language
    if(language == 'eng'):
        is_on_1 = 0
        is_on_2 = 1
    else:
        is_on_1 = 1
        is_on_2 = 0

    var = IntVar()
    print(f"lang: {language}")
    print(f"is_on_1: {is_on_1}")
    print(f"is_on_2: {is_on_2}")
    R1 = tkinter.Radiobutton(filewin, text="slovensky", variable=var, value=is_on_1, command=change_val_svk, bg='cyan')
    R1.pack(anchor=W)

    R2 = tkinter.Radiobutton(filewin, text="english", variable=var, value=is_on_2, command=change_val_eng, bg='cyan')
    R2.pack(anchor=W)


'''----------------------------------------------------------------------------------'''
'''
# funkcia ktora vyberie obraz, zmeni size a ulozi do 
  globalnej premennej pre zobrazenie do platna

'''
def selectImage():
    tfield.delete('1.0', END)
    global path
    path = fd.askopenfilename()

    global image
    img = cv2.imread(path)  # perfect (shifted)
    image = cv2.imread(path)
    scale = float(450 / img.shape[0])
    width = int(img.shape[1] * scale)

    disp_image = cv2.resize(img, (width, 450))
    global photo
    photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(disp_image))
    canvas1.create_image(12, 12, image=photo, anchor=tkinter.NW)

'''###############################################################################'''
'''
# graficke platno, obsahujuce obraz, vypis a menubar

'''
global image
image = cv2.imread('C:/Users/ccc7c/PycharmProjects/detect/queryImage/noimg.png') # perfect (shifted)
scale = float(450/image.shape[0])
width = int(image.shape[1]*scale)
global disp_image
disp_image = cv2.resize(image, (width, 450))


window = tkinter.Tk()
window.title("Midline shift Detector")
window.geometry("750x500")
p1 = PhotoImage(file = 'C:/Users/ccc7c/PycharmProjects/detect/queryImage/logo.png')
window.iconphoto(False, p1)


canvas1 = tkinter.Canvas(window, bg='black', width=400, height=500)
canvas1.pack(side="left", fill="both", expand=True)

canvas2 = tkinter.Canvas(window, bg='black', width=150, height=500)
canvas2.pack(side="right", fill="both", expand=False)


# Use PIL (Pillow) to convert the NumPy ndarray to a PhotoImage
photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(disp_image))
canvas1.create_image(12, 12, image=photo, anchor=tkinter.NW)


img_btn = PhotoImage(file = r"queryImage/procc.png")
btn_blur = tkinter.Button(canvas2, bd=0, image=img_btn, width=147, height=73, command=call_seq)
btn_blur.place(x=0, y=0)
btn_blur.pack(anchor=tkinter.CENTER, expand=False)



menubar = Menu(window)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Open..", command=selectImage)
filemenu.add_command(label="Set skull size", command=setSizeSkull)
filemenu.add_command(label="Deep searching", command=deepSearch)
filemenu.add_command(label="Save image", command=saveImage)
filemenu.add_command(label="Save data", command=saveData)
filemenu.add_command(label="Set language", command=setLanguage)

filemenu.add_separator()

filemenu.add_command(label="Exit", command=window.quit)
menubar.add_cascade(label="File", menu=filemenu)

helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="Help", command=infoCanvas)
helpmenu.add_command(label="About...", command=author)
menubar.add_cascade(label="Help", menu=helpmenu)

window.config(menu=menubar)


global tfield
tfield = tkinter.Text(canvas2)
tfield.place(x=10, y=20, height=240, width=150)
tfield.pack()

window.mainloop()


#######################################################################################################




