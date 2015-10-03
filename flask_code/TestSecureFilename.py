import unittest
import pdf_upload as pu

class TestSecureFilename(unittest.TestCase):

    # tests the 'allowed_file' function in the pdf_upload.py module
    def test_secure_filename(self):
        print('----------------------------')
        print('----------------------------')
        print('--Testing Secure Filename---')
        print('----------------------------')
        print('----------------------------')

        # list of file names that do not need modification
        secureNamesToCheck = ['something.pdf', 'something_else.txt', 'foo']
        secureNamestToCompare = ['something.pdf', 'something_else.txt', 'foo']
        for k in range(0,2):
            print('Testing for filename:', secureNamesToCheck[k])
            # make sure these files are not changed
            self.assertEqual(pu.get_secure_filename(secureNamesToCheck[k]), secureNamestToCompare[k], 'Uh-oh')

        # list of file names that need modification
        insecureNamesToCheck = ['something with spaces.pdf', '../../something/with/slashes', 'more spaces to check']
        secureNamestToCompare = ['something_with_spaces.pdf', 'something_with_slashes', 'more_spaces_to_check']
        for k in range(0,2):
            print('Testing for filename:', insecureNamesToCheck[k])
            # make sure these filenames are converted
            self.assertEqual(pu.get_secure_filename(insecureNamesToCheck[k]), secureNamestToCompare[k], 'Uh-oh')

if __name__ == '__main__':
    unittest.main()