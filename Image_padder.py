""" 
Function : Pre-Processing of image for docTR
Author : Saranya
For : Itech India Pvt Ltd

Usage : Add padding on top and bottom of a input image
"""
from PIL import Image
def padder(Image_path:str)->str:
    """Read an image from a path to add padding to it.

    Args:
        Image_path (str): path to an image file

    Returns:
        output_path : Output Path to the processed image
    """
    left_padding_percent = 10  # Adjust the percentage as needed
    right_padding_percent = 10  # Adjust the percentage as needed
    top_padding_percent = 15  # Adjust the percentage as needed
    bottom_padding_percent = 15  # Adjust the percentage as needed

    image = Image.open(Image_path)
    width, height = image.size

    left_padding = int(width * (left_padding_percent / 100))
    right_padding = int(width * (right_padding_percent / 100))
    top_padding = int(height * (top_padding_percent / 100))
    bottom_padding = int(height * (bottom_padding_percent / 100))

    new_width = width + left_padding + right_padding
    new_height = height + top_padding + bottom_padding
    canvas = Image.new('RGB', (new_width, new_height), color='white')
    canvas.paste(image, (left_padding, top_padding))
    output_path = 'temp/padded_img.png'
    canvas.save(output_path)
    return output_path
    
