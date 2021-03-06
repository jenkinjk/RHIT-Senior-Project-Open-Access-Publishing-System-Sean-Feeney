import documentHandler
import boto3
import botocore

# get credentials from file
credential_file = open('amazonCredentials.txt', 'r')
credential_file.readline()
credentials = credential_file.readline().split(',')

USER_NAME = credentials[0][1:-1]
AWS_ACCESS_KEY_ID = credentials[1]
AWS_SECRET_ACCESS_KEY = credentials[2].strip()
AWS_DEFAULT_REGION = 'us-east-1'
DOC_FOLDER = 'docs/'
THUMBNAIL_FOLDER =  'thumbnails/'

print "username:", USER_NAME
print "accesskey:",AWS_ACCESS_KEY_ID
print "secretkey:",AWS_SECRET_ACCESS_KEY

class S3DocumentHandler(documentHandler.DocumentHandler):

    def __init__(self, mode="Production"):
        session = boto3.Session(aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY, region_name='us-east-1')
        self.s3 = session.resource('s3')
        s3_client = session.client('s3')
        if mode == "Test":
            self.BUCKET_NAME = 'openaccesspub-test'
        elif mode == "Development":
            self.BUCKET_NAME = 'openaccesspub-dev'
        elif mode == "Production":
            self.BUCKET_NAME = 'openaccesspub-prod'
            
        #bucket = self.s3.Bucket(self.BUCKET_NAME)
        exists = True
        try:
            #print self.s3.meta.client.head_bucket(Bucket=self.BUCKET_NAME)
            #print s3_client.head_bucket(Bucket=self.BUCKET_NAME)
            s3_client.head_bucket(Bucket=self.BUCKET_NAME)
            print 'connected to', self.BUCKET_NAME, 'bucket'
        except botocore.exceptions.ClientError as e:
            # If a client error is thrown, then check that it was a 404 error.
            # If it was a 404 error, then the bucket does not exist.
            error_code = int(e.response['Error']['Code'])
            if error_code == 404:
                exists = False
                print 'ERROR: amazon S3 bucket', self.BUCKET_NAME, 'does not exist'
            elif error_code == 403:
                print 'ERROR: amazon S3 access is forbidden, check account credentials'

    def storeDocument(self, file, uniqueID):
        #self.s3.Object(self.BUCKET_NAME, uniqueID).put(Body=file)
        return self.s3.Object(self.BUCKET_NAME, DOC_FOLDER + uniqueID).put(Body=file)

    def storeThumbnail(self, file, uniqueID):
        #self.s3.Object(self.BUCKET_NAME, uniqueID).put(Body=file)
        return self.s3.Object(self.BUCKET_NAME, THUMBNAIL_FOLDER + uniqueID).put(Body=file)

    def documentExists(self, uniqueID):
        try:
            # just try and see if we can get metadata about it,  if so it exists
            self.s3.ObjectAcl(self.BUCKET_NAME, DOC_FOLDER + uniqueID).owner
        except botocore.exceptions.ClientError as e:
            #print 'exception:', e
            return False
        return True

    def thumbnailExists(self, uniqueID):
        try:
            # just try and see if we can get metadata about it,  if so it exists
            self.s3.ObjectAcl(self.BUCKET_NAME, THUMBNAIL_FOLDER + uniqueID).owner
        except botocore.exceptions.ClientError as e:
            #print 'exception:', e
            return False
        return True

    def retrieveDocument(self, uniqueID):
        print self.s3
        print self.s3.Object
        return self.s3.Object(self.BUCKET_NAME, DOC_FOLDER + uniqueID).get()

    def retrieveThumbnail(self, uniqueID):
        return self.s3.Object(self.BUCKET_NAME, THUMBNAIL_FOLDER + uniqueID).get()

    def retrieveDocuments(self, uniqueIDs):
        return [self.retrieveDocument(uid) for uid in uniqueIDs]

    def retrieveThumbnails(self, uniqueIDs):
        return [self.retrieveDocument(uid) for uid in uniqueIDs]

    def removeDocument(self, uniqueID):
        return self.s3.Object(self.BUCKET_NAME, DOC_FOLDER + uniqueID).delete()

    def removeThumbnail(self, uniqueID):
        return self.s3.Object(self.BUCKET_NAME, THUMBNAIL_FOLDER + uniqueID).delete()

    def removeAllNonMatching(self, uniqueIDs):
        # removes all files from the S3 datastore that don't match one of the uniqueIDs in the list
        startOfRealName = len(DOC_FOLDER)
        for obj in self.s3.Bucket(self.BUCKET_NAME).objects.filter(Prefix=DOC_FOLDER):
            if obj.key[startOfRealName:] not in uniqueIDs and obj.key != DOC_FOLDER :
                obj.delete()

        startOfRealName = len(THUMBNAIL_FOLDER)
        for obj in self.s3.Bucket(self.BUCKET_NAME).objects.filter(Prefix=THUMBNAIL_FOLDER):
            if obj.key[startOfRealName:] not in uniqueIDs and obj.key != THUMBNAIL_FOLDER :
                obj.delete()

def main():
    # test this by uploading and retrieving a pdf
    docHandler = S3DocumentHandler()
    #document = open('./pdfs/present2-2.pdf', 'rb')
    #print 'stored document', docHandler.storeDocument(document, "107")

    #file2 = docHandler.retrieveDocument('106')
    #file2['Body']
    #print 'downloaded file', file2
    #outFile = open('testDownload.pdf', 'wb')
    #outFile.write(file2['Body'].read())

    #print docHandler.documentExists('106')
    #print docHandler.documentExists('0304')

    #docHandler.removeAllNonMatching(['0', '1', '2', '3'])

if __name__ == '__main__':
    main()
