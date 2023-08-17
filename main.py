import Image_padder as ip
from docTR import docTr
from make_CSV import make_csv


path='/Users/901002/work/Invoice/Samples/45436b1fb879160aea90ce6e3dd21e7da087a465954b302ecb69567d.jpg'
word_coordinates=docTr(ip.padder(path,1000,800),True)

make_csv(data=word_coordinates, headers_list=['Description', 'Type', 'Per Unit', 'Units', 'FxRate', 'Total'])