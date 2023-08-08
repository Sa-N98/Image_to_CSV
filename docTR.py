""" 
Function : Pre-Processing output of docTR output
Author : Saranya
For : Itech India Pvt Ltd

Usage : Converts the docTR output in to list of word and its location coordinate in given Image.
        NOTE: Import function docTr from the module.
"""

from PIL import Image
import torch
import torchvision
from torchvision.io import read_image
from torchvision.utils import draw_bounding_boxes
from doctr.io import DocumentFile
from doctr.models import ocr_predictor


model = ocr_predictor(det_arch='db_resnet50', reco_arch='crnn_vgg16_bn', pretrained=True)

def OCR(Image_path:str)->dict:
    """Read an image from a path to the OCR

    Args:
        Image_path (str): path to an image file

    Returns:
        Dictionary : Dictionary containing info regarding words in the image
    """
    
    single_img_doc = DocumentFile.from_images(Image_path)
    result = model(single_img_doc)
    dict_output = result.export()
    return dict_output

def JSON_Processor(Json:dict)->list:
    """Extracts the words and there coordinates and stores then in two separate list for docTR dictionary.
       NOTE: The list  of words and coordinates are mapped 
       i.e word in the first index of the label list maps to the coordinates in the first index of the bbox_coordinates list

    Args:
        Json (dict): DocTR output dictionary.

    Returns:
        lables : list containing words in the image.
        bbox_coordinates : List of coordinates of the words in the image.
    """

    word_coordinate_pairs=list()
    image_height,image_width =Json['pages'][0]['dimensions']

    for pages in Json['pages']:
        for blocks in pages['blocks']:
            temp=list()
            for word in blocks['lines'][0]['words']:
                temp.append([word ['value'],
                    [word ['geometry'][0][0] * image_width,
                    word ['geometry'][0][1] * image_height,
                    word ['geometry'][1][0] * image_width,
                    word ['geometry'][1][1] * image_height]])
            word_coordinate_pairs.append(temp)
    # further processing to pair words of same sentance or cell.
    for items in word_coordinate_pairs:
        if len(items)>1:
            for i in range(len(items) - 1):
                first_entry = items[i]
                second_entry = items[i + 1]
                if second_entry[1][0] - first_entry[1][2]<3:
                    items[i]='remove'
                    items[i + 1]=[first_entry[0]+' '+second_entry[0], [first_entry[1][0],first_entry[1][1],second_entry[1][2],second_entry[1][3]]]         

    for items in word_coordinate_pairs:
        if len(items)>1:
            while 'remove' in items:
                items.remove('remove')

    lables=list()
    bbox_coordinates=list() 

    for items in word_coordinate_pairs:
        for item in  items:
            lables.append(item[0])
            bbox_coordinates.append(item[1])
    return lables,bbox_coordinates

def visualizer(Image_path:str,bbox_coordinates:list,lables:list):
    """Read an image from a path torchvision for drawing border boxes.

    Args:
        Image_path (str): path to an image file
        bbox_coordinates (list): List of x-min, y-min, x-max, y-max coordinates
        lables (list): List of words 

    Returns:
        None
    """
    Image.open(Image_path).convert("RGB").save(Image_path)
    img = read_image(Image_path)
    bbox = torch.tensor(bbox_coordinates, dtype=torch.int)
    image_out = torchvision.transforms.ToPILImage()(draw_bounding_boxes(img, bbox, width=2, colors=(255,0,0),fill =False,labels= lables,font_size=1500 ))
    image_out.show()

def docTr(Image_path:str ,visualize=False)->list:
    """Read an image to extract the words and their coordinate location.

    Args:
        Image_path (str): path to an image file
        visualize (bool): By default False, Set it to True to get the labeled image
        

    Returns:
       A list of words with there coordinates.
       EXAMPLE: [ .... ['Ocean Freight', [0.0, 136.013671875, 137.314453125, 159.498046875]] ....]
                
    """
    lables,bbox_coordinates=JSON_Processor(OCR(Image_path))
    if visualize:
        visualizer(Image_path=Image_path,bbox_coordinates=bbox_coordinates,lables=lables)
    return [ [word, coordinates] for word ,coordinates in zip(lables, bbox_coordinates)]


# print(docTr('/Users/901002/work/Invoice/padded_image.png'))