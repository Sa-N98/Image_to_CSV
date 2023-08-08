import Image_padder as ip
from docTR import docTr
from make_CSV import make_csv


path='/Users/901002/work/Invoice/Main/TEST/Screenshot 2023-07-28 at 3.13.08 PM.png'
word_coordinates=docTr(ip.padder(path,100,100))

make_csv(data=word_coordinates, headers_list=['Description', 'Type', 'Units', 'PerUnit', 'FxRate', 'Total'])