import documentHandler
import boto3
import botocore

BUCKET_NAME = 'openaccesstemp'
USER_NAME = 'openAccessServer'
AWS_ACCESS_KEY_ID = 'AKIAIINGYMLIHZOKZU3A'
AWS_SECRET_ACCESS_KEY = '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'
AWS_DEFAULT_REGION = 'us-east-1'

class S3DocumentHandler(documentHandler.DocumentHandler):

    def __init__(self):
        session = boto3.Session(aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY, region_name='us-east-1')
        #self.s3 = session.resource('s3')
        self.s3 = session.client('s3')
        #bucket = self.s3.Bucket(BUCKET_NAME)
        exists = True
        try:
            #print self.s3.meta.client.head_bucket(Bucket=BUCKET_NAME)
            print self.s3.head_bucket(Bucket=BUCKET_NAME)
            print 'connected to', BUCKET_NAME, 'bucket'
        except botocore.exceptions.ClientError as e:
            # If a client error is thrown, then check that it was a 404 error.
            # If it was a 404 error, then the bucket does not exist.
            error_code = int(e.response['Error']['Code'])
            if error_code == 404:
                exists = False
                print 'ERROR: bucket', BUCKET_NAME, 'does not exist'

    def storeDocument(self, file):
        # stores the file and returns its uniqueID key that can be used to access
        # it later
        uniqueID = '00002' # or could use some variant of file.name
        #self.s3.Object(BUCKET_NAME, uniqueID).put(Body=file)
        self.s3.put_object(Body=file, Bucket=BUCKET_NAME, Key=uniqueID)
        return uniqueID

    def documentExists(self, uniqueID):
        try:
            self.s3.get_object_acl(Bucket=BUCKET_NAME, Key=uniqueID)
        except botocore.exceptions.ClientError as e:
            #print 'exception:', e
            return False
        return True

    def retrieveDocument(self, uniqueID):
        return self.s3.get_object(Bucket=BUCKET_NAME, Key=uniqueID)

    def retrieveDocuments(self, uniqueIDs):
        return [self.retrieveDocument(uid) for uid in uniqueIDs]

    def removeDocument(self, uniqueID):
        return self.s3.delete_object(Bucket=BUCKET_NAME, Key=uniqueID)


def main():
    # test this by uploading and retrieving a pdf
    docHandler = S3DocumentHandler()
    #document = open('./pdfs/present2-2.pdf', 'rb')
    #uid = docHandler.storeDocument(document)
    #print 'stored document, uid =', uid

    #file2 = docHandler.retrieveDocument('00003')
    #file2['Body']
    #print 'downloaded file', file2
    #outFile = open('testDownload.pdf', 'wb')
    #outFile.write(file2['Body'].read())

    print docHandler.documentExists('00002')
    print docHandler.documentExists('00004')

if __name__ == '__main__':
    main()