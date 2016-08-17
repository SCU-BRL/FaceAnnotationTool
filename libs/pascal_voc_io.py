import sys
from xml.etree import ElementTree
from xml.etree.ElementTree import Element, SubElement
from xml.dom import minidom
from lxml import etree

class PascalVocWriter:
    def __init__(self, foldername, filename, imgSize ,databaseSrc='Unknown', localImgPath=None):
        self.foldername = foldername
        self.filename = filename
        self.databaseSrc = databaseSrc
        self.imgSize = imgSize
        self.boxlist = []
        self.localImgPath = localImgPath

    def prettify(self, elem):
        """
            Return a pretty-printed XML string for the Element.
        """
        rough_string = ElementTree.tostring(elem,'utf8')
        reparsed = minidom.parseString(rough_string)
        return reparsed.toprettyxml(indent="\t")

    def genXML(self):
        """
            Return XML root
        """
        # Check conditions
        if self.filename is None or \
                self.foldername is None or \
                self.imgSize is None or \
                len(self.boxlist) <= 0:
                    return None

        top = Element('annotation')
        folder = SubElement(top,'folder')
        folder.text = self.foldername

        filename = SubElement(top,'filename')
        filename.text = self.filename

        localImgPath = SubElement(top,'path')
        localImgPath.text = self.localImgPath

        source = SubElement(top,'source')
        database = SubElement(source,'database')
        database.text = self.databaseSrc

        size_part = SubElement(top,'size')
        width = SubElement(size_part,'width')
        height = SubElement(size_part,'height')
        depth = SubElement(size_part,'depth')
        width.text = str(self.imgSize[1])
        height.text = str(self.imgSize[0])
        if len(self.imgSize)==3:
            depth.text = str(self.imgSize[2])
        else:
            depth.text = '1'

        segmented = SubElement(top,'segmented')
        segmented.text ='0'

        return top

    def addBndBox(self, x, y, width, height, name, pose):
        bndbox = {'x':x, 'y':y, 'width':width, 'height':height}
        bndbox['name'] = name
        bndbox['pose'] = pose
        self.boxlist.append(bndbox)

    def appendObjects(self, top):
        for each_object in self.boxlist:
            object_item = SubElement(top,'object')
            name = SubElement(object_item, 'name')
            name.text = str(each_object['name'])
            pose = SubElement(object_item, 'pose')
            pose.text = str(each_object['pose'])
            truncated = SubElement(object_item, 'truncated')
            truncated.text = "0"
            difficult = SubElement(object_item, 'difficult')
            difficult.text = "0"
            bndbox = SubElement(object_item, 'bndbox')
            x = SubElement(bndbox, 'x')
            x.text = str(each_object['x'])
            y = SubElement(bndbox, 'y')
            y.text = str(each_object['y'])
            width = SubElement(bndbox, 'width')
            width.text = str(each_object['width'])
            height = SubElement(bndbox, 'height')
            height.text = str(each_object['height'])


    def save(self, targetFile = None):
        root = self.genXML()
        self.appendObjects(root)
        out_file = None
        if targetFile is None:
            out_file = open(self.filename + '.xml','w')
        else:
            out_file = open(targetFile, 'w')

        out_file.write(self.prettify(root))
        out_file.close()


class PascalVocReader:

    def __init__(self, filepath):
        ## shapes type:
        ## [labbel, [(x1,y1), (x2,y2), (x3,y3), (x4,y4)], color, color]
        self.shapes=[]
        self.filepath = filepath
        self.parseXML()

    def getShapes(self):
        return self.shapes

    def addShape(self, label, rect, pose):
        x = rect[0]
        y = rect[1]
        width = rect[2]
        height = rect[3]
        points = [(x,y), (x,y+height), (x+width, y+height), (x+width, y)]
        self.shapes.append((label, points, pose, None, None))

    def parseXML(self):
        assert self.filepath.endswith('.xml'), "Unsupport file format"
        xmltree = ElementTree.parse(self.filepath).getroot()
        filename = xmltree.find('filename').text

        for object_iter in xmltree.findall('object'):
            rects = []
            bndbox = object_iter.find("bndbox")
            rects.append([int(it.text) for it in bndbox])
            label = object_iter.find('name').text
            pose = object_iter.find('pose').text

            for rect in rects:
                self.addShape(label, rect, pose)
        return True


# tempParseReader = PascalVocReader('test.xml')
# shape = tempParseReader.getShapes()
# print shape

# Test
# tmp = PascalVocWriter('temp','test', (10,20,3),'0 0 0')
# tmp.addBndBox(10,10,20,30,'chair','0 90 0')
# tmp.addBndBox(1,1,600,600,'car','9 0 0')
# tmp.save()

