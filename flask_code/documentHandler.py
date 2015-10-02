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
        self.saved_data = os.path.join(self.upload_folder, 'simpleDocHandlerData.p')
        self.temp_fp = None
        if(os.path.isfile(self.saved_data)):
            # if the pickled already_seen set is present, load it
            data_file = open(self.saved_data, 'rb')
            self.already_seen = cPickle.load(data_file)
            data_file.close()
        else:
            # else create a new one
            self.already_seen = set()
        print 'document store entries:', self.already_seen

    def storeDocument(self, file):
        # stores the file and returns its uniqueID key that can be used to access
        # it later
        filename = secure_filename(file.filename)
        file.save(os.path.join(self.upload_folder, filename))
        self.already_seen.add(filename)

        # now we save our set of already_seen uniqueIDs in case the server stops running
        data_file = open(self.saved_data, 'wb')
        cPickle.dump(self.already_seen, data_file, -1)
        data_file.close()

        # now generate and return the UniqueID for that stored file.  in reality this 
        # should probably be a long integer, but for now a string works
        uniqueID = filename
        return uniqueID

    def documentExists(self, uniqueID):
        return uniqueID in self.already_seen

    def retrieveDocument(self, uniqueID):
        self.temp_fp = open(os.path.join(self.upload_folder, uniqueID), 'r')
        return self.temp_fp

    def retrieveDocuments(self, uniqueIDs):
        return [self.retrieveDocument(uid) for uid in uniqueIDs]

