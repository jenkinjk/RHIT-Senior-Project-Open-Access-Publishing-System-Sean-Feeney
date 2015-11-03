from werkzeug import secure_filename
import os
import cPickle

class DocumentHandler:
    # interface for storing documents as (uniqueID, data) pairs
    def storeDocument(self, file):
        # stores the file and returns its uniqueID key that can be used to access
        # it later
        return "STORE DOCUMENT NOT IMPLEMENTED"

    def documentExists(self, uniqueID):
        return "DOCUMENT EXISTS NOT IMPLEMENTED"

    def retrieveDocument(self, uniqueID):
        return "RETRIEVE DOCUMENT NOT IMPLEMENTED"

    def retrieveDocuments(self, uniqueIDs):
        return "RETRIEVE DOCUMENTS NOT IMPLEMENTED"

    def removeDocument(self, uniqueID):
        return "REMOVE DOCUMENT NOT IMPLEMENTED"


class SimpleDocHandler(DocumentHandler):
    # simple storage handler that sticks them on the filesystem
    def __init__(self):
        self.upload_folder = './pdfs'
        self.temp_fp = None

    def storeDocument(self, file, uniqueID):

        filename = secure_filename(uniqueID)
        file.save(os.path.join(self.upload_folder, os.path.join("docs/", uniqueID)))

    def retrieveDocument(self, uniqueID):
        self.temp_fp = open(os.path.join(self.upload_folder, os.path.join("docs/", uniqueID)), 'r')
        return self.temp_fp
