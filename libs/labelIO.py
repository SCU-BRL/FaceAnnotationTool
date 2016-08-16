import os

# write and read myself face label data

class Writer:
    def __init__(self):
        self.shapes = []

class Reader:
    def __init__(self, labelPath):
        ## shapes type:
        ## [label(default:face), [(x1,y1), (x2,y2), (x3,y3), (x4,y4)], color, color]
        self.shapes = []
        self.labelPath = labelPath

    def loadShapes(self):
        if os.path.exists(self.labelPath) is None:
            print 'label Existence.'
            return
        fp = open(self.labelPath)



print os.path.exists('E:\Multi-Pie\labels')
