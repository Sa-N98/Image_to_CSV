import Image_padder as ip
from docTR import docTr
from make_CSV import make_csv


path='TEST/a80bc3bc2a9fb28faba44cf6f64ce8e58cafb8d1575f2557e7eb497e.jpg'
word_coordinates=docTr(ip.padder(path,100,100))

make_csv(data=word_coordinates, headers_list=['Description', 'Qty', 'Basis', 'Rate', 'Charge'])