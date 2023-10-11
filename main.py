""" 
Usage : Converts table images to csv file.
Author : Saranya
For : Itech India Pvt Ltd

"""


import cv2
import numpy as np
from PIL import Image
import easyocr
import Levenshtein
import pandas as pd

reader = easyocr.Reader(['en'],gpu=True) 

def image_preprocessing(image_path:str)->None:
    """Takes a image path, preprocess the image for ocr and saves
       the processed image in the local working directory

    Args:
       image_path: Url for the image location.
    
    Returns:
        None
    
    """
    im = Image.open(image)
    im.save("test-600.png", dpi=(300,300))
    image = cv2.imread("test-600.png")
    _, binary_image = cv2.threshold(image, 130, 255, cv2.THRESH_BINARY)
    cv2.imwrite('binary_image.jpg', binary_image)
    im = Image.open('binary_image.jpg')
    im.save("test-601.png", dpi=(300,300))

    
def ocr(image:Image)->list:
    """Takes a image extracts the text and the text coordinates. 
       Returns the output in a list.

    Args:
       image: Image file
    
    Returns:
        List of words and coordinate 
        eg - [....  [[x1,y1], [x2,y2],[x3,y3],[x4,y4]], word]   ....]
    
    """
    output=reader.readtext(image)
    return output


def runner(image_path:str, headers:list)->None:
    """Takes a image of table path, and convert the table image to csv.

    Args:
       image_path: Url for the image location.
       headers: List of table headers
    
    Returns:
        None
    
    """
    image_preprocessing(image_path)

    ocr_output=ocr("test-601.png")
    coordinates=list()
    words=list()
    headderCoordinates=[]
    
    for entry in ocr_output:
        coordinates.append(entry[0][0]+entry[0][2])
        words.append(entry[1])  
    
    # separating the heater tags from the ocr output:
    for title in headers:
        bestmatch=0
        best_match_word=''
        index=0
        for i,word in enumerate(words):
            levenshtein_distance = Levenshtein.distance(title.upper(), word.upper())
            percentage_match = 100 * (1 - (levenshtein_distance / max(len(title), len(word))))
            if percentage_match >= bestmatch:
                bestmatch = percentage_match
                best_match_word=word
                index=i
        coordinates[index][3]=1500
        headderCoordinates.append([coordinates[index],best_match_word])
    
    for  i in headderCoordinates:
        if i[1] in words:
            del coordinates[words.index(i[1])]
            words.remove(i[1])

    for i in range(len(coordinates)):
        coordinates[i][2]=1500

    # mapping the table containt words to the headers
    csv_dictionary=dict()
    for i in [i[1] for i in headderCoordinates]:
        csv_dictionary[i]=[]

    for index_i, i in enumerate(coordinates):
        for index_j, j in enumerate([i[0] for i in headderCoordinates]):
            x1_min, y1_min, x1_max, y1_max = i
            x2_min, y2_min, x2_max, y2_max = j
            if (x1_min < x2_max and x1_max > x2_min):
                if headderCoordinates[index_j][1] not in csv_dictionary:
                    csv_dictionary[headderCoordinates[index_j][1]]=[]
                    csv_dictionary[headderCoordinates[index_j][1]].append([i,words[index_i]])
                else:
                    csv_dictionary[headderCoordinates[index_j][1]].append([i,words[index_i]])
                break

    for i in csv_dictionary:
        for j in  range(len(csv_dictionary[i])-1,0,-1):
            if abs(csv_dictionary[i][j][0][1]- csv_dictionary[i][j-1][0][1]) <=3:
                print( csv_dictionary[i][j-1][1], csv_dictionary[i][j][1])
                csv_dictionary[i][j-1][1]  = csv_dictionary[i][j-1][1]+ " "+ csv_dictionary[i][j][1]
                csv_dictionary[i][j]='to_be_removed'
    
    for i in csv_dictionary:
        while 'to_be_removed' in csv_dictionary[i]:
            csv_dictionary[i].remove('to_be_removed')

    cell_posY=list()
    for i in coordinates:
        if i[1] not in cell_posY:
            cell_posY.append(i[1])
    
    for i in csv_dictionary:
        if csv_dictionary[i]:
            for index, j in enumerate(csv_dictionary[i]):
                csv_dictionary[i][index][0]=(0,cell_posY.index(j[0][1]))
    
    # making csv from the mapped dictionary of words to headers
    csv_df=dict()
    max_col=0
    for i in csv_dictionary:
        csv_df[i]=[]
        for j in csv_dictionary[i]:
            if j[0][1]>max_col:
                max_col= j[0][1]


    for i in csv_df:
        for j in range(max_col+1):
            csv_df[i].append(np.NaN)

    for i in csv_df:
        if csv_dictionary[i]:
            for index, j in enumerate(csv_dictionary[i]):
                csv_df[i][j[0][1]] = j[1]
    
    
    df = pd.DataFrame(csv_df)
    df
    df.to_csv('example.csv', index=False)



runner('/Users/901002/work/Invoice/invoice v2/6b074f8d3f9f94268e1f21987b3bcf7fc7dfaa5a76b8c8546736141b.jpg')