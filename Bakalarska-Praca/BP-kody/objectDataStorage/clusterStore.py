
'''
# objekt sluzi na ulozenie jedneho zhluku v strukture listu, kde su ulozene vsetky pixely
# patriace do daneho zhluku
'''

class clusterStore:
    def __init__(self, x, y):
        self.array = []
        self.array.append([x, y])


    # prejde cely zoznam aby zistil ci sa v nom nachadza pixel
    def getPixel(self, x, y):
        for i in range(0, len(self.array)):
            if (self.array[i] == [x,y]):
                return True
        return False

    # pprida dalsi pixel
    def addPixel(self, x, y):
        self.array.append([x,y])

    # vrati zoznam pixelov
    def returnPixels(self):
        return self.array

    # vrati pocet pixelov aby sa eliminovali zhluky ktore do zkumania nepatria
    def getAmountOfPixels(self):
        return len(self.array)

    def getLast(self):
        return self.array[-1]

    # najde stred zhluku
    def center_of_cluster(self):
        x = 0
        y = 0

        for i in range(0, len(self.array)):
            x += self.array[i][0]
            y += self.array[i][1]
        x = int( x / len(self.array))
        y = int( y / len(self.array))

        return [x, y]


