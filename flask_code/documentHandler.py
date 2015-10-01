from werkzeug import secure_filename
import os

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
        self.already_seen = set()

    def storeDocument(self, file):
        # stores the file and returns its uniqueID key that can be used to access
        # it later
        filename = secure_filename(file.filename)
        file.save(os.path.join(self.upload_folder, filename))
        self.already_seen.add(filename)
        # now generate and return the UniqueID for that stored file.  in reality this 
        # should probably be a long integer, but for now a string works
        uniqueID = filename
        return uniqueID

    def documentExists(self, uniqueID):
        return uniqueID in self.already_seen

    def retrieveDocument(self, uniqueID):
        return open(os.path.join(self.upload_folder, uniqueID), 'r')

    def retrieveDocuments(self, uniqueIDs):
        return [self.retrieveDocument(uid) for uid in uniqueIDs]

