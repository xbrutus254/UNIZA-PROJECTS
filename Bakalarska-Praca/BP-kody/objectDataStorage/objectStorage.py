
'''
# objekt v ktorom su ulozene riadiace body, disponuje nim hlavna funkcia click() v runCode a
# vsetky funkcie ktorym objekt priradi hlavna funkcia click()
'''

class ObjectStore:
    def __init__(self):
        self.pointA = 0
        self.pointB = 0
        self.pointC = [0,0,0,0]
        self.pointD = [0,0,0,0]
        self.center = [0,0]


    def getPointA(self):
        return self.pointA

    def getPointB(self):
        return self.pointB

    def getPointC(self):
        return self.pointC

    def getPointD(self):
        return self.pointD

    def getCenter(self):
        return self.center

    #@ObjectStore.setter
    def setPointA(self, pointA):
        self.pointA = pointA

    #@ObjectStore.setter
    def setPointB(self, pointB):
        self.pointB = pointB

    def setPointC(self, pointC):
        self.pointC = pointC

    #@ObjectStore.setter
    def setPointD(self, pointD):
        self.pointD = pointD

    # @ObjectStore.setter
    def setCenter(self, center):
            self.center = center

