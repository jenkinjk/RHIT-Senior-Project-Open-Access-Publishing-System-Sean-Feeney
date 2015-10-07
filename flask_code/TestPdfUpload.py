import unittest
import pdf_upload as pu

class TestPdfUpload(unittest.TestCase):

    # tests the 'allowed_file' function in the pdf_upload.py module
    def test_allowed_file(self):
        print('-------------------------')
        print('-------------------------')
        print('--Testing Allowed File---')
        print('-------------------------')
        print('-------------------------')

        # list of allowable file extensions
        goodextensions = ['excel.pdf', 'word.pdf', 'powerpoint.pdf']
        for filext in goodextensions:
            print('Testing for file ext:', filext)
            # make sure these files are checked and are allowed
            self.assertTrue(pu.allowed_file(filext))

        # list of not allowed file extensions
        badextensions = ['excel.xlsx', 'word.docx', 'powerpoint.ppt, executable.exe']
        for filext in badextensions:
            print('Testing for file ext:', filext)
            # make sure these files are checked and NOT allowed
            self.assertFalse(pu.allowed_file(filext))

if __name__ == '__main__':
    unittest.main()