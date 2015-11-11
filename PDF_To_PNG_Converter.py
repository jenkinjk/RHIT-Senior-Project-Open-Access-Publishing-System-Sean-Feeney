from wand.image import Image
import os
class PDF_To_PNG_Converter():
def convert(self, PDFname):
p = Image(file = PDFname, format = 'png')
p = p.sequence[0]
p = Image(p)
p.resize(50, 50)
# p.save(filename = "test.png") #This line is for demos
return p
def delete(self, fileName):
#Delete this file
os.remove(fileName)
