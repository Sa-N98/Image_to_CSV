import Image_padder as ip
from docTR import docTr
from make_CSV import make_csv


path='/Users/901002/work/Invoice/Samples/8dff599aa668fe37a757420b23d28b6706ed7ed06558017eb8192e78.jpg'
word_coordinates=docTr(ip.padder(path,100,100),True)

make_csv(data=word_coordinates, headers_list=['Description', 'Quantity', 'Quantité', 'Code Code', 'Weight Poids', 'Rate', 'Discount%', 'Gross Amount', 'Net Amount'])