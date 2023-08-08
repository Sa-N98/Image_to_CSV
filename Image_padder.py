""" 
Function : Pre-Processing of image for docTR
Author : Saranya
For : Itech India Pvt Ltd

Usage : Add padding on top and bottom of a input image
"""
from PIL import Image
def padder(Image_path:str,top_padding:int,bottom_padding:int)->str:
    """Read an image from a path to add padding to it.

    Args:
        Image_path (str): path to an image file
        top_padding (int): Padding at the top
        bottom_padding (int): Padding at the bottom

    Returns:
        output_path : Output Path to the processed image
    """
    image = Image.open(Image_path)
    width, height = image.size
    new_height = height + top_padding + bottom_padding
    canvas = Image.new('RGB', (width, new_height), color='white')
    canvas.paste(image, (0, top_padding))
    output_path = 'temp/padded_img.png'
    canvas.save(output_path)
    return output_path
    
