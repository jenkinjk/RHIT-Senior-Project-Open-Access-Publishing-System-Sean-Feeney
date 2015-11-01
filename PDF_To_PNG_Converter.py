from wand.image import Image
import os
class PDF_To_PNG_Converter():


  def convert(self, PDFname):

    # Converting first page into JPG
    with Image(filename=PDFname+".pdf[0]") as img:
      img.save(filename=PDFname+".png")
    # Resizing this image
    with Image(filename=PDFname+".png") as img:
      img.resize(50, 50)
      img.save(filename=PDFname+".png")


  def delete(self, fileName):
    #Delete this file
    os.remove(fileName)
