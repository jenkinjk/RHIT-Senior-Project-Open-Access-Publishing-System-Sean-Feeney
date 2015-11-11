from wand.image import Image
import os
class PDF_To_PNG():

# Note to run this from the command line for testing purposes use:
#python -c "from PDF_To_PNG_Converter import PDF_To_PNG; PDF_To_PNG.convert(PDF_To_PNG(), open('tempfile.pdf'))"

  def convert(self, PDFname):
    p = Image(file = PDFname, format = 'png')
    p = p.sequence[0]
    p = Image(p)
    p.resize(50, 50)
    p.save(filename = "test.png") #This line is for demos
    return p

  def delete(self, fileName):
    #Delete this file
    os.remove(fileName)
