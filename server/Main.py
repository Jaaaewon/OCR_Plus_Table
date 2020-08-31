import cv2
import numpy as np
import glob,os
from ImageProcessing import *
from Contour import *
from File import *
from MakeTable import *
from Sort import *
from mExcel import *
#from MakeTable.Preprocessing import *

#from TFOCR.TFmain import *

def Cmain(inputdir,imagePath, type,resultdir, model=0):
    #imagePath = './Test/t11.jpg'
    #imagePath = 'test4.jpg'

    # image = cv2.imread(inputdir+imagePath+ type)
    image = cv2.imread(imagePath+ type)
    # cv2.imshow("opening", cv2.resize(image, dsize=(0, 0), fx=0.2, fy=0.2, interpolation=cv2.INTER_LINEAR))
    # cv2.waitKey(0)
    fileList = glob.glob("./TableCrop/*"+ type)
    for f in fileList:
        os.remove(f)
    fileList = glob.glob("./TextCrop/*" + type)
    for f in fileList:
        os.remove(f)
    print("doc")
    print(image.shape)

    # 표만들기 ================================================================================
    resizeFile(image)
    # print(cv2.imread(image).shape)
    main_process = Export2Document.Export2Document('document.jpg', verbose='v')
    main_process.process()
    main_process.ocr_by_box()
    main_process.export_to_xlsx()
    index_list = main_process.get_cell_index()
    # print("===========================indexlist")
    # ========================================================================================

    # 글자따기 ================================================================================
    #croppedImages, coordinateList = processImage(imagePath+'.jpg')  # process the image and get cropped screenshot
    croppedImages, coordinateList = processImage(image)  # process the image and get cropped screenshot

    count = 0
    print(len(croppedImages))
    for cropImage in croppedImages:
        count += 1
        saveImage(cropImage, "./TextCrop/crop_" + str(count))
    # ===================    == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == =

    # 정렬하기 ================================================================================

    #xmlP(coordinateList)
    # print(index_list)
    #fontsize = getFontsize(coordinateList)
    root = set_base_xml(index_list, coordinateList)
    # makeExcel(root,resultdir+imagePath)
    makeExcel(root,imagePath)

    main_process = Preprocessing.Preprocessing('document.jpg', verbose='v')
    main_process.process()
    sortImages = main_process.cal_cell_needed()
    #print(sortImages)
    # ========================================================================================

# if __name__ == '__main__':
#     #model = load_Model()
#     # Cmain(dirPath='./TestCase/', imagePath='testcase5', type='.jpg', resultdir='./TestResult/')
#     Cmain(inputdir='./TestCase/',imagePath='2020915319', type='.jpg', resultdir='./TestResult/')
#     # Cmain(dirPath='./TestCase/', imagePath='_erased_img', type='.png', resultdir='./TestResult/')


